from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth, projects, activities, analytics, ai

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DevInsight AI API",
    description="AI Developer Productivity & Code Risk Analysis Platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(activities.router)
app.include_router(analytics.router)
app.include_router(ai.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to DevInsight AI API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
