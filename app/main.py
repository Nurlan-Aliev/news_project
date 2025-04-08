from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.auth.views import router as auth_router

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

app.include_router(auth_router, prefix='/auth')

