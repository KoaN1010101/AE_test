from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.db import Base


class TaskType(str, Enum):
    MANAGER = 'manager'
    TECHNICAL_SPECIALIST = 'technical_specialist'


class StatusType(str, Enum):
    NEW = 'new'
    PROGRESS = 'progress'
    DONE = 'done'


class Task(Base):
    __tablename__ = 'tasks'
    title = Column(String, index=True)
    description = Column(Text)
    status = Column(Enum(StatusType.NEW, StatusType.PROGRESS, StatusType.DONE), nullable=False)
    creation_date = Column(DateTime)
    modification_date = Column(DateTime)
    project_id = Column(Integer, ForeignKey('projects.id'))
    subproject_id = Column(Integer, ForeignKey('subprojects.id'))
    user_id = Column(Integer, ForeignKey('users.id', name='fk_task_user_id_user'))
    task_type = Column(Enum(TaskType.MANAGER, TaskType.TECHNICAL_SPECIALIST), nullable=False)

    def __repr__(self):
        return (
            f'Задача {self.title} со статусом {self.status} создана {self.creation_date}'
        )
