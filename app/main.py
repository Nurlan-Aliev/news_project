from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.auth.views import router as auth_router
from app.news.views import router as news_router
from app.database import Base, db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(db_helper.engine)
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(auth_router, prefix="/auth")
app.include_router(news_router, prefix="/news")
