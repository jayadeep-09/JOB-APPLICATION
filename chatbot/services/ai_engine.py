import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Pre-defined database of skills and roles for the rule-based AI
SKILLS_DB = {
    'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'go', 'rust', 'typescript', 'html', 'css'],
    'frameworks': ['django', 'react', 'angular', 'vue', 'spring', 'flask', 'node.js', 'express', 'laravel'],
    'databases': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'nosql', 'sqlite'],
    'tools_devops': ['git', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'jenkins', 'ci/cd', 'linux', 'bash'],
    'data_ai': ['machine learning', 'deep learning', 'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'nlp', 'data analysis']
}

ROLE_DEFINITIONS = [
    {
        'title': 'Python Developer',
        'keywords': 'python django flask sql git linux backend api',
        'required_skills': ['python', 'django', 'sql', 'git']
    },
    {
        'title': 'Full Stack Developer',
        'keywords': 'javascript react typescript html css node.js python django sql git',
        'required_skills': ['javascript', 'react', 'python', 'sql']
    },
    {
        'title': 'Data Analyst',
        'keywords': 'python pandas numpy sql excel data analysis visualization tableau',
        'required_skills': ['python', 'sql', 'data analysis', 'pandas']
    },
    {
        'title': 'DevOps Engineer',
        'keywords': 'linux bash aws docker kubernetes jenkins git ci/cd python',
        'required_skills': ['linux', 'docker', 'aws', 'ci/cd']
    },
    {
        'title': 'Machine Learning Engineer',
        'keywords': 'python machine learning tensorflow pytorch scikit-learn pandas numpy sql nlp',
        'required_skills': ['python', 'machine learning', 'tensorflow', 'scikit-learn']
    }
]

def extract_entities(text):
    text_lower = text.lower()
    
    found_skills = []
    found_tech = []
    
    for category, skills in SKILLS_DB.items():
        for skill in skills:
            # Word boundary matching
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                found_skills.append(skill.title())
                if category in ['frameworks', 'databases', 'tools_devops', 'data_ai']:
                    found_tech.append(skill.title())
                    
    # Basic heuristic for education (looking for degrees)
    education = "Not explicitly found"
    if re.search(r'\b(bachelor|bs|ba|b\.s|b\.a|master|ms|ma|m\.s|m\.a|phd|degree)\b', text_lower):
        education = "Degree mentioned"

    experience = "Not explicitly found"
    if re.search(r'\b(experience|work history|employment)\b', text_lower):
        experience = "Experience section found"
        
    return {
        'skills': list(set(found_skills)),
        'technologies': list(set(found_tech)),
        'education': education,
        'experience': experience
    }

def suggest_roles(resume_text, extracted_skills):
    if not resume_text.strip():
        return []
        
    # Prepare documents for TF-IDF
    corpus = [resume_text.lower()]
    titles = []
    
    for role in ROLE_DEFINITIONS:
        corpus.append(role['keywords'])
        titles.append(role['title'])
        
    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        tfidf_matrix = vectorizer.fit_transform(corpus)
        # Calculate similarity between resume (index 0) and roles (index 1 to end)
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    except Exception:
        # Fallback if empty vocabulary
        cosine_sim = [0] * len(titles)
        
    suggestions = []
    extracted_lower = [s.lower() for s in extracted_skills]
    
    for idx, score in enumerate(cosine_sim):
        match_percentage = int(score * 100)
        
        # Boost score slightly based on direct required skill overlap
        role_reqs = ROLE_DEFINITIONS[idx]['required_skills']
        overlap = set(extracted_lower).intersection(set(role_reqs))
        if len(role_reqs) > 0:
            boost = (len(overlap) / len(role_reqs)) * 20
            match_percentage = min(99, int(match_percentage + boost))
            
        # Find missing skills
        missing = [skill.title() for skill in role_reqs if skill not in extracted_lower]
        
        if match_percentage > 20: # Only suggest if there's some relevance
            suggestions.append({
                'role_title': titles[idx],
                'match_percentage': match_percentage,
                'missing_skills': missing
            })
            
    # Sort by highest match
    suggestions = sorted(suggestions, key=lambda x: x['match_percentage'], reverse=True)[:3]
    return suggestions

def calculate_ats_score(resume_text, skills):
    score = 40 # Base score for having text
    
    if len(skills) > 5:
        score += 20
    elif len(skills) > 2:
        score += 10
        
    text_lower = resume_text.lower()
    if re.search(r'\b(experience|work history)\b', text_lower):
        score += 15
    if re.search(r'\b(education|degree|university)\b', text_lower):
        score += 15
    if len(resume_text.split()) > 200:
        score += 10
        
    score = min(99, score)
    
    improvements = []
    if len(skills) < 5:
        improvements.append("Add more specific industry keywords and technical skills.")
    if 'experience' not in text_lower:
        improvements.append("Clearly label your Work Experience section.")
    if 'education' not in text_lower:
        improvements.append("Clearly label your Education section.")
        
    if not improvements:
        improvements.append("Resume looks well-formatted. Consider tailoring it further to specific job descriptions.")
        
    return score, " ".join(improvements)

def generate_chat_response(message, resume_analysis=None, suggestions=None):
    msg_lower = message.lower()
    
    if not resume_analysis:
        return "I am your AI Resume Assistant. Please upload your resume (PDF or DOCX) so I can analyze it and help you find the best roles!"
        
    if "score" in msg_lower or "ats" in msg_lower:
        return f"Your estimated ATS score is **{resume_analysis.ats_score}%**. {resume_analysis.improvements}"
        
    if "skill" in msg_lower or "technology" in msg_lower:
        skills_str = ", ".join(resume_analysis.skills) if resume_analysis.skills else "None found"
        return f"I found the following skills in your resume: {skills_str}. If any are missing, try adding them explicitly to your resume."
        
    if "role" in msg_lower or "job" in msg_lower or "suggest" in msg_lower:
        if suggestions and len(suggestions) > 0:
            top = suggestions[0]
            resp = f"Based on your profile, your top match is **{top.role_title}** ({top.match_percentage}% match). "
            if top.missing_skills:
                resp += f"To improve your chances, consider learning: {', '.join(top.missing_skills)}."
            return resp
        return "I couldn't find a strong match for predefined roles yet. Try adding more specific technical keywords to your resume."
        
    if "improve" in msg_lower or "feedback" in msg_lower:
        return f"Here is my feedback on your resume: {resume_analysis.improvements}"
        
    return "I'm here to help with your career! I've analyzed your resume. You can ask me about your ATS score, extracted skills, role suggestions, or how to improve your resume."
