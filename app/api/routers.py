from fastapi import APIRouter

from app.api.endpoints import project_router, subproject_router, task_router, user_router

main_router = APIRouter()
main_router.include_router(
    project_router, prefix='/projects', tags=['Projects']
)
main_router.include_router(
    subproject_router, prefix='/subprojects', tags=['SubProjects']
)
main_router.include_router(
    task_router, prefix='/tasks', tags=['Tasks']
)

main_router.include_router(user_router)
