import os
from sqlalchemy import (
    create_engine, MetaData, Table, Column,
    Integer, String, Boolean, Float, DateTime,
    Text, ForeignKey, select
)

class SimpleDB:

    def __init__(self, db_url):
        self.engine = create_engine(db_url, pool_pre_ping=True)
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)

    def _type(self, t):
        return {
            "INT": Integer,
            "TEXT": Text,
            "VARCHAR": String(255),
            "BOOL": Boolean,
            "FLOAT": Float,
            "DATETIME": DateTime
        }.get(t.upper(), String(255))

    def init_table(self, name, fields, primary_key=None):
        if name in self.metadata.tables:
            return self.metadata.tables[name]

        columns = []

        for field, ftype in fields.items():

            if isinstance(ftype, tuple) and ftype[0] == "FOREIGN KEY":
                ref = ftype[1].replace("(", ".").replace(")", "")
                columns.append(Column(field, Integer, ForeignKey(ref)))
                continue

            col_type = self._type(ftype)

            columns.append(
                Column(
                    field,
                    col_type,
                    primary_key=(field == primary_key),
                    autoincrement=(field == primary_key)
                )
            )

        table = Table(name, self.metadata, *columns)
        table.create(self.engine)

        self.metadata.reflect(bind=self.engine)
        return table

    def insert(self, table_name, data):
        table = self.metadata.tables[table_name]

        with self.engine.begin() as conn:
            conn.execute(table.insert().values(**data))

    def select(self, table_name, where=None):
        table = self.metadata.tables[table_name]
        stmt = select(table)

        if where:
            for k, v in where.items():
                stmt = stmt.where(table.c[k] == v)

        with self.engine.connect() as conn:
            return conn.execute(stmt).mappings().all()

    def select_one(self, table_name, where):
        rows = self.select(table_name, where)
        return rows[0] if rows else None

    def update(self, table_name, where, data):
        table = self.metadata.tables[table_name]
        stmt = table.update()

        if where:
            for k, v in where.items():
                stmt = stmt.where(table.c[k] == v)

        with self.engine.begin() as conn:
            conn.execute(stmt.values(**data))

db_url = os.environ.get(
    "DATABASE_LINK",
    "sqlite:////tmp/local.db"
)

db = SimpleDB(db_url)
