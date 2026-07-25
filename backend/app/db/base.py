# app/db/base.py

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class that all SQLAlchemy models inherit from.
    SQLAlchemy uses this to collect metadata about every table
    when it's time to create them or generate migrations.
    """
    pass