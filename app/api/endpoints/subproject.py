from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_subproject_exists, check_subproject_title_duplicate
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.subproject import subproject_crud
from app.crud.task import task_crud
from app.schemas.subproject import SubProjectCreate, SubProjectDB, SubProjectUpdate
from app.schemas.task import TaskDB

router = APIRouter()


@router.post(
    '/',
    summary='Создание подпроекта',
    response_model=SubProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_subproject(
        subproject: SubProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_subproject_title_duplicate(subproject.title, session)
    new_subproject = await subproject_crud.create(session, subproject)
    return new_subproject


@router.get(
    '/',
    summary='Получение всех подпроектов',
    response_model=list[SubProjectDB],
    response_model_exclude_none=True,
)
async def get_all_subproject(
        session: AsyncSession = Depends(get_async_session),
):
    all_subprojects = await subproject_crud.get_multi(session)
    return all_subprojects


@router.patch(
    '/{subproject_id}',
    summary='Изменение подпроекта',
    response_model=SubProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_subproject(
        subproject_id: int,
        obj_in: SubProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    subproject = await check_subproject_exists(
        subproject_id, session
    )

    if obj_in.title is not None:
        await check_subproject_title_duplicate(obj_in.title, session)

    subproject = await subproject_crud.update(
        subproject, obj_in, session
    )
    return subproject


@router.delete(
    '/{subproject_id}',
    summary='Удаление подпроекта',
    response_model=SubProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_subproject(
        subproject_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    subproject = await check_subproject_exists(subproject_id, session)
    subproject = await subproject_crud.remove(subproject, session)
    return subproject


@router.get(
    '/{subproject_id}/tasks',
    summary='Получение задач по подпроекту',
    response_model=list[TaskDB],
    response_model_exclude={'user_id'},
)
async def get_tasks_for_subproject(
        subproject_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    await check_subproject_exists(subproject_id, session)
    tasks = await task_crud.get_tasks_for_subproject(
        subproject_id=subproject_id, session=session
    )
    return tasks
