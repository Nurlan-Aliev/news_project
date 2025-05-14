from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.views import router as auth_router
from app.news.ruoters import router as news_router
from app.database import Base, db_helper
from app.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(db_helper.engine)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGIN,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth")
app.include_router(news_router, prefix="/news")
