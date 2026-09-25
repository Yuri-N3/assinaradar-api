from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

Currency = Literal['BRL', 'USD', 'EUR', 'GBP']


class SubscriptionInput(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)

    nome: str = Field(min_length=1, max_length=100, examples=['Armazenamento em nuvem'])
    categoria: str = Field(min_length=1, max_length=50, examples=['Produtividade'])
    valor: Decimal = Field(gt=0, le=1000000, max_digits=9, decimal_places=2, examples=['29.90'])
    moeda: Currency = 'BRL'
    periodicidade: Literal['mensal', 'anual'] = 'mensal'
    proxima_cobranca: date
    ativo: bool = True

    @field_validator('categoria')
    @classmethod
    def normalize_category(cls, value: str) -> str:
        return value.casefold()


class Subscription(SubscriptionInput):
    id: int


class SubscriptionPage(BaseModel):
    total: int
    limite: int
    offset: int
    itens: list[Subscription]


class Quote(BaseModel):
    moeda: Currency
    destino: Literal['BRL'] = 'BRL'
    taxa: Decimal = Field(gt=0)
    data: date
    fonte: str
