from typing import Optional
from datetime import datetime
from sqlmodel import Field, Session, SQLModel, create_engine
from sqlalchemy import Column, Text

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    disabled: bool = False

class PoliceReport(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime
    title: str
    content: str = Field(sa_column=Column(Text))
    location: str
    url: str = Field(unique=True)

# Database connection
DATABASE_URL = "sqlite:///./police_reports.db"
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session