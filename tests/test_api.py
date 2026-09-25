from datetime import date

import httpx
import pytest
from fastapi.testclient import TestClient

from app.main import create_app


def payload(**overrides):
    return {'nome': 'Nuvem', 'categoria': 'Produtividade', 'valor': '29.90', 'moeda': 'BRL',
            'periodicidade': 'mensal', 'proxima_cobranca': '2026-10-10', 'ativo': True, **overrides}


@pytest.fixture
def client(tmp_path):
    with TestClient(create_app(str(tmp_path / 'test.db'))) as client:
        yield client


def test_crud_filters_pagination_and_persistence(tmp_path):
    app = create_app(str(tmp_path / 'persistent.db'))
    with TestClient(app) as client:
        created = client.post('/assinaturas', json=payload())
        assert created.status_code == 201
        item_id = created.json()['id']
        client.post('/assinaturas', json=payload(nome='Outro', ativo=False))
        listing = client.get('/assinaturas', params={'ativo': True, 'categoria': 'PRODUTIVIDADE', 'limite': 1}).json()
        assert listing['total'] == 1
        assert listing['itens'][0]['valor'] == '29.9'
        assert client.get('/assinaturas?offset=2').json()['itens'] == []
        assert client.put(f'/assinaturas/{item_id}', json=payload(valor='49.99')).status_code == 200
    with TestClient(create_app(str(tmp_path / 'persistent.db'))) as client:
        assert client.get('/assinaturas').json()['itens'][0]['valor'] == '49.99'
        assert client.delete(f'/assinaturas/{item_id}').status_code == 204
        assert client.delete(f'/assinaturas/{item_id}').status_code == 404
        assert client.put(f'/assinaturas/{item_id}', json=payload()).status_code == 404


@pytest.mark.parametrize('changes', [{'valor': '-1'}, {'valor': '1.001'}, {'valor': 'NaN'},
                                     {'nome': '  '}, {'moeda': 'ABC'}, {'proxima_cobranca': 'ontem'},
                                     {'periodicidade': 'semanal'}, {'campo_extra': True}])
def test_invalid_input(client, changes):
    assert client.post('/assinaturas', json=payload(**changes)).status_code == 422
    assert client.get('/assinaturas').json()['total'] == 0


def test_query_validation_and_unknown_simulation(client):
    assert client.get('/assinaturas?ordem=valor').status_code == 422
    assert client.get('/assinaturas?limite=0').status_code == 422
    assert client.get('/analises/economia?excluir_ids=999').status_code == 422
    assert client.get('/analises/projecao?meses=0').status_code == 422


def test_exchange_and_analysis_integration(tmp_path):
    captured = []

    def handler(request):
        if request.url.host == 'api.frankfurter.dev':
            assert request.url.path == '/v2/rate/usd/brl'
            return httpx.Response(200, json={'base': 'USD', 'quote': 'BRL', 'rate': 5,
                                             'date': date.today().isoformat()})
        import json
        captured.append(json.loads(request.content))
        return httpx.Response(200, json={'moeda': 'BRL', 'mensal': '100.00'})

    with TestClient(create_app(str(tmp_path / 'integration.db'), httpx.MockTransport(handler))) as client:
        client.post('/assinaturas', json=payload(valor='20.00', moeda='USD'))
        client.post('/assinaturas', json=payload(valor='30.00', moeda='USD', ativo=False))
        result = client.get('/analises/resumo')
        assert result.status_code == 200
        assert result.json()['cotacoes'][0]['taxa'] == '5'
        assert len(captured[0]['itens']) == 1
        assert captured[0]['itens'][0]['valor_centavos_brl'] == 10000


@pytest.mark.parametrize('payload_', [{}, {'base': 'EUR', 'quote': 'BRL', 'rate': 5, 'date': '2026-01-01'},
                                    {'base': 'USD', 'quote': 'BRL', 'rate': -1, 'date': '2026-01-01'}])
def test_invalid_exchange(tmp_path, payload_):
    with TestClient(create_app(str(tmp_path / 'bad.db'), httpx.MockTransport(
            lambda _: httpx.Response(200, json=payload_)))) as client:
        assert client.get('/cotacoes/USD').status_code == 502


def test_downstream_unavailable(tmp_path):
    def handler(request):
        raise httpx.ConnectError('offline', request=request)

    with TestClient(create_app(str(tmp_path / 'offline.db'), httpx.MockTransport(handler))) as client:
        assert client.get('/cotacoes/USD').status_code == 502
        assert client.get('/analises/resumo').status_code == 502
        assert client.post('/assinaturas', json=payload()).status_code == 201
        assert client.get('/cotacoes/BRL').status_code == 200


def test_openapi(client):
    schema = client.get('/openapi.json').json()
    assert set(schema['paths']['/assinaturas']) == {'get', 'post'}
    assert set(schema['paths']['/assinaturas/{assinatura_id}']) == {'put', 'delete'}
    assert client.get('/docs').status_code == 200
