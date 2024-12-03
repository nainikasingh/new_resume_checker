from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.endpoints.upload import router as upload_router
from flask import Flask
from flask_cors import CORS

app = FastAPI(
    title="Resume AI Analyzer",
    description="AI-powered resume analysis and scoring system",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://nishantz3.sg-host.com","https://nishantz3.sg-host.com"],  # Allow all origins. Replace with specific origins in production.
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods: GET, POST, etc.
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(upload_router, prefix="/api/v1", tags=["Resume Analysis"])

@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - Health check"""
    return {
        "status": "online",
        "message": "Resume AI Analyzer API is running",
        "version": "1.0.0"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Service is running normally"
    }
