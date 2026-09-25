import sqlite3
from contextlib import contextmanager
from pathlib import Path
from decimal import Decimal

from .models import SubscriptionInput


class Database:
    def __init__(self, path: str):
        self.path = path

    @contextmanager
    def connection(self):
        connection = sqlite3.connect(self.path, timeout=10)
        connection.row_factory = sqlite3.Row
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def initialize(self):
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as connection:
            connection.execute('''CREATE TABLE IF NOT EXISTS assinaturas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                categoria TEXT NOT NULL,
                valor_centavos INTEGER NOT NULL CHECK(valor_centavos > 0),
                moeda TEXT NOT NULL CHECK(moeda IN ('BRL','USD','EUR','GBP')),
                periodicidade TEXT NOT NULL CHECK(periodicidade IN ('mensal','anual')),
                proxima_cobranca TEXT NOT NULL,
                ativo INTEGER NOT NULL CHECK(ativo IN (0,1))
            )''')

    @staticmethod
    def decode(row):
        item = dict(row)
        item['valor'] = Decimal(item.pop('valor_centavos')) / 100
        item['ativo'] = bool(item['ativo'])
        return item

    @staticmethod
    def values(item: SubscriptionInput):
        return (item.nome, item.categoria, int(item.valor * 100), item.moeda,
                item.periodicidade, item.proxima_cobranca.isoformat(), int(item.ativo))

    def create(self, item):
        with self.connection() as connection:
            cursor = connection.execute('''INSERT INTO assinaturas
                (nome,categoria,valor_centavos,moeda,periodicidade,proxima_cobranca,ativo)
                VALUES (?,?,?,?,?,?,?)''', self.values(item))
            return self.decode(connection.execute('SELECT * FROM assinaturas WHERE id=?', (cursor.lastrowid,)).fetchone())

    def replace(self, item_id, item):
        with self.connection() as connection:
            cursor = connection.execute('''UPDATE assinaturas SET nome=?,categoria=?,valor_centavos=?,
                moeda=?,periodicidade=?,proxima_cobranca=?,ativo=? WHERE id=?''', self.values(item) + (item_id,))
            if cursor.rowcount == 0:
                return None
            return self.decode(connection.execute('SELECT * FROM assinaturas WHERE id=?', (item_id,)).fetchone())

    def delete(self, item_id):
        with self.connection() as connection:
            return connection.execute('DELETE FROM assinaturas WHERE id=?', (item_id,)).rowcount > 0

    def list(self, categoria=None, ativo=None, ordem='cobranca', limite=None, offset=0):
        clauses, values = [], []
        if categoria is not None:
            clauses.append('categoria=?')
            values.append(categoria.strip().casefold())
        if ativo is not None:
            clauses.append('ativo=?')
            values.append(int(ativo))
        where = (' WHERE ' + ' AND '.join(clauses)) if clauses else ''
        order = {'cobranca': 'proxima_cobranca, id', 'nome': 'nome COLLATE NOCASE, id'}[ordem]
        with self.connection() as connection:
            total = connection.execute('SELECT COUNT(*) FROM assinaturas' + where, values).fetchone()[0]
            query = 'SELECT * FROM assinaturas' + where + ' ORDER BY ' + order
            if limite is not None:
                query += ' LIMIT ? OFFSET ?'
                values += [limite, offset]
            return total, [self.decode(row) for row in connection.execute(query, values).fetchall()]
