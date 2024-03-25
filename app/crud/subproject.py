from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.subproject import SubProject
from app.schemas.subproject import SubProjectCreate, SubProjectUpdate


class CRUDSubproject(CRUDBase):

    async def get_subproject_id_by_title(
            self,
            subproject_title: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_subproject_id = await session.execute(
            select(SubProject.id).where(
                SubProject.title == subproject_title
            )
        )
        db_subproject_id = db_subproject_id.scalars().first()
        return db_subproject_id


subproject_crud = CRUDSubproject(SubProject)
