# resume-ai-analyzer
# Resume AI Analyzer API

An advanced AI-powered Resume Analysis API that provides comprehensive feedback and scoring for resumes. Built with FastAPI, this service analyzes resumes for ATS compatibility, grammar, keyword optimization, and provides detailed improvement suggestions.

## 🚀 Features

- **Resume Analysis**
  - Grammar and spelling check
  - ATS (Applicant Tracking System) compatibility
  - Keyword optimization
  - Action verbs usage
  - Page length optimization
  - Section completeness

- **Scoring System**
  - Overall resume score
  - Grammar score
  - Keyword relevance score
  - ATS compatibility score
  - Action verbs score
  - Page length score

- **Improvement Suggestions**
  - Grammar corrections
  - Missing keywords
  - ATS optimization tips
  - Format improvements
  - Content enhancements

## 🛠️ Technology Stack

- Python 3.11+
- FastAPI
- SpaCy (NLP)
- PyPDF2 (PDF Processing)
- Language Tool (Grammar Check)
- Uvicorn (ASGI Server)

## 📋 Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## 🔧 Installation

1. Clone the repository:




## 📚 API Endpoints

### Resume Analysis
- `POST /api/v1/upload` - Basic resume analysis
- `POST /api/v1/analyze-resume` - Detailed resume analysis

### Utility Endpoints
- `GET /api/v1/keywords` - Get analysis keywords
- `GET /api/v1/metrics` - Get scoring metrics
- `POST /api/v1/keyword-check` - Check text for keywords
- `GET /api/v1/suggestions` - Get improvement suggestions
- `GET /api/v1/action-verbs` - Get recommended action verbs
- `GET /api/v1/version` - Get API version

### Health Checks
- `GET /` - Root endpoint
- `GET /health` - Service health check

## 📝 API Usage Examples

### Basic Resume Analysis
