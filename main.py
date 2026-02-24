from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, tasks

app = FastAPI(
    title="Task Management API",
    description="A secure REST API for managing tasks with JWT authentication.",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# CORS — adjust origins for your frontend in production
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(auth.router)
app.include_router(tasks.router)


@app.get("/", tags=["Health"])
def health_check():
    """Simple health-check endpoint."""
    return {"status": "ok", "message": "Task Management API is running"}
