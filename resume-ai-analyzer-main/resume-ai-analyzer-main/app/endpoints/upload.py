from fastapi import APIRouter, File, UploadFile, HTTPException
import tempfile
import os
from app.services.resume_service import analyze_resume, get_detailed_scores

router = APIRouter()

@router.post("/upload")
async def upload_and_analyze(file: UploadFile = File(...)):
    """Basic resume analysis endpoint"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Only PDF files are allowed."
        )
    
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        try:
            result = analyze_resume(temp_file_path)
            return result
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-resume")
async def detailed_resume_analysis(file: UploadFile = File(...)):
    """
    Detailed resume analysis with comprehensive scoring
    Returns:
    - Total final score
    - Grammar score
    - Action verbs score
    - ATS compatibility score
    - Keywords relevance score
    - Page length optimization score
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Only PDF files are allowed."
        )
    
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        try:
            basic_analysis = analyze_resume(temp_file_path)
            detailed_scores = get_detailed_scores(temp_file_path, basic_analysis)
            
            return {
                "detailed_scores": {
                    "total_final_score": detailed_scores["total_final_score"],
                    "grammar_final_score": detailed_scores["grammar_final_score"],
                    "action_final_score": detailed_scores["action_final_score"],
                    "ats_final_score": detailed_scores["ats_final_score"],
                    "keywords_final_score": detailed_scores["keywords_final_score"],
                    "page_length_final_score": detailed_scores["page_length_final_score"]
                },
                "analysis_details": basic_analysis,
                "improvement_suggestions": detailed_scores["suggestions"]
            }
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))