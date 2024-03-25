from app.core.db import Base
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import (
    Boolean,
    Column,
    String,
)


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"
    username = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
