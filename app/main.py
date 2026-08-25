from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.auth import router as auth_router
from app.routers.applications import router as apps_router

# Create database tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Application Tracker API",
    version="1.0.0",
    description="Backend API for a production-style job application tracker"
)

# Configure CORS so React (running on port 5173 or 3000) can talk to FastAPI
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(apps_router, prefix="/api/v1/applications", tags=["Applications"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Job Application Tracker API"}