from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, profile
from app.middleware import log_requests
from app.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("=" * 50)
    logger.info("Profile Management API Starting...")
    logger.info("=" * 50)
    
    yield
    
    # Shutdown
    logger.info("=" * 50)
    logger.info("Profile Management API Shutting Down...")
    logger.info("=" * 50)


app = FastAPI(
    title="Profile Management System",
    lifespan=lifespan
)

# Add logging middleware
app.middleware("http")(log_requests)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(profile.router)


@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "Profile Management System API is running"}