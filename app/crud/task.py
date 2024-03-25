from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Task, User


class CRUDTask(CRUDBase):

    async def get_tasks_for_project(
            self,
            project_id: int,
            session: AsyncSession,
    ):
        tasks = await session.execute(
            select(Task).where(
                Task.project_id == project_id,
            )
        )
        tasks = tasks.scalars().all()
        return tasks

    async def get_by_user(
            self, session: AsyncSession, user: User
    ):
        tasks = await session.execute(
            select(Task).where(
                Task.user_id == user.id
            )
        )
        return tasks.scalars().all()


task_crud = CRUDTask(Task)
