from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator
from app.models.task import TaskType, StatusType

CREATION_DATE = (
    datetime.now() + timedelta(minutes=10)
).isoformat(timespec='minutes')

MODIFICATION_DATE = (
    datetime.now() + timedelta(hours=1)
).isoformat(timespec='minutes')


class TaskBase(BaseModel):
    title: str
    description: Optional[str]
    status: StatusType
    creation_date: datetime = Field(..., example=CREATION_DATE)
    modification_date: datetime = Field(..., example=MODIFICATION_DATE)
    task_type: TaskType

    class Config:
        extra = Extra.forbid
        arbitrary_types_allowed = True
        schema_extra = {
           'example': {
               'title': 'TEST',
               'description': 'TTTEST',
               'status': 'new',
               'creation_date': CREATION_DATE,
               'modification_date': MODIFICATION_DATE,
               'project_id': 1,
               'task_type': 'manager'
            }
        }


class TaskUpdate(TaskBase):

    @validator('creation_date')
    def check_creation_date(cls, value):
        if value <= datetime.now():
            raise ValueError(
                'Время создания не может быть меньше текущего времени'
            )
        return value


class TaskCreate(TaskUpdate):
    project_id: Optional[int]
    subproject_id: Optional[int]


class TaskDB(TaskBase):
    id: int
    project_id: int
    user_id: Optional[int]

    class Config:
        orm_mode = True
