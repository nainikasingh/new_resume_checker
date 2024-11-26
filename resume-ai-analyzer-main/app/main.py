from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.endpoints.upload import router as upload_router
from pdf2image import convert_from_bytes
import base64
from io import BytesIO



app = FastAPI(
    title="Resume AI Analyzer",
    description="AI-powered resume analysis and scoring system",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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