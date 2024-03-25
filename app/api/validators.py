from fastapi import HTTPException, Security
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.project import project_crud
from app.crud.subproject import subproject_crud
from app.crud.task import task_crud
from app.models import Project, Task, User, SubProject

from fastapi.security import OAuth2PasswordBearer
from app.core.user import current_user


async def check_title_duplicate(
        project_title: str,
        session: AsyncSession,
) -> None:
    project_id = await project_crud.get_project_id_by_title(project_title, session)
    if project_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Проект с таким названием уже существует!',
        )


async def check_subproject_title_duplicate(
        subproject_title: str,
        session: AsyncSession,
) -> None:
    subproject_id = await subproject_crud.get_subproject_id_by_title(subproject_title, session)
    if subproject_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Подпроект с таким названием уже существует!',
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> Project:
    project = await project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return project


async def check_subproject_exists(
        subproject_id: int,
        session: AsyncSession,
) -> SubProject:
    subproject = await project_crud.get(subproject_id, session)
    if subproject is None:
        raise HTTPException(
            status_code=404,
            detail='Подпроект не найден!'
        )
    return subproject


async def check_task_before_edit(
        task_id: int,
        session: AsyncSession,
        user: User,
) -> Task:
    task = await task_crud.get(
        obj_id=task_id, session=session
    )
    if not task:
        raise HTTPException(status_code=404, detail='Задача не найдена!')
    if task.user_id != user.id and not user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail='Невозможно редактировать или удалить чужую задачу!'
        )
    return task


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def check_task_permission(
    task_id: int,
    session: AsyncSession,
    user: User = Security(current_user, scopes=["user", "admin"])
):
    task = await task_crud.get(
        obj_id=task_id, session=session
    )
    if task.user_id != user.id or not user.is_admin:
        raise HTTPException(status_code=403, detail="У вас недостаточно прав")
    return task
