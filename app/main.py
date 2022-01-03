from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth, user

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(user.router)


@app.get("/")
def root():
    return {"message": "Welcome to money transfer api service"}
