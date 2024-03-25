from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_task_before_edit, check_task_permission
from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.task import task_crud
from app.models import User
from app.models.task import TaskType, StatusType
from app.schemas.task import TaskCreate, TaskDB, TaskUpdate

router = APIRouter()


@router.post(
    '/',
    summary='Создание задачи',
    response_model=TaskDB
)
async def create_task(
        task: TaskCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
        task_type: TaskType = None,
        status_type: StatusType = None,
):
    new_task = await task_crud.create(
        session, task, user, task_type, status_type
    )
    return new_task


@router.get(
    '/',
    summary='Получение задач',
    response_model=list[TaskDB]
)
async def get_all_tasks(
        session: AsyncSession = Depends(get_async_session)
):
    tasks = await task_crud.get_multi(session)
    return tasks


@router.delete(
    '/{task_id}',
    summary='Удаление задачи',
    response_model=TaskDB
)
async def delete_reservation(
        task_id: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    task = await check_task_before_edit(
        task_id, session, user
    )
    task = await task_crud.remove(
        task, session
    )
    return task


@router.patch(
    '/{task_id}',
    summary='Изменение задачи',
    response_model=TaskDB
)
async def update_task(
        task_id: int,
        obj_in: TaskUpdate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    task = await check_task_before_edit(
        task_id, session, user
    )
    if task.status != obj_in.status:
        task.modification_date = datetime.now()

    task = await task_crud.update(
        db_obj=task,
        obj_in=obj_in,
        session=session,
    )
    return task


@router.get(
    '/my_tasks',
    summary='Получение созданных собой задачи',
    response_model=list[TaskDB],
    response_model_exclude={'user_id'}
)
async def get_my_tasks(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Получает список всех задач для текущего пользователя."""
    tasks = await task_crud.get_by_user(
        session=session, user=user
    )
    return tasks
