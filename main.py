
from contextlib import asynccontextmanager

from fastapi import FastAPI


from database import Base, engine
from routers.auth import router as auth_router
from routers.tasks import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(
    title="Tasks API",
    lifespan=lifespan,
)


app.include_router(auth_router)
app.include_router(tasks_router)

    
