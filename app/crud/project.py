from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


class CRUDProject(CRUDBase):

    async def get_project_id_by_title(
            self,
            project_title: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(Project.id).where(
                Project.title == project_title
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id


project_crud = CRUDProject(Project)
