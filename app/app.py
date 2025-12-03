from fastapi import FastAPI

from app.routers import auth, profile


app = FastAPI(title="Profile Management System")


app.include_router(auth.router)
app.include_router(profile.router)


