def init_database_scheme(db):
    user_fields = {
        "id": "INT",
        "name": "TEXT",
        "email": "TEXT",
        "email_verified": "BOOL",
    }
    db.init_table("users", user_fields, primary_key="id")
    
    org_fields = {
        "id": "INT",
        "name": "TEXT",
        "owner_id": ("FOREIGN KEY", "users(id)"),
    }
    db.init_table("orgs", org_fields, primary_key="id")

    tokens_fields = {
        "id": "INT",
        "token": "TEXT",
        "owner_id": ("FOREIGN KEY", "users(id)"),
    }
    db.init_table("tokens", tokens_fields, primary_key="id")

    code_fields = {
        "id": "INT",
        "code": "TEXT",
        "email": "TEXT",
    }
    db.init_table("codes", code_fields, primary_key="id")