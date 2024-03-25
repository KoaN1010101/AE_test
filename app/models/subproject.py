from app.core.db import Base
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.models.task import Task


class SubProject(Base):
    __tablename__ = "subprojects"
    title = Column(String, index=True, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"))
    tasks = relationship("Task", cascade='delete')
