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
                'python', 'tensorflow', 'pytorch', 'r', 'deep learning', 'nlp','ai', 'ml', 'data science', 'neural networks', 'cloud platforms'
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
                'python', 'r', 'sql', 'tableau', 'power bi', 'data wrangling',
                'machine learning', 'statistics', 'data visualization'
            ],
            'soft_skills': [
                'data interpretation', 'communication', 'business acumen', 'critical thinking'
            ],
            'education': [
                'master', 'data science', 'statistics', 'analytics', 'mathematics'
            ]
        },
'       Cloud Engineer': {
            'technical_skills': [
                'aws', 'azure', 'google cloud', 'terraform', 'docker', 'kubernetes',
                'devops', 'linux', 'cloud architecture', 'networking'
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
                'penetration testing', 'firewalls', 'ids/ips', 'ethical hacking',
                'encryption', 'risk assessment', 'incident response', 'siem tools'
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
                'javascript', 'node.js', 'react', 'angular', 'html', 'css',
                'mongodb', 'express.js', 'sql', 'typescript', 'api integration'
            ],
            'soft_skills': [
                'time management', 'collaboration', 'critical thinking', 'problem solving'
            ],
            'education': [
                'bachelor', 'software engineering', 'computer science', 'certification', 'coding bootcamp'
           ]
        },
        'Digital Marketing Specialist' or 'Digital Marketing': {
            'technical_skills': [
                'seo', 'ppc', 'google ads', 'social media marketing', 'analytics tools',
        '       content management systems', 'email marketing', 'keyword research', 'marketing automation'
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
                'figma', 'sketch', 'adobe xd', 'html', 'css', 'user testing',
                'wireframing', 'prototyping', 'responsive design', 'design systems'
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
                'docker', 'kubernetes', 'jenkins', 'ci/cd pipelines', 'ansible',
                'terraform', 'git', 'aws', 'linux', 'cloud computing'
            ],
    '       soft_skills': [
                'collaboration', 'problem solving', 'time management', 'critical thinking'
            ],
            'education': [
                'bachelor', 'computer science', 'information technology', 'devops certification'
            ]
        },
        'Product Manager': {
            'technical_skills': [
                'jira', 'trello', 'roadmap planning', 'user research', 'agile methodologies',
                'business analysis', 'data analysis', 'market research', 'project management tools'
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
        'solidity', 'smart contracts', 'ethereum', 'web3', 'cryptography',
        'blockchain architecture', 'c++', 'python', 'node.js', 'distributed ledger technology'
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
                'swift', 'kotlin', 'react native', 'flutter', 'android studio',
                'xcode', 'api integration', 'ui/ux for mobile', 'firebase', 'restful services'
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
                'sql', 'excel', 'tableau', 'power bi', 'data analysis',
                'requirements gathering', 'project management tools', 'business process modeling'
            ],
            'soft_skills': [
                'communication', 'analytical thinking', 'problem solving', 'stakeholder management'
            ],
            'education': [
                'bachelor', 'business administration', 'economics', 'mba', 'certifications in business analysis'
            ]
        },
        'IT Support Specialist': {
            'technical_skills': [
                'hardware troubleshooting', 'networking', 'windows/osx/linux', 'active directory',
                'cloud systems', 'help desk software', 'ticketing systems', 'vpn configuration'
            ],
            'soft_skills': [
                'customer service', 'communication', 'problem solving', 'time management'
            ],
            'education': [
                'bachelor', 'information technology', 'computer science', 'certifications like comptia a+ or ccna'
            ]
        },
        'Network Engineer': {
            'technical_skills': [
                'routing and switching', 'network security', 'cisco technologies',
                'firewalls', 'wireless networks', 'voip', 'vpn', 'network diagnostics'
            ],
            'soft_skills': [
                'critical thinking', 'problem solving', 'team collaboration', 'attention to detail'
            ],
            'education': [
                'bachelor', 'network engineering', 'information systems', 'certifications like ccie, ccna, or ccnp'
            ]
        },
        'QA Engineer': {
            'technical_skills': [
                'selenium', 'jira', 'test automation', 'manual testing', 'api testing',
                'load testing', 'functional testing', 'sql', 'agile methodologies'
            ],
            'soft_skills': [
                'attention to detail', 'critical thinking', 'problem solving', 'collaboration'
            ],
            'education': [
                'bachelor', 'computer science', 'software engineering', 'certifications in qa testing'
            ]
        },
        'Systems Administrator': {
            'technical_skills': [
                'linux', 'windows server', 'active directory', 'virtualization',
                'network management', 'shell scripting', 'dns', 'backup solutions', 'vmware'
            ],
            'soft_skills': [
                'problem solving', 'attention to detail', 'teamwork', 'time management'
            ],
            'education': [
                'bachelor', 'information technology', 'computer science', 'certifications like mcsa, rhce'
            ]
        },
        'Data Engineer': {
            'technical_skills': [
                'python', 'sql', 'hadoop', 'spark', 'etl tools', 'data pipelines',
                'data modeling', 'aws', 'google cloud', 'databases'
            ],
            'soft_skills': [
                'problem solving', 'analytical thinking', 'communication', 'attention to detail'
            ],
            'education': [
                'bachelor', 'data engineering', 'computer science', 'certifications in big data or cloud'
            ]
        },
        'Graphic Designer': {
            'technical_skills': [
                'adobe photoshop', 'adobe illustrator', 'indesign', 'canva', 
                'graphic design', 'branding', 'typography', 'color theory', 'vector graphics'
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
                'seo', 'copywriting', 'content strategy', 'editing', 'wordpress',
                'social media management', 'analytics tools', 'storytelling'
            ],
            'soft_skills': [
                'creativity', 'communication', 'time management', 'research skills'
            ],
            'education': [
                'bachelor', 'english literature', 'communications', 'journalism', 'certifications in digital marketing'
            ]
        },
        'Database Administrator': {
            'technical_skills': [
                'sql', 'mysql', 'oracle', 'mongodb', 'postgresql', 'database design',
                'data backup', 'data migration', 'performance tuning', 'cloud databases'
            ],
            'soft_skills': [
                'problem solving', 'analytical thinking', 'attention to detail', 'communication'
            ],
            'education': [
                'bachelor', 'computer science', 'information systems', 'certifications like oracle dba or microsoft sql server'
            ]
        },  
        'SEO Specialist': {
            'technical_skills': [
                'google analytics', 'seo audits', 'keyword research', 'content optimization',
                'backlink analysis', 'technical seo', 'html', 'wordpress', 'rank tracking'
            ],
            'soft_skills': [
                'critical thinking', 'problem solving', 'analytical mindset', 'communication'
            ],
            'education': [
                'bachelor', 'marketing', 'digital marketing', 'certifications in seo or google analytics'
            ]
        },
        'HR Specialist': {
            'technical_skills': [
                'payroll systems', 'recruitment tools', 'hr management software', 'performance appraisal systems',
                'employment laws', 'talent acquisition', 'onboarding processes', 'training and development'
            ],
            'soft_skills': [
                'communication', 'empathy', 'problem solving', 'conflict resolution'
            ],
            'education': [
                'bachelor', 'human resources', 'business administration', 'mba in hr management'
            ]
        },
        'Financial Analyst': {
            'technical_skills': [
                'excel', 'financial modeling', 'data analysis', 'sql', 'tableau',
                'power bi', 'forecasting', 'budgeting', 'sap', 'erp systems'
            ],
            'soft_skills': [
                'analytical thinking', 'problem solving', 'decision making', 'time management'
            ],
            'education': [
                'bachelor', 'finance', 'economics', 'accounting', 'mba', 'cfa certification'
            ]
        },
        'Mechanical Engineer': {
            'technical_skills': [
                'autocad', 'solidworks', 'ansys', 'matlab', '3d modeling',
                'finite element analysis', 'thermodynamics', 'manufacturing processes'
            ],
            'soft_skills': [
                'problem solving', 'analytical thinking', 'teamwork', 'attention to detail'
            ],
            'education': [
                'bachelor', 'mechanical engineering', 'certifications in cad or fea tools'
            ]
        },
        'Civil Engineer': {
            'technical_skills': [
                'autocad', 'structural design', 'site development', 'construction management',
                'project planning', 'civil engineering software', 'cost estimation', 'building codes'
            ],
            'soft_skills': [
                'problem solving', 'communication', 'attention to detail', 'team collaboration'
            ],
            'education': [
                'bachelor', 'civil engineering', 'construction management', 'certifications in project management'
            ]
        },
        'Marketing Manager': {
            'technical_skills': [
                'digital marketing', 'seo', 'content marketing', 'market research', 'branding',
                'email marketing', 'social media strategy', 'analytics tools', 'campaign management'
            ],
            'soft_skills': [
                'leadership', 'strategic thinking', 'communication', 'creativity'
            ],
            'education': [
                'bachelor', 'marketing', 'business administration', 'mba in marketing'
            ]
        },
'Cloud Architect': {
    'technical_skills': [
        'aws', 'azure', 'google cloud', 'cloud architecture', 'devops', 'kubernetes', 'docker',
        'terraform', 'cloud migration', 'security in cloud environments'
    ],
    'soft_skills': [
        'leadership', 'problem solving', 'strategic thinking', 'team collaboration'
    ],
    'education': [
        'bachelor', 'computer science', 'information technology', 'certifications in cloud platforms like AWS or Azure'
    ]
},
'IT Project Manager': {
    'technical_skills': [
        'project management tools', 'agile methodologies', 'scrum', 'budgeting', 'risk management',
        'time management', 'team coordination', 'stakeholder management'
    ],
    'soft_skills': [
        'leadership', 'problem solving', 'communication', 'decision making'
    ],
    'education': [
        'bachelor', 'information technology', 'project management', 'pmp certification'
    ]
},
'Data Scientist': {
    'technical_skills': [
        'python', 'r', 'machine learning', 'deep learning', 'sql', 'data visualization',
        'statistics', 'data wrangling', 'big data technologies', 'hadoop', 'spark'
    ],
    'soft_skills': [
        'analytical thinking', 'problem solving', 'communication', 'critical thinking'
    ],
    'education': [
        'bachelor', 'computer science', 'data science', 'statistics', 'masters or phd in data science'
    ]
},
'Cybersecurity Analyst': {
    'technical_skills': [
        'network security', 'firewalls', 'encryption', 'incident response', 'penetration testing',
        'vulnerability assessment', 'siem tools', 'aws security', 'compliance frameworks'
    ],
    'soft_skills': [
        'problem solving', 'attention to detail', 'communication', 'risk management'
    ],
    'education': [
        'bachelor', 'information security', 'cybersecurity', 'certifications like compTIA security+, CEH, CISSP'
    ]
},
'Marketing Analyst': {
    'technical_skills': [
        'google analytics', 'seo', 'market research', 'excel', 'power bi', 'customer segmentation',
        'data analysis', 'digital marketing', 'crm systems'
    ],
    'soft_skills': [
        'analytical thinking', 'communication', 'problem solving', 'attention to detail'
    ],
    'education': [
        'bachelor', 'marketing', 'business administration', 'mba in marketing'
    ]
},
'QA Engineer': {
    'technical_skills': [
        'manual testing', 'automated testing', 'selenium', 'pytest', 'test case development',
        'bug tracking', 'performance testing', 'ci/cd', 'software testing life cycle'
    ],
    'soft_skills': [
        'attention to detail', 'problem solving', 'communication', 'analytical thinking'
    ],
    'education': [
        'bachelor', 'computer science', 'information technology', 'certifications in software testing'
    ]
},
'Digital Marketing Specialist': {
    'technical_skills': [
        'seo', 'ppc', 'google ads', 'facebook ads', 'email marketing', 'social media marketing',
        'analytics tools', 'content strategy', 'search engine marketing', 'google analytics'
    ],
    'soft_skills': [
        'creativity', 'problem solving', 'communication', 'time management'
    ],
    'education': [
        'bachelor', 'marketing', 'digital marketing', 'certifications in google ads, facebook marketing'
    ]
},
'Product Manager': {
    'technical_skills': [
        'product roadmaps', 'agile methodologies', 'scrum', 'user stories', 'ux design',
        'market research', 'data analysis', 'roadmap planning', 'stakeholder management'
    ],
    'soft_skills': [
        'leadership', 'problem solving', 'decision making', 'communication'
    ],
    'education': [
        'bachelor', 'business administration', 'engineering', 'mba in product management'
    ]
},
'Sales Manager': {
    'technical_skills': [
        'crm systems', 'sales strategies', 'lead generation', 'sales forecasting', 'market research',
        'email marketing', 'sales analytics', 'negotiation', 'client relationship management'
    ],
    'soft_skills': [
        'leadership', 'communication', 'problem solving', 'team collaboration'
    ],
    'education': [
        'bachelor', 'business administration', 'marketing', 'mba in sales management'
    ]
},
'Network Engineer': {
    'technical_skills': [
        'network troubleshooting', 'routing and switching', 'tcp/ip', 'vpn', 'firewall configuration',
        'wi-fi', 'lan/wlan', 'network monitoring', 'ipv4/ipv6', 'network security'
    ],
    'soft_skills': [
        'problem solving', 'attention to detail', 'communication', 'time management'
    ],
    'education': [
        'bachelor', 'computer science', 'network engineering', 'ccna, ccnp certifications'
    ]
},
'Cloud Security Engineer': {
    'technical_skills': [
        'aws security', 'azure security', 'cloud architecture', 'vpn', 'firewall management', 'encryption',
        'incident response', 'identity and access management', 'cloud vulnerability assessments'
    ],
    'soft_skills': [
        'problem solving', 'attention to detail', 'communication', 'risk management'
    ],
    'education': [
        'bachelor', 'cybersecurity', 'computer science', 'cloud computing', 'certifications in cloud security'
    ]
},
'Video Editor': {
    'technical_skills': [
        'adobe premiere pro', 'final cut pro', 'video editing software', 'motion graphics', 'color grading',
        'audio editing', 'storyboarding', 'post-production'
    ],
    'soft_skills': [
        'creativity', 'attention to detail', 'time management', 'communication'
    ],
    'education': [
        'bachelor', 'film production', 'media studies', 'certifications in video editing software'
    ]
},
'Artificial Intelligence Engineer': {
    'technical_skills': [
        'python', 'tensorflow', 'keras', 'pytorch', 'machine learning', 'deep learning', 'computer vision',
        'natural language processing', 'reinforcement learning', 'neural networks'
    ],
    'soft_skills': [
        'problem solving', 'analytical thinking', 'communication', 'team collaboration'
    ],
    'education': [
        'bachelor', 'computer science', 'artificial intelligence', 'masters or phd in ai or machine learning'
    ]
},
'Customer Support Representative': {
    'technical_skills': [
        'crm software', 'ticketing systems', 'customer service tools', 'helpdesk systems', 'chatbots',
        'email support', 'phone support', 'issue tracking'
    ],
    'soft_skills': [
        'communication', 'problem solving', 'empathy', 'patience'
    ],
    'education': [
        'high school diploma', 'bachelor', 'customer service certifications'
    ]
},
'Business Development Manager': {
    'technical_skills': [
        'market research', 'sales strategies', 'crm systems', 'lead generation', 'negotiation', 
        'b2b sales', 'relationship building', 'business analysis', 'sales forecasting', 'strategic planning'
    ],
    'soft_skills': [
        'communication', 'problem solving', 'negotiation', 'relationship building', 'collaboration'
    ],
    'education': [
        'bachelor', 'business administration', 'marketing', 'mba', 'certifications in business development'
    ]
},
'CEO': {
    'technical_skills': [
        'strategic planning', 'financial management', 'corporate governance', 'leadership', 'business operations', 
        'stakeholder management', 'decision making', 'corporate strategy', 'public relations'
    ],
    'soft_skills': [
        'leadership', 'problem solving', 'communication', 'visionary thinking', 'adaptability'
    ],
    'education': [
        'bachelor', 'business administration', 'economics', 'mba', 'executive leadership programs'
    ]
},
'Vice President': {
    'technical_skills': [
        'strategic leadership', 'business development', 'financial planning', 'corporate governance', 
        'project management', 'operations management', 'risk management', 'stakeholder communication'
    ],
    'soft_skills': [
        'leadership', 'negotiation', 'decision making', 'team collaboration', 'communication'
    ],
    'education': [
        'bachelor', 'business administration', 'finance', 'mba', 'leadership programs'
    ]
},
'Team Leader': {
    'technical_skills': [
        'project management', 'agile methodologies', 'team collaboration', 'conflict resolution', 
        'performance tracking', 'task delegation', 'mentorship', 'process improvement'
    ],
    'soft_skills': [
        'leadership', 'communication', 'problem solving', 'team motivation', 'time management'
    ],
    'education': [
        'bachelor', 'business administration', 'management', 'certifications in leadership or team management'
    ]
},
'Manager': {
    'technical_skills': [
        'project management', 'budgeting', 'financial planning', 'team leadership', 'performance reviews',
        'strategic planning', 'resource allocation', 'operations management', 'crm tools', 'marketing strategies'
    ],
    'soft_skills': [
        'communication', 'decision making', 'problem solving', 'leadership', 'team collaboration'
    ],
    'education': [
        'bachelor', 'business administration', 'management', 'mba', 'certifications in project management'
    ]
},
'Sales Consultant': {
    'technical_skills': [
        'sales techniques', 'crm systems', 'sales strategies', 'market research', 'product knowledge', 
        'customer engagement', 'lead generation', 'b2b sales', 'negotiation skills'
    ],
    'soft_skills': [
        'communication', 'persuasion', 'problem solving', 'customer service', 'relationship building'
    ],
    'education': [
        'bachelor', 'business administration', 'marketing', 'sales management', 'certifications in sales or marketing'
    ]
},
'Human Resources Manager': {
    'technical_skills': [
        'recruitment', 'employee relations', 'hr management software', 'payroll systems', 'labor law',
        'training and development', 'performance management', 'compliance management'
    ],
    'soft_skills': [
        'communication', 'problem solving', 'leadership', 'conflict resolution', 'empathy'
    ],
    'education': [
        'bachelor', 'human resources', 'business administration', 'mba in human resources', 'certifications in HR management'
    ]
},
'Digital Transformation Manager': {
    'technical_skills': [
        'change management', 'cloud computing', 'data analytics', 'digital strategy', 'ai implementation',
        'business process reengineering', 'automation', 'project management'
    ],
    'soft_skills': [
        'leadership', 'communication', 'adaptability', 'problem solving', 'collaboration'
    ],
    'education': [
        'bachelor', 'business administration', 'digital transformation', 'mba in digital innovation'
    ]
},
'Scrum Master': {
    'technical_skills': [
        'agile methodologies', 'scrum framework', 'project management', 'team collaboration', 'product backlog management',
        'sprint planning', 'jira', 'kanban', 'scrum ceremonies'
    ],
    'soft_skills': [
        'leadership', 'communication', 'problem solving', 'conflict resolution', 'collaboration'
    ],
    'education': [
        'bachelor', 'project management', 'computer science', 'certifications in scrum (CSM)'
    ]
},
'Frontend Developer' or 'WordPress Developer': {
    'technical_skills': [
        'html', 'css', 'javascript', 'react', 'angular', 'vue.js', 'jquery', 'sass', 'responsive design', 
        'cross-browser compatibility', 'web performance optimization', 'frontend frameworks'
    ],
    'soft_skills': [
        'problem solving', 'creativity', 'attention to detail', 'team collaboration', 'communication'
    ],
    'education': [
        'bachelor', 'computer science', 'software engineering', 'web development', 'certifications in frontend development'
    ]
},
'Researcher' or 'General Researcher' or 'Market Researcher' or 'Scientific Researcher': {
    'technical_skills': [
        'data analysis', 'research methods', 'statistical analysis', 'qualitative research', 'quantitative research', 
        'literature review', 'hypothesis testing', 'data visualization', 'survey design', 'research software tools (e.g., SPSS, R)'
    ],
    'soft_skills': [
        'critical thinking', 'problem solving', 'attention to detail', 'communication', 'organization'
    ],
    'education': [
        'bachelor', 'master', 'phd', 'research methodology', 'specialized certifications in research fields'
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
