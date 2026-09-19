import streamlit as st
from pypdf import PdfReader
import re

st.set_page_config(
    page_title="AI Resume Screening",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Resume Screening")
st.write("Upload a resume and get a basic ATS-style screening report.")

SKILLS = [
    "python", "java", "c", "c++", "javascript",
    "html", "css", "react", "node.js",
    "sql", "mysql", "mongodb",
    "machine learning", "deep learning",
    "artificial intelligence", "data science",
    "pandas", "numpy", "scikit-learn",
    "tensorflow", "pytorch",
    "git", "github", "docker",
    "aws", "azure",
    "flask", "django", "fastapi",
    "streamlit", "excel", "power bi"
]

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def find_skills(text):
    text = text.lower()
    found_skills = []

    for skill in SKILLS:
        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills


uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

if uploaded_file:

    st.success("Resume uploaded successfully!")

    resume_text = extract_text_from_pdf(uploaded_file)

    if not resume_text.strip():
        st.error("Could not extract text from this PDF.")
        st.stop()

    st.subheader("📄 Resume Text")

    with st.expander("View extracted text"):
        st.write(resume_text)

    found_skills = find_skills(resume_text)

    st.subheader("🛠️ Skills Detected")

    if found_skills:
        st.write(", ".join(found_skills))
    else:
        st.warning("No known skills detected.")

    skill_score = min(len(found_skills) * 3, 40)

    experience_score = 25 if re.search(
        r"\b(experience|internship|intern)\b",
        resume_text,
        re.IGNORECASE
    ) else 0

    education_score = 15 if re.search(
        r"\b(btech|b\.tech|bachelor|degree|12th|10th|engineering)\b",
        resume_text,
        re.IGNORECASE
    ) else 0

    project_score = 10 if re.search(
        r"\b(project|projects)\b",
        resume_text,
        re.IGNORECASE
    ) else 0

    certification_score = 10 if re.search(
        r"\b(certification|certificate|certified)\b",
        resume_text,
        re.IGNORECASE
    ) else 0

    total_score = (
        skill_score
        + experience_score
        + education_score
        + project_score
        + certification_score
    )

    st.divider()

    st.subheader("📊 ATS Screening Score")

    st.metric(
        "Overall Score",
        f"{total_score}/100"
    )

    st.progress(total_score / 100)

    st.subheader("🔍 Score Breakdown")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Skills", f"{skill_score}/40")
    col2.metric("Experience", f"{experience_score}/25")
    col3.metric("Education", f"{education_score}/15")
    col4.metric("Projects", f"{project_score}/10")
    col5.metric("Certifications", f"{certification_score}/10")

    st.divider()

    st.subheader("💡 Screening Result")

    if total_score >= 75:
        st.success("Strong Resume")
    elif total_score >= 50:
        st.warning("Moderate Resume")
    else:
        st.error("Resume Needs Improvement")