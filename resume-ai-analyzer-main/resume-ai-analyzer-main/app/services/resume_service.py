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
    'AI/Machine Learning Engineer': {
        'technical_skills': [
            'python', 'tensorflow', 'pytorch', 'r', 'deep learning', 'nlp', 'ai', 'ml', 'data science', 'neural networks', 'cloud platforms'
        ],
        'soft_skills': [
            'problem solving', 'analytical thinking', 'team collaboration', 'creativity'
        ],
        'education': [
            'master', 'phd', 'computer science', 'mathematics', 'artificial intelligence'
        ]
    },
    'Data Scientist/Analyst': {
        'technical_skills': [
            'python', 'r', 'sql', 'tableau', 'power bi', 'data wrangling', 'machine learning', 'statistics', 'data visualization'
        ],
        'soft_skills': [
            'data interpretation', 'communication', 'business acumen', 'critical thinking'
        ],
        'education': [
            'master', 'data science', 'statistics', 'analytics', 'mathematics'
        ]
    },
    'Cloud Engineer': {
        'technical_skills': [
            'aws', 'azure', 'google cloud', 'terraform', 'docker', 'kubernetes', 'devops', 'linux', 'cloud architecture', 'networking'
        ],
        'soft_skills': [
            'adaptability', 'teamwork', 'critical thinking', 'problem solving'
        ],
        'education': [
            'certification', 'aws', 'azure', 'gcp', 'bachelor', 'cloud computing'
        ]
    },
    'Cybersecurity Specialist': {
        'technical_skills': [
            'penetration testing', 'firewalls', 'ids/ips', 'ethical hacking', 'encryption', 'risk assessment', 'incident response', 'siem tools'
        ],
        'soft_skills': [
            'attention to detail', 'problem solving', 'risk management', 'critical thinking'
        ],
        'education': [
            'bachelor', 'cybersecurity', 'information security', 'certification', 'computer science'
        ]
    },
    'Full-Stack Developer': {
        'technical_skills': [
            'javascript', 'node.js', 'react', 'angular', 'html', 'css', 'mongodb', 'express.js', 'sql', 'typescript', 'api integration'
        ],
        'soft_skills': [
            'time management', 'collaboration', 'critical thinking', 'problem solving'
        ],
        'education': [
            'bachelor', 'software engineering', 'computer science', 'certification', 'coding bootcamp'
        ]
    },
    'Digital Marketing Specialist': {
        'technical_skills': [
            'seo', 'ppc', 'google ads', 'social media marketing', 'analytics tools', 'content management systems', 'email marketing', 'keyword research', 'marketing automation'
        ],
        'soft_skills': [
            'creativity', 'communication', 'strategy development', 'time management'
        ],
        'education': [
            'bachelor', 'marketing', 'communications', 'digital marketing certification'
        ]
    },
    'UX/UI Designer': {
        'technical_skills': [
            'figma', 'sketch', 'adobe xd', 'html', 'css', 'user testing', 'wireframing', 'prototyping', 'responsive design', 'design systems'
        ],
        'soft_skills': [
            'empathy', 'problem solving', 'creativity', 'collaboration'
        ],
        'education': [
            'bachelor', 'graphic design', 'human-computer interaction', 'certification in ux design'
        ]
    },
    'DevOps Engineer': {
        'technical_skills': [
            'docker', 'kubernetes', 'jenkins', 'ci/cd pipelines', 'ansible', 'terraform', 'git', 'aws', 'linux', 'cloud computing'
        ],
        'soft_skills': [
            'collaboration', 'problem solving', 'time management', 'critical thinking'
        ],
        'education': [
            'bachelor', 'computer science', 'information technology', 'devops certification'
        ]
    },
    'Product Manager': {
        'technical_skills': [
            'jira', 'trello', 'roadmap planning', 'user research', 'agile methodologies', 'business analysis', 'data analysis', 'market research', 'project management tools'
        ],
        'soft_skills': [
            'leadership', 'communication', 'problem solving', 'decision making'
        ],
        'education': [
            'bachelor', 'mba', 'business administration', 'certification in product management'
        ]
    },
    'Blockchain Developer': {
        'technical_skills': [
            'solidity', 'smart contracts', 'ethereum', 'web3', 'cryptography', 'blockchain architecture', 'c++', 'python', 'node.js', 'distributed ledger technology'
        ],
        'soft_skills': [
            'problem solving', 'critical thinking', 'attention to detail', 'collaboration'
        ],
        'education': [
            'bachelor', 'computer science', 'cryptography', 'blockchain certification'
        ]
    },
    'Mobile App Developer': {
        'technical_skills': [
            'swift', 'kotlin', 'react native', 'flutter', 'android studio', 'xcode', 'api integration', 'ui/ux for mobile', 'firebase', 'restful services'
        ],
        'soft_skills': [
            'creativity', 'problem solving', 'time management', 'team collaboration'
        ],
        'education': [
            'bachelor', 'computer science', 'mobile application development', 'certifications in ios/android'
        ]
    },
    'Business Analyst': {
        'technical_skills': [
            'sql', 'excel', 'tableau', 'power bi', 'data analysis', 'requirements gathering', 'project management tools', 'business process modeling'
        ],
        'soft_skills': [
            'communication', 'analytical thinking', 'problem solving', 'stakeholder management'
        ],
        'education': [
            'bachelor', 'business administration', 'economics', 'mba', 'certifications in business analysis'
        ]
    },
    'QA Engineer': {
        'technical_skills': [
            'selenium', 'jira', 'test automation', 'manual testing', 'api testing', 'load testing', 'functional testing', 'sql', 'agile methodologies'
        ],
        'soft_skills': [
            'attention to detail', 'critical thinking', 'problem solving', 'collaboration'
        ],
        'education': [
            'bachelor', 'computer science', 'software engineering', 'certifications in qa testing'
        ]
    },
    'Graphic Designer': {
        'technical_skills': [
            'adobe photoshop', 'adobe illustrator', 'indesign', 'canva', 'graphic design', 'branding', 'typography', 'color theory', 'vector graphics'
        ],
        'soft_skills': [
            'creativity', 'attention to detail', 'communication', 'time management'
        ],
        'education': [
            'bachelor', 'graphic design', 'visual arts', 'certifications in design tools'
        ]
    },
    'Content Writer': {
        'technical_skills': [
            'seo', 'copywriting', 'content strategy', 'editing', 'wordpress', 'social media management', 'analytics tools', 'storytelling'
        ],
        'soft_skills': [
            'creativity', 'communication', 'time management', 'research skills'
        ],
        'education': [
            'bachelor', 'english literature', 'communications', 'journalism', 'certifications in digital marketing'
        ]
    }
        'Content Writer': {
        'technical_skills': [
            'seo', 'copywriting', 'content strategy', 'editing', 'wordpress', 'social media management', 'analytics tools', 'storytelling'
        ],
        'soft_skills': [
            'creativity', 'communication', 'time management', 'research skills'
        ],
        'education': [
            'bachelor', 'english literature', 'communications', 'journalism', 'certifications in digital marketing'
        ]
    },

    'Sales Executive': {
        'technical_skills': [
            'crm systems', 'sales strategies', 'lead generation', 'cold calling', 'sales analytics', 'negotiation', 'pipeline management'
        ],
        'soft_skills': [
            'communication', 'persuasion', 'relationship building', 'time management'
        ],
        'education': [
            'bachelor', 'business administration', 'marketing', 'sales certifications'
        ]
    },
    'Manager': {
        'technical_skills': [
            'project management', 'team leadership', 'budgeting', 'performance reviews', 'crm tools', 'strategic planning', 'resource allocation'
        ],
        'soft_skills': [
            'leadership', 'communication', 'decision making', 'problem solving', 'team collaboration'
        ],
        'education': [
            'bachelor', 'business administration', 'management', 'mba', 'certifications in project management'
        ]
    },
    'Business Development Manager': {
        'technical_skills': [
            'market research', 'crm systems', 'sales forecasting', 'b2b sales', 'negotiation', 'business analysis', 'strategic planning'
        ],
        'soft_skills': [
            'communication', 'problem solving', 'negotiation', 'relationship building', 'collaboration'
        ],
        'education': [
            'bachelor', 'business administration', 'marketing', 'mba', 'certifications in business development'
        ]
    },
    'Marketing Manager': {
        'technical_skills': [
            'digital marketing', 'seo', 'content marketing', 'branding', 'market research', 'email marketing', 'social media strategy', 'analytics tools'
        ],
        'soft_skills': [
            'leadership', 'creativity', 'strategic thinking', 'communication', 'team collaboration'
        ],
        'education': [
            'bachelor', 'marketing', 'business administration', 'mba in marketing'
        ]
    },
    'Director of Operations': {
        'technical_skills': [
            'operations management', 'strategic planning', 'budget management', 'supply chain management', 'kpis', 'risk management', 'crm tools'
        ],
        'soft_skills': [
            'leadership', 'problem solving', 'decision making', 'communication', 'adaptability'
        ],
        'education': [
            'bachelor', 'business administration', 'mba in operations', 'certifications in operations management'
        ]
    },
    'Chief Marketing Officer (CMO)': {
        'technical_skills': [
            'branding', 'market analysis', 'digital marketing', 'crm systems', 'content strategy', 'data-driven marketing', 'growth hacking'
        ],
        'soft_skills': [
            'visionary thinking', 'leadership', 'strategic planning', 'communication', 'team management'
        ],
        'education': [
            'bachelor', 'marketing', 'business administration', 'mba in marketing'
        ]
    },
    'Human Resources Manager': {
        'technical_skills': [
            'employee relations', 'recruitment', 'hr software', 'payroll systems', 'compliance management', 'training and development'
        ],
        'soft_skills': [
            'communication', 'empathy', 'conflict resolution', 'leadership', 'decision making'
        ],
        'education': [
            'bachelor', 'human resources', 'business administration', 'mba in HR', 'certifications in HR management'
        ]
    },
    'Account Manager': {
        'technical_skills': [
            'crm systems', 'relationship management', 'negotiation', 'sales forecasting', 'key account management', 'data analysis'
        ],
        'soft_skills': [
            'communication', 'time management', 'problem solving', 'relationship building'
        ],
        'education': [
            'bachelor', 'marketing', 'business administration', 'sales certifications'
        ]
    },
    'Marketer': {
        'technical_skills': [
            'seo', 'social media marketing', 'email marketing', 'campaign management', 'market research', 'google ads', 'content creation'
        ],
        'soft_skills': [
            'creativity', 'communication', 'analytical thinking', 'time management'
        ],
        'education': [
            'bachelor', 'marketing', 'communications', 'digital marketing certifications'
        ]
    },
    'Customer Success Manager': {
        'technical_skills': [
            'crm tools', 'customer onboarding', 'account management', 'data analysis', 'customer feedback', 'renewal strategies'
        ],
        'soft_skills': [
            'empathy', 'relationship building', 'problem solving', 'communication'
        ],
        'education': [
            'bachelor', 'business administration', 'communications', 'certifications in customer success'
        ]
    },
    'Financial Analyst': {
        'technical_skills': [
            'financial modeling', 'excel', 'sql', 'tableau', 'power bi', 'forecasting', 'budgeting', 'data analysis'
        ],
        'soft_skills': [
            'analytical thinking', 'problem solving', 'time management', 'communication'
        ],
        'education': [
            'bachelor', 'finance', 'economics', 'accounting', 'mba', 'cfa certification'
        ]
    },
    'Director of Operations': {
        'technical_skills': [
            'operations management', 'strategic planning', 'budget management', 'supply chain management', 'kpis', 'risk management', 'crm tools'
        ],
        'soft_skills': [
            'leadership', 'problem solving', 'decision making', 'communication', 'adaptability'
        ],
        'education': [
            'bachelor', 'business administration', 'mba in operations', 'certifications in operations management'
        ]
    },
    'Chief Marketing Officer (CMO)': {
        'technical_skills': [
            'branding', 'market analysis', 'digital marketing', 'crm systems', 'content strategy', 'data-driven marketing', 'growth hacking'
        ],
        'soft_skills': [
            'visionary thinking', 'leadership', 'strategic planning', 'communication', 'team management'
        ],
        'education': [
            'bachelor', 'marketing', 'business administration', 'mba in marketing'
        ]
    },
    'Customer Success Manager': {
        'technical_skills': [
            'crm tools', 'customer onboarding', 'account management', 'data analysis', 'customer feedback', 'renewal strategies'
        ],
        'soft_skills': [
            'empathy', 'relationship building', 'problem solving', 'communication'
        ],
        'education': [
            'bachelor', 'business administration', 'communications', 'certifications in customer success'
        ]
    },
    'Financial Analyst': {
        'technical_skills': [
            'financial modeling', 'excel', 'sql', 'tableau', 'power bi', 'forecasting', 'budgeting', 'data analysis'
        ],
        'soft_skills': [
            'analytical thinking', 'problem solving', 'time management', 'communication'
        ],
        'education': [
            'bachelor', 'finance', 'economics', 'accounting', 'mba', 'cfa certification'
        ]
    },
    'Event Planner': {
        'technical_skills': [
            'event coordination', 'budget management', 'vendor negotiation', 'marketing tools', 'crm systems', 'project management tools'
        ],
        'soft_skills': [
            'time management', 'problem solving', 'creativity', 'communication'
        ],
        'education': [
            'bachelor', 'hospitality management', 'business administration', 'certifications in event management'
        ]
    },
    'Public Relations Specialist': {
        'technical_skills': [
            'media relations', 'press releases', 'crisis management', 'content creation', 'social media management', 'branding'
        ],
        'soft_skills': [
            'communication', 'relationship building', 'strategic thinking', 'problem solving'
        ],
        'education': [
            'bachelor', 'public relations', 'communications', 'journalism'
        ]
    },
    'HR Specialist': {
        'technical_skills': [
            'recruitment', 'onboarding processes', 'employee relations', 'hr software', 'compliance management', 'payroll systems'
        ],
        'soft_skills': [
            'empathy', 'problem solving', 'communication', 'organizational skills'
        ],
        'education': [
            'bachelor', 'human resources', 'business administration', 'mba in HR management'
        ]
    },
    'Data Entry Specialist': {
        'technical_skills': [
            'data entry software', 'microsoft office', 'excel', 'typing skills', 'data verification', 'database management'
        ],
        'soft_skills': [
            'attention to detail', 'time management', 'accuracy', 'problem solving'
        ],
        'education': [
            'high school diploma', 'bachelor', 'certifications in data management'
        ]
    },
    'Operations Manager': {
        'technical_skills': [
            'operations management', 'workflow optimization', 'team coordination', 'project management tools', 'kpi monitoring', 'budgeting'
        ],
        'soft_skills': [
            'leadership', 'problem solving', 'decision making', 'communication'
        ],
        'education': [
            'bachelor', 'business administration', 'mba in operations'
        ]
    },
    'Software Product Manager': {
        'technical_skills': [
            'agile methodologies', 'scrum', 'roadmap planning', 'jira', 'market research', 'data analysis'
        ],
        'soft_skills': [
            'communication', 'leadership', 'decision making', 'problem solving'
        ],
        'education': [
            'bachelor', 'computer science', 'mba', 'certifications in product management'
        ]
    },
    'Creative Director': {
        'technical_skills': [
            'graphic design', 'branding', 'advertising campaigns', 'content strategy', 'art direction', 'digital marketing'
        ],
        'soft_skills': [
            'creativity', 'visionary thinking', 'communication', 'collaboration'
        ],
        'education': [
            'bachelor', 'fine arts', 'graphic design', 'communications'
        ]
    },
    'Supply Chain Manager': {
        'technical_skills': [
            'supply chain management', 'inventory management', 'procurement', 'logistics', 'data analysis', 'erp systems'
        ],
        'soft_skills': [
            'problem solving', 'time management', 'communication', 'decision making'
        ],
        'education': [
            'bachelor', 'supply chain management', 'logistics', 'mba in supply chain'
        ]
    },
    'CEO': {
        'technical_skills': [
            'strategic planning', 'financial management', 'business operations', 'corporate strategy', 'leadership development', 'risk management'
        ],
        'soft_skills': [
            'visionary thinking', 'leadership', 'decision making', 'problem solving', 'communication'
        ],
        'education': [
            'bachelor', 'business administration', 'mba', 'executive leadership programs'
        ]
    },
    'Accountant': {
        'technical_skills': [
            'financial reporting', 'bookkeeping', 'tax preparation', 'excel', 'quickbooks', 'payroll systems'
        ],
        'soft_skills': [
            'attention to detail', 'problem solving', 'time management', 'organizational skills'
        ],
        'education': [
            'bachelor', 'accounting', 'finance', 'certified public accountant (CPA)'
        ]
    }
}
        
    
    # Results dictionary to store findings
    results = {}
    
    # Convert the input text to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    # Check if the job profile is 'Researcher'
    if 'researcher' in text_lower:
        # Extract the keywords and analyze their presence in the text
        profile = 'Researcher'
        keywords = keyword_categories[profile]
        
        for category, category_keywords in keywords.items():
            found = [word for word in category_keywords if word in text_lower]
            missing = [word for word in category_keywords if word not in text_lower]
            
            results[category] = {
                'found': found,
                'missing': missing,
                'score': len(found) / len(category_keywords)
            }
    else:
        # If the job category is not 'Researcher', return 'job category not found'
        results = {"message": "Job category not found"}
    
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
        print(f"Analyzing file: {file_path}")
        #remove
        print(f"Extracted text: {text[:200]}")
        #remove
        text = extract_text(file_path)
        
        sections = {
            'education': bool(re.search(r'education|degree|university|college', text, re.I)),
            'experience': bool(re.search(r'experience|work|employment|job', text, re.I)),
            'skills': bool(re.search(r'skills|technologies|tools|languages', text, re.I))
        }
        print(f"Sections identified: {sections}")
        #remove
        grammar_analysis = analyze_grammar(text)
        print(f"Grammar analysis: {grammar_analysis}")
        #remove
        keyword_analysis = analyze_keywords(text)
        print(f"Keyword analysis: {keyword_analysis}")
        #remove
        scores = calculate_scores(text, sections, grammar_analysis, keyword_analysis)
        print(f"Scores calculated: {scores}")
        #remove
        }
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
