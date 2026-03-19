def init_database_scheme(db):
    users_fields = {
        "id": "INT",
        "name": "TEXT",
        "email": "TEXT",
        "org_id": ("FOREIGN KEY", "orgs(id)"),
    }
    db.init_table("users", users_fields, primary_key="id")
    
    orgs_fields = {
        "id": "INT",
        "name": "TEXT",
        "owner_id": ("FOREIGN KEY", "users(id)"),
    }
    db.init_table("orgs", orgs_fields, primary_key="id")

    tokens_fields = {
        "id": "INT",
        "token": "TEXT",
        "owner_id": ("FOREIGN KEY", "users(id)"),
    }
    db.init_table("tokens", tokens_fields, primary_key="id")

    codes_fields = {
        "id": "INT",
        "code": "TEXT",
        "created_at": "DATETIME",
        "email": "TEXT",
    }
    db.init_table("codes", codes_fields, primary_key="id")

    tools_fields = {
        "id": "INT",
        "type": "INT",
        "name": "TEXT",
        "owner_id": ("FOREIGN KEY", "users(id)"),
    }
    db.init_table("tools", tools_fields, primary_key="id")

    plates_fields = {
        "id": "INT",
        "date": "DATETIME",
        "name": "TEXT",
        "org_id": ("FOREIGN KEY", "orgs(id)"),
        "owner_id": ("FOREIGN KEY", "users(id)"),
    }
    db.init_table("plates", plates_fields, primary_key="id")