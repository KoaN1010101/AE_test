from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_project_exists, check_title_duplicate
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.project import project_crud
from app.crud.task import task_crud
from app.schemas.project import ProjectCreate, ProjectDB, ProjectUpdate
from app.schemas.task import TaskDB

router = APIRouter()


@router.post(
    '/',
    summary='Создание проекта',
    response_model=ProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_project(
        project: ProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_title_duplicate(project.title, session)
    new_project = await project_crud.create(session, project)
    return new_project


@router.get(
    '/',
    summary='Получение всех проектов',
    response_model=list[ProjectDB],
    response_model_exclude_none=True,
)
async def get_all_projects(
        session: AsyncSession = Depends(get_async_session),
):
    all_projects = await project_crud.get_multi(session)
    return all_projects


@router.patch(
    '/{project_id}',
    summary='Изменение проекта',
    response_model=ProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_project(
        project_id: int,
        obj_in: ProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_project_exists(
        project_id, session
    )

    if obj_in.title is not None:
        await check_title_duplicate(obj_in.title, session)

    project = await project_crud.update(
        project, obj_in, session
    )
    return project


@router.delete(
    '/{project_id}',
    summary='Удаление проекта',
    response_model=ProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_project_exists(project_id, session)
    project = await project_crud.remove(project, session)
    return project


@router.get(
    '/{project_id}/tasks',
    summary='Получение задач по проекту',
    response_model=list[TaskDB],
    response_model_exclude={'user_id'},
)
async def get_tasks_for_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    await check_project_exists(project_id, session)
    tasks = await task_crud.get_tasks_for_project(
        project_id=project_id, session=session
    )
    return tasks
