import os

from contextlib import asynccontextmanager
from typing import Literal

import httpx
from fastapi import FastAPI, HTTPException, Query, Response



from .database import Database
from .models import Currency, Quote, Subscription, SubscriptionInput, SubscriptionPage
from .services import analyze, fetch_quote


def create_app(database_path=None, transport=None):
    database = Database(database_path or os.getenv('DATABASE_PATH', 'data/assinaradar.db'))
    analytics_url = os.getenv('ANALYTICS_URL', 'http://127.0.0.1:8001').rstrip('/')
    exchange_url = 'https://api.frankfurter.dev'

    @asynccontextmanager
    async def lifespan(app):
        database.initialize()
        async with httpx.AsyncClient(timeout=10, transport=transport) as client:
            app.state.client = client
            yield

    app = FastAPI(title='AssinaRadar | Assinaturas', version='1.0.0', lifespan=lifespan,
                  description='Cadastro de serviços digitais e análise de custos em reais. '
                              'Use PUT para substituir todos os campos. Valores monetários saem como strings decimais.')

    @app.get('/health', include_in_schema=False)
    def health():
        return {'status': 'ok'}

    @app.post('/assinaturas', response_model=Subscription, status_code=201, tags=['Assinaturas'],
              summary='Cadastrar assinatura')
    def create(item: SubscriptionInput):
        return database.create(item)

    @app.get('/assinaturas', response_model=SubscriptionPage, tags=['Assinaturas'],
             summary='Listar, filtrar e ordenar assinaturas')
    def listing(categoria: str | None = Query(None, max_length=50), ativo: bool | None = None,
                ordem: Literal['cobranca', 'nome'] = 'cobranca',
                limite: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0)):
        total, items = database.list(categoria, ativo, ordem, limite, offset)
        return {'total': total, 'limite': limite, 'offset': offset, 'itens': items}

    @app.put('/assinaturas/{assinatura_id}', response_model=Subscription, tags=['Assinaturas'],
             summary='Substituir assinatura ou cancelar com ativo=false', responses={404: {'description': 'Não encontrada'}})
    def replace(assinatura_id: int, item: SubscriptionInput):
        updated = database.replace(assinatura_id, item)
        if updated is None:
            raise HTTPException(404, 'Assinatura não encontrada.')
        return updated

    @app.delete('/assinaturas/{assinatura_id}', status_code=204, tags=['Assinaturas'],
                summary='Excluir assinatura', responses={404: {'description': 'Não encontrada'}})
    def delete(assinatura_id: int):
        if not database.delete(assinatura_id):
            raise HTTPException(404, 'Assinatura não encontrada.')
        return Response(status_code=204)

    @app.get('/cotacoes/{moeda}', response_model=Quote, tags=['Câmbio'],
             summary='Consultar cotação de referência e sua data', responses={502: {'description': 'Falha no câmbio'}})
    async def quotation(moeda: Currency):
        return await fetch_quote(app.state.client, exchange_url, moeda)

    @app.get('/analises/{tipo}', tags=['Análises'], summary='Analisar assinaturas ativas em reais',
             responses={422: {'description': 'IDs inválidos'}, 502: {'description': 'Falha de integração'}})
    async def analysis(tipo: Literal['resumo', 'categorias', 'projecao', 'economia'],
                       meses: int = Query(12, ge=1, le=60),
                       excluir_ids: list[int] = Query(default=[])):
        _, items = database.list(ativo=True)
        if tipo == 'economia' and not set(excluir_ids).issubset({item['id'] for item in items}):
            raise HTTPException(422, 'Informe apenas IDs de assinaturas ativas existentes.')
        return await analyze(app.state.client, analytics_url, exchange_url, items, tipo, meses, excluir_ids)

    return app


app = create_app()
