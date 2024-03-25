from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.core.db import Base
from app.models.subproject import SubProject
from app.models.task import Task


class Project(Base):
    __tablename__ = "projects"
    title = Column(String, index=True, unique=True, nullable=False)
    subproject = relationship("SubProject", cascade='delete')
    tasks = relationship("Task", cascade='delete')
