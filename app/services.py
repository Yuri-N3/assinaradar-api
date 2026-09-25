from datetime import date
from decimal import Decimal, ROUND_HALF_UP

import httpx
from fastapi import HTTPException
from pydantic import ValidationError

from .models import Quote


async def fetch_quote(client: httpx.AsyncClient, base_url: str, currency: str) -> Quote:
    if currency == 'BRL':
        return Quote(moeda='BRL', taxa=1, data=date.today(), fonte='Paridade BRL/BRL')
    try:
        response = await client.get(f'{base_url}/v2/rate/{currency.lower()}/brl')
        response.raise_for_status()
        payload = response.json()
        if payload['base'].upper() != currency or payload['quote'].upper() != 'BRL':
            raise ValueError('Par de moedas inesperado')
        quote = Quote(moeda=currency, taxa=payload['rate'], data=payload['date'], fonte='Frankfurter')
        if quote.data > date.today():
            raise ValueError('Data futura')
        return quote
    except (httpx.HTTPError, ValueError, KeyError, TypeError, AttributeError, ValidationError) as exc:
        raise HTTPException(502, 'Cotação indisponível ou inválida. Tente novamente mais tarde.') from exc


async def analyze(client, analytics_url, exchange_url, items, kind, months, excluded):
    quotes = {}
    normalized = []
    for item in items:
        currency = item['moeda']
        if currency not in quotes:
            quotes[currency] = await fetch_quote(client, exchange_url, currency)
        cents = int((item['valor'] * quotes[currency].taxa * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
        normalized.append({'id': item['id'], 'categoria': item['categoria'],
                           'valor_centavos_brl': cents, 'periodicidade': item['periodicidade']})
    body = {'itens': normalized}
    if kind == 'projecao':
        body['meses'] = months
    if kind == 'economia':
        body['excluir_ids'] = excluded
    try:
        response = await client.post(f'{analytics_url}/{kind}', json=body)
        response.raise_for_status()
        result = response.json()
        if not isinstance(result, dict) or result.get('moeda') != 'BRL':
            raise ValueError('Resposta inesperada')
    except (httpx.HTTPError, ValueError) as exc:
        raise HTTPException(502, 'Serviço de análise indisponível ou resposta inválida.') from exc
    return {'resultado': result, 'cotacoes': [q.model_dump(mode='json') for q in quotes.values()],
            'observacao': 'Estimativa das assinaturas ativas, sem impostos, IOF ou reajustes. '
                          'Valores anuais são rateados em 12 meses; não é um calendário de pagamentos.'}
