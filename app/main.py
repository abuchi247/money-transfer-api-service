from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth, user
from app.core.config import settings


def include_router(app):
    app.include_router(auth.router)
    app.include_router(user.router)


def configure_allowed_origins(app):
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def start_application():
    app = FastAPI(title=settings.project_title, version=settings.project_version)
    include_router(app)
    configure_allowed_origins(app)
    return app

#
# @app.get("/")
# def root():
#     return {"message": "Welcome to money transfer api service"}


app = start_application()