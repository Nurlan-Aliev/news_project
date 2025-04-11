from fastapi import FastAPI
from app.auth.views import router as auth_router
from app.news.views import router as news_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(news_router, prefix="/news")
