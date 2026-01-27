from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.endpoints import router as api_router
from .db.database import engine
from .models.models import Base
from app.ollama_router import router as ollama_router
from .ollama_router import router as ollama_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Zip Listen Analytics API",
    description="Music streaming analytics API for Zip Listen",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api", tags=["analytics"])
app.include_router(ollama_router)


@app.get("/")
def read_root():
    return {
        "message": "Welcome to Zip Listen Analytics API",
        "version": "1.0.0",
        "endpoints": [
            "/api/genres/by-region",
            "/api/subscribers/by-region",
            "/api/artists/top",
            "/api/artists/rising",
            "/api/ollama/ask",
        ],
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
