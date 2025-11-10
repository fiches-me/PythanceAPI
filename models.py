from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    email_verified: bool = False

    # Relationships
    orgs: list["Org"] = Relationship(back_populates="owner")
    tokens: list["Token"] = Relationship(back_populates="owner")

class Org(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    owner_id: int = Field(foreign_key="user.id")
    owner: User = Relationship(back_populates="orgs")

class Token(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    token: str
    owner_id: int = Field(foreign_key="user.id")
    owner: User = Relationship(back_populates="tokens")

class Code(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str
    email: str