import PyPDF2
import re
import spacy
import language_tool_python
from typing import Dict, List
from fastapi import HTTPException

# Initialize spaCy and LanguageTool
try:
    nlp = spacy.load("en_core_web_sm")
    tool = language_tool_python.LanguageTool('en-US')
except Exception as e:
    print(f"Error initializing NLP tools: {e}")
    raise

def extract_text(file_path: str) -> str:
    """Extract text from PDF file"""
    try:
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting text: {str(e)}")

def analyze_grammar(text: str) -> Dict:
    """Analyze grammar and spelling"""
    try:
        matches = tool.check(text)
        return {
            'errors_count': len(matches),
            'suggestions': [str(match.message) for match in matches[:5]],
            'score': max(0, 1 - (len(matches) / 100))
        }
    except Exception as e:
        return {'errors_count': 0, 'suggestions': [], 'score': 0}

def analyze_keywords(text: str) -> Dict:
    """Analyze presence of important keywords"""
    keyword_categories = {
        'technical_skills': [
            'python', 'java', 'javascript', 'sql', 'aws', 'cloud', 'docker',
            'kubernetes', 'react', 'angular', 'node', 'ml', 'ai'
        ],
        'soft_skills': [
            'leadership', 'communication', 'teamwork', 'problem solving',
            'analytical', 'project management', 'agile', 'scrum'
        ],
        'education': [
            'bachelor', 'master', 'phd', 'degree', 'certification',
            'diploma', 'university', 'college'
        ]
    }
    
    results = {}
    text_lower = text.lower()
    
    for category, keywords in keyword_categories.items():
        found = [word for word in keywords if word in text_lower]
        missing = [word for word in keywords if word not in text_lower]
        results[category] = {
            'found': found,
            'missing': missing,
            'score': len(found) / len(keywords)
        }
    
    return results

def analyze_action_verbs(text: str) -> Dict:
    """Analyze the usage of action verbs"""
    action_verbs = [
        "achieved", "improved", "trained", "managed", "created", "developed",
        "implemented", "increased", "decreased", "negotiated", "launched",
        "coordinated", "generated", "restructured", "supervised"
    ]
    
    found_verbs = [verb for verb in action_verbs if verb in text.lower()]
    score = len(found_verbs) / len(action_verbs)
    
    return {
        "score": score,
        "found_verbs": found_verbs,
        "missing_verbs": [verb for verb in action_verbs if verb not in found_verbs]
    }

def analyze_ats_compatibility(text: str) -> Dict:
    """Analyze ATS compatibility"""
    ats_issues = []
    score = 1.0
    
    if len(text.split()) < 100:
        ats_issues.append("Resume might be too short for ATS")
        score -= 0.2
    
    if text.count('\n\n') > 20:
        ats_issues.append("Too many blank lines might affect ATS parsing")
        score -= 0.1
    
    return {
        "score": max(0, score),
        "issues": ats_issues
    }

def analyze_page_length(file_path: str) -> Dict:
    """Analyze resume length"""
    with open(file_path, 'rb') as file:
        pdf = PyPDF2.PdfReader(file)
        num_pages = len(pdf.pages)
        
        if num_pages == 1:
            return {"score": 0.8, "message": "Resume is concise but might need more detail"}
        elif num_pages == 2:
            return {"score": 1.0, "message": "Optimal resume length"}
        else:
            return {"score": 0.6, "message": "Resume might be too long"}

def calculate_scores(text: str, sections: Dict, grammar_analysis: Dict, keyword_analysis: Dict) -> Dict:
    """Calculate various scores"""
    completeness_score = sum(1 for v in sections.values() if v) / len(sections)
    grammar_score = grammar_analysis.get('score', 0)
    keyword_scores = [data['score'] for data in keyword_analysis.values()]
    keyword_score = sum(keyword_scores) / len(keyword_scores) if keyword_scores else 0
    
    scores = {
        'completeness': completeness_score,
        'grammar': grammar_score,
        'keyword_match': keyword_score,
        'overall': (completeness_score * 0.4 + grammar_score * 0.3 + keyword_score * 0.3)
    }
    
    return {k: round(v * 100, 2) for k, v in scores.items()}

def analyze_resume(file_path: str) -> Dict:
    """Main function to analyze resume"""
    try:
        text = extract_text(file_path)
        
        sections = {
            'education': bool(re.search(r'education|degree|university|college', text, re.I)),
            'experience': bool(re.search(r'experience|work|employment|job', text, re.I)),
            'skills': bool(re.search(r'skills|technologies|tools|languages', text, re.I))
        }
        
        grammar_analysis = analyze_grammar(text)
        keyword_analysis = analyze_keywords(text)
        scores = calculate_scores(text, sections, grammar_analysis, keyword_analysis)
        
        return {
            'scores': scores,
            'sections_found': [k for k, v in sections.items() if v],
            'grammar_analysis': grammar_analysis,
            'keyword_analysis': keyword_analysis,
            'improvement_suggestions': {
                'grammar': grammar_analysis['suggestions'],
                'keywords': {cat: data['missing'] for cat, data in keyword_analysis.items() if data['missing']}
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_detailed_scores(file_path: str, basic_analysis: Dict) -> Dict:
    """Calculate detailed scores"""
    text = extract_text(file_path)
    
    action_verbs_analysis = analyze_action_verbs(text)
    ats_analysis = analyze_ats_compatibility(text)
    page_length_analysis = analyze_page_length(file_path)
    
    grammar_final_score = basic_analysis["grammar_analysis"]["score"] * 100
    action_final_score = action_verbs_analysis["score"] * 100
    ats_final_score = ats_analysis["score"] * 100
    keywords_final_score = basic_analysis["scores"]["keyword_match"]
    page_length_final_score = page_length_analysis["score"] * 100
    
    weights = {
        "grammar": 0.2,
        "action": 0.2,
        "ats": 0.2,
        "keywords": 0.2,
        "page_length": 0.2
    }
    
    total_final_score = (
        grammar_final_score * weights["grammar"] +
        action_final_score * weights["action"] +
        ats_final_score * weights["ats"] +
        keywords_final_score * weights["keywords"] +
        page_length_final_score * weights["page_length"]
    )
    
    return {
        "total_final_score": round(total_final_score, 2),
        "grammar_final_score": round(grammar_final_score, 2),
        "action_final_score": round(action_final_score, 2),
        "ats_final_score": round(ats_final_score, 2),
        "keywords_final_score": round(keywords_final_score, 2),
        "page_length_final_score": round(page_length_final_score, 2),
        "suggestions": {
            "action_verbs": {
                "found": action_verbs_analysis["found_verbs"],
                "missing": action_verbs_analysis["missing_verbs"]
            },
            "ats_issues": ats_analysis["issues"],
            "page_length": page_length_analysis["message"]
        }
    }