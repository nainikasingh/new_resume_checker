from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.endpoints.upload import router as upload_router
<<<<<<< HEAD
from flask import Flask
from flask_cors import CORS
=======
from pdf2image import convert_from_bytes
import base64
from io import BytesIO


>>>>>>> 38b0cc63ae5fb89036b2240fb1e5e5b8811748a9

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
<<<<<<< HEAD
=======

@app.post("/preview/")
async def generate_preview(file: UploadFile = File(...)):
    # Read the PDF file into memory
    pdf_data = await file.read()
    
    # Convert the PDF pages to images
    images = convert_from_bytes(pdf_data)
    
    # Encode the images as base64 strings with numbered labels
    preview_images = []
    for i, img in enumerate(images):
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        preview_images.append({
            "page": i + 1,
            "image": f"data:image/jpeg;base64,{img_base64}"
        })
    
    # Return the numbered images
    return JSONResponse(content={"preview_images": preview_images})
>>>>>>> 38b0cc63ae5fb89036b2240fb1e5e5b8811748a9
