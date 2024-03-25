from typing import Optional

from pydantic import BaseModel, Field, validator


class SubProjectBase(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)


class SubProjectCreate(SubProjectBase):
    title: str = Field(..., min_length=1, max_length=100)

    class Config:
        title = 'Пример'
        schema_extra = {
           'example': {
               'title': 'TEST'
           }
        }


class SubProjectUpdate(SubProjectBase):
    @validator('title')
    def title_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Название проекта не может быть пустым!')
        return value


class SubProjectDB(SubProjectBase):
    id: int

    class Config:
        orm_mode = True
