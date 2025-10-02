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
        # Rafraîchir la métadonnée pour s'assurer que toutes les tables sont connues
        self.metadata.reflect(bind=self.engine)

        if not self.inspector.has_table(table_name):
            columns = []
            for name, type_ in fields.items():
                if isinstance(type_, tuple) and type_[0] == "FOREIGN KEY":
                    ref_table, ref_column = type_[1].split("(")
                    ref_column = ref_column.rstrip(")")
                    # Vérifiez que la table référencée existe dans la métadonnée
                    if ref_table not in self.metadata.tables:
                        # Si la table existe dans la base mais pas dans la métadonnée, chargez-la
                        Table(ref_table, self.metadata, autoload_with=self.engine)
                    columns.append(Column(name, Integer, ForeignKey(f"{ref_table}.{ref_column}")))
                else:
                    columns.append(self._parse_field(name, type_))
            table = Table(table_name, self.metadata, *columns, extend_existing=True)
            table.create(self.engine)
        else:
            print(f"La table {table_name} existe déjà.")


    def _parse_field(self, name, type_):
        from sqlalchemy import Integer, String, Boolean, Float, DateTime, Text
        type_map = {
        "INT": Integer,
        "TEXT": Text,  # ici on met Text() qui est cross-DB et valide en MySQL/Postgres/SQLite
        "VARCHAR": lambda: String(255),  # toujours explicite
        "BOOL": Boolean,
        "FLOAT": Float,
        "DATETIME": DateTime,
        }

        if type_.upper() in type_map:
            t = type_map[type_.upper()]
            return Column(name, t() if callable(t) else t)

    # fallback → varchar(255) pour MySQL compat
    return Column(name, String(255))
        # fallback → varchar(255)
        return Column(name, String(255))
    def execute(self, query, params=None):
        """Exécute une requête SQL brute."""
        if params is None:
            params = ()
        # Assurez-vous que params est un tuple ou une liste de valeurs
        return self.connection.execute(text(query), params)


    def select(self, table, where=None, params=None):
        """Select rows from a table."""
        query = f"SELECT * FROM {table}"
        if where:
            query += f" WHERE {where}"
        return self.execute(query, params)

    def insert(self, table, data):
        """Insère une nouvelle ligne dans la table spécifiée."""
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        # Assurez-vous que les valeurs sont bien un tuple de valeurs simples
        values = tuple(data.values())
        print("Valeurs à insérer :", values)  # Pour le débogage
        return self.execute(query, values)

    
    def print_schema(self):
        """Imprime le schéma de la base de données."""
        print("Tables dans la base de données :")
        for table_name in self.inspector.get_table_names():
            print(f"\nTable: {table_name}")
            columns = self.inspector.get_columns(table_name)
            for column in columns:
                print(f"  - {column['name']} ({column['type']})")
            # Afficher les clés étrangères si elles existent
            fks = self.inspector.get_foreign_keys(table_name)
            for fk in fks:
                print(f"  - FK: {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")


    def close(self):
        """Close the connection."""
        self.connection.close()
