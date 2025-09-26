from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql import text
from sqlalchemy.engine.reflection import Inspector

class SimpleDB:
    """
    This code allows us to use any database provider instead of SQLite/Mysql only

    Wrotten and maintained by Guilhem @ funa.dev
    """
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.metadata = MetaData()
        self.connection = self.engine.connect()
        self.inspector = Inspector.from_engine(self.engine)

    def init_table(self, table_name, fields, primary_key=None):
        """Create a table if it doesn't exist, with support for foreign keys."""
        if not self.inspector.has_table(table_name):
            columns = []
            for name, type_ in fields.items():
                if isinstance(type_, tuple) and type_[0] == "FOREIGN KEY":
                    ref_table, ref_column = type_[1].split("(")
                    ref_column = ref_column.rstrip(")")  # Remove the closing parenthesis
                    columns.append(Column(name, Integer, ForeignKey(f"{ref_table}.{ref_column}")))
                else:
                    columns.append(self._parse_field(name, type_))
            table = Table(table_name, self.metadata, *columns, extend_existing=True)
            table.create(self.engine)


    def _parse_field(self, name, type_):
        """Convert a string type to a SQLAlchemy type."""
        from sqlalchemy import Integer, String, Boolean, Float, DateTime
        type_map = {
            "INT": Integer,
            "TEXT": String,
            "BOOL": Boolean,
            "FLOAT": Float,
            "DATETIME": DateTime,
        }
        return Column(name, type_map.get(type_.upper(), String))

    def execute(self, query, params=None):
        """Execute a raw SQL query."""
        return self.connection.execute(text(query), params or ())

    def select(self, table, where=None, params=None):
        """Select rows from a table."""
        query = f"SELECT * FROM {table}"
        if where:
            query += f" WHERE {where}"
        return self.execute(query, params)

    def insert(self, table, data):
        """Insert a row into a table."""
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        return self.execute(query, tuple(data.values()))

    def close(self):
        """Close the connection."""
        self.connection.close()
