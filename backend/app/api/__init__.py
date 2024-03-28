from fastapi import APIRouter

from .assistants import router as assistants_router
from runs import router as runs_router
from threads import router as threads_router

router = APIRouter()


@router.get("/ok")
async def ok():
    return {"ok": True}


router.include_router(
    assistants_router,
    prefix="/assistants",
    tags=["assistants"],
)
router.include_router(
    runs_router,
    prefix="/runs",
    tags=["runs"],
)
router.include_router(
    threads_router,
    prefix="/threads",
    tags=["threads"],
)
