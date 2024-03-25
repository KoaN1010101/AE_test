from datetime import datetime, timedelta

from fastapi import FastAPI
from sqlalchemy.future import select

from app.api.routers import main_router
from app.core.config import settings
from app.core.db import AsyncSessionLocal
from app.core.init_db import create_first_superuser
from app.models import Project, SubProject, Task

app = FastAPI(
    title=settings.app_title,
)

app.include_router(main_router)

CREATION_DATE = datetime.now() + timedelta(minutes=10)
MODIFICATION_DATE = datetime.now() + timedelta(hours=1)


@app.on_event('startup')
async def startup():
    await create_first_superuser()
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Project).where(Project.title == "Test Project"))
        if not result.scalars().first():
            new_project = Project(title="Test Project")
            session.add(new_project)
            await session.commit()
            await session.refresh(new_project)
        result = await session.execute(select(SubProject).where(SubProject.title == "Test SubProject"))
        if not result.scalars().first():
            new_project = SubProject(title="Test SubProject")
            session.add(new_project)
            await session.commit()
            await session.refresh(new_project)
        result = await session.execute(select(Task).where(Task.title == "Test Task"))
        if not result.scalars().first():
            new_project = Task(
                title="Test Task",
                description="Test Task",
                status="new",
                creation_date=CREATION_DATE,
                modification_date=MODIFICATION_DATE,
                project_id=1,
                user_id=1,
                task_type="manager",
            )
            session.add(new_project)
            await session.commit()
            await session.refresh(new_project)
