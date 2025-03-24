

import streamlit as st
import pdfplumber
import nltk
import spacy

# Download required NLTK and spaCy models
nltk.download("punkt")
nltk.download("stopwords")
nlp = spacy.load("en_core_web_sm")

# Define job roles and required skills
JOB_ROLES = {
    "Data Scientist": {"Python", "SQL", "Machine Learning", "Deep Learning", "NLP", "Statistics", "Pandas", "Scikit-Learn"},
    "Software Engineer": {"Python", "Java", "C++", "Git", "OOP", "Algorithms"},
    "Cloud Engineer": {"AWS", "Azure", "Docker", "Kubernetes", "Terraform", "Networking"},
    "Cybersecurity Analyst": {"Cybersecurity", "Ethical Hacking", "Network Security", "Penetration Testing"},
    "AI Engineer": {"Python", "TensorFlow", "PyTorch", "Machine Learning", "Deep Learning", "AI"}
}

# Predefined common skills
COMMON_SKILLS = {
    "Python", "Java", "C++", "SQL", "Machine Learning", "Deep Learning", "NLP", "Pandas", "Scikit-Learn",
    "TensorFlow", "PyTorch", "Data Analysis", "Cybersecurity", "Ethical Hacking", "AWS", "Azure", "Docker",
    "Kubernetes", "Flask", "Django", "Linux", "JavaScript", "React", "Node.js", "Computer Vision", "Statistics",
    "Mathematics", "Tableau", "Power BI", "Time Management", "Problem Solving", "Communication", "Teamwork"
}

# Learning recommendations for missing skills
LEARNING_RESOURCES = {
    "Python": "https://www.udemy.com/course/python-for-data-science-and-machine-learning-bootcamp/",
    "SQL": "https://www.coursera.org/learn/sql-for-data-science",
    "Machine Learning": "https://www.coursera.org/learn/machine-learning",
    "Deep Learning": "https://www.udemy.com/course/deep-learning-a-z/",
    "NLP": "https://www.udemy.com/course/nlp-natural-language-processing-with-python/",
    "Statistics": "https://www.khanacademy.org/math/statistics-probability",
    "AWS": "https://www.udemy.com/course/aws-certified-solutions-architect-associate/",
    "Cybersecurity": "https://www.udemy.com/course/the-complete-cyber-security-course-hacker-exposed/",
}

def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file."""
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text if text else "Error extracting text from PDF"

def extract_skills(text):
    """Extract skills from resume using predefined list and NLP."""
    extracted_skills = set()
    text_lower = text.lower()

    # Match predefined skills
    for skill in COMMON_SKILLS:
        if skill.lower() in text_lower:
            extracted_skills.add(skill)

    # Use spaCy for Named Entity Recognition (NER)
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PERSON", "GPE", "FACILITY", "EVENT"]:  # Avoid extracting non-skills
            continue
        if ent.text in COMMON_SKILLS:  # Extract only valid skills
            extracted_skills.add(ent.text)

    return list(extracted_skills)

def extract_summary(text):
    """Extract a concise summary from the resume using NLP."""
    doc = nlp(text)
    for sent in doc.sents:
        if len(sent.text.split()) > 5:  # Ensure it's a meaningful sentence
            return sent.text
    return "Summary not found."

def calculate_match_score(resume_skills, job_role):
    """Calculate match score and identify matched/missing skills."""
    required_skills = JOB_ROLES.get(job_role, set())
    if not required_skills:
        return 0.0, set(), set(), []

    matched_skills = set(resume_skills) & required_skills
    missing_skills = required_skills - matched_skills
    match_percentage = (len(matched_skills) / len(required_skills)) * 100

    # Generate learning recommendations
    learning_links = [f"{skill}: {LEARNING_RESOURCES.get(skill, 'No course available')}" for skill in missing_skills]

    return round(match_percentage, 2), matched_skills, missing_skills, learning_links

# Streamlit UI
st.title("📄 Resume Skill Matcher & Learning Recommendations")
st.markdown("Upload your resume and select a job role to check your match score and get learning recommendations.")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_role = st.selectbox("Select Job Role", list(JOB_ROLES.keys()))

if uploaded_file and job_role:
    with st.spinner("Processing Resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)
        extracted_skills = extract_skills(resume_text)
        summary = extract_summary(resume_text)
        match_score, matched_skills, missing_skills, learning_links = calculate_match_score(extracted_skills, job_role)

        # Display results
        st.subheader("✅ Match Score")
        st.write(f"**{match_score}%**")

        st.subheader("📄 Resume Summary")
        st.write(summary)

        st.subheader("💡 Extracted Skills")
        st.write(", ".join(extracted_skills) if extracted_skills else "None")

        st.subheader("✅ Matched Skills")
        st.write(", ".join(matched_skills) if matched_skills else "None")

        st.subheader("⚠️ Missing Skills")
        st.write(", ".join(missing_skills) if missing_skills else "None")

        st.subheader("📚 Learning Recommendations")
        for link in learning_links:
            st.markdown(f"- {link}")

st.sidebar.markdown("Developed using **Streamlit** 🚀")
