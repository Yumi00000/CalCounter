from fastapi import APIRouter


def get_handlers_router() -> APIRouter:
    from backend.app.api.v1.endpoints import user
    router = APIRouter()
    router.include_router(user.router)

    return router