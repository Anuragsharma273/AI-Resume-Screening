import streamlit as st
from pypdf import PdfReader
import re
import pandas as pd

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Resume Screening",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# BLACK THEME
# =========================================================

st.markdown("""
<style>

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: #000000 !important;
    color: #ffffff !important;
}

[data-testid="stHeader"] {
    background: #000000 !important;
}

section[data-testid="stSidebar"] {
    background: #000000 !important;
    border-right: 1px solid #333333;
}

section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

.main-title {
    font-size: 40px;
    font-weight: 800;
    color: #ffffff !important;
}

.subtitle {
    font-size: 17px;
    color: #cccccc !important;
    margin-bottom: 25px;
}

.section-title {
    font-size: 25px;
    font-weight: 700;
    color: #ffffff !important;
    margin-top: 20px;
    margin-bottom: 15px;
}

h1, h2, h3, h4, h5, h6,
p, label, span {
    color: #ffffff !important;
}

.skill-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 8px;
    margin-bottom: 15px;
}

.skill {
    display: inline-block;
    background: #222222 !important;
    color: #ffffff !important;
    padding: 7px 12px;
    border-radius: 20px;
    border: 1px solid #555555;
    font-size: 13px;
    font-weight: 600;
}

.matched {
    background: #123d2a !important;
    border-color: #2e8b57 !important;
}

.missing {
    background: #421818 !important;
    border-color: #a94442 !important;
}

.candidate-card {
    background: #111111 !important;
    padding: 20px;
    border: 1px solid #444444;
    border-radius: 15px;
    margin-top: 15px;
    margin-bottom: 10px;
}

.profile-name {
    font-size: 24px;
    font-weight: 700;
    color: #ffffff !important;
}

.profile-contact {
    font-size: 14px;
    color: #cccccc !important;
}

.status-good,
.status-medium,
.status-low {
    color: #ffffff !important;
    font-weight: 700;
}

textarea,
input {
    background: #111111 !important;
    color: #ffffff !important;
    border: 1px solid #555555 !important;
}

textarea::placeholder,
input::placeholder {
    color: #aaaaaa !important;
}

[data-testid="stFileUploader"] {
    background: #111111 !important;
    border: 1px solid #555555 !important;
    border-radius: 12px;
}

[data-testid="stFileUploader"] * {
    color: #ffffff !important;
}

.stButton button {
    background: #111111 !important;
    color: #ffffff !important;
    border: 1px solid #666666 !important;
}

.stButton button:hover {
    background: #222222 !important;
    border-color: #ffffff !important;
}

.stAlert {
    background: #111111 !important;
    color: #ffffff !important;
    border: 1px solid #555555 !important;
}

[data-testid="stMetric"] {
    background: #111111 !important;
    border: 1px solid #444444 !important;
    border-radius: 12px;
    padding: 12px;
}

[data-testid="stMetricLabel"] {
    color: #cccccc !important;
}

[data-testid="stMetricValue"] {
    color: #ffffff !important;
}

hr {
    border-color: #444444 !important;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SKILLS DATABASE
# =========================================================

SKILLS = [
    "python",
    "java",
    "c++",
    "c",
    "javascript",
    "typescript",
    "html",
    "css",
    "react",
    "node.js",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "git",
    "github",
    "docker",
    "aws",
    "azure",
    "flask",
    "django",
    "fastapi",
    "streamlit",
    "excel",
    "power bi",
    "tableau",
    "figma",
    "linux",
    "rest api",
    "data structures",
    "algorithms"
]


# =========================================================
# TEXT EXTRACTION
# =========================================================

def extract_text(pdf_file):

    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# =========================================================
# SKILL DETECTION
# =========================================================

def find_skills(text):

    text_lower = text.lower()

    found = []

    for skill in SKILLS:

        pattern = (
            r"(?<![a-zA-Z0-9])"
            + re.escape(skill.lower())
            + r"(?![a-zA-Z0-9])"
        )

        if re.search(pattern, text_lower):

            found.append(skill)

    return found


# =========================================================
# NAME
# =========================================================

def extract_name(text):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    for line in lines[:10]:

        if (
            len(line.split()) <= 5
            and "@" not in line
            and not re.search(r"\d{5,}", line)
            and len(line) > 2
        ):

            return line

    return "Candidate"


# =========================================================
# EMAIL
# =========================================================

def extract_email(text):

    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    if match:
        return match.group()

    return "Not found"


# =========================================================
# PHONE
# =========================================================

def extract_phone(text):

    match = re.search(
        r"(?:\+91[\s-]?)?[6-9]\d{9}",
        text
    )

    if match:
        return match.group()

    return "Not found"


# =========================================================
# EXPERIENCE
# =========================================================

def extract_experience(text):

    patterns = [
        r"\b\d+\+?\s*(?:years?|yrs?)\s*(?:of)?\s*experience\b",
        r"\b\d+\s*(?:months?|mos?)\s*(?:of)?\s*experience\b",
        r"\binternship\b",
        r"\bintern\b",
        r"\bexperience\b",
        r"\bworked\b",
        r"\bemployment\b"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group()

    return "Not detected"


# =========================================================
# EDUCATION
# =========================================================

def extract_education(text):

    patterns = [
        r"\bB\.?Tech\b",
        r"\bB\.?E\.?\b",
        r"\bBachelor(?:'s)?\b",
        r"\bBCA\b",
        r"\bMCA\b",
        r"\bM\.?Tech\b",
        r"\bMBA\b",
        r"\bComputer Science\b",
        r"\bEngineering\b",
        r"\b12th\b",
        r"\b10th\b",
        r"\bDegree\b"
    ]

    found = []

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE
        )

        for item in matches:

            if item.lower() not in [
                x.lower() for x in found
            ]:

                found.append(item)

    if found:
        return ", ".join(found[:5])

    return "Not detected"


# =========================================================
# PROJECTS
# =========================================================

def extract_projects(text):

    if re.search(
        r"\bprojects?\b",
        text,
        re.IGNORECASE
    ):

        return "Projects detected"

    return "Not detected"


# =========================================================
# CERTIFICATIONS
# =========================================================

def extract_certifications(text):

    if re.search(
        r"\b(certifications?|certificate|certified|courses?)\b",
        text,
        re.IGNORECASE
    ):

        return "Certification/Course detected"

    return "Not detected"


# =========================================================
# ATS SCORE
# =========================================================

def calculate_ats(text, skills):

    skill_score = min(
        len(skills) * 3,
        40
    )

    experience_score = (
        25
        if re.search(
            r"\b(experience|internship|intern|worked|employment)\b",
            text,
            re.IGNORECASE
        )
        else 0
    )

    education_score = (
        15
        if re.search(
            r"\b(btech|b\.tech|bachelor|degree|engineering|computer science|12th|10th)\b",
            text,
            re.IGNORECASE
        )
        else 0
    )

    project_score = (
        10
        if re.search(
            r"\bprojects?\b",
            text,
            re.IGNORECASE
        )
        else 0
    )

    certification_score = (
        10
        if re.search(
            r"\b(certifications?|certificate|certified|course)\b",
            text,
            re.IGNORECASE
        )
        else 0
    )

    return {
        "total": (
            skill_score
            + experience_score
            + education_score
            + project_score
            + certification_score
        ),
        "skills": skill_score,
        "experience": experience_score,
        "education": education_score,
        "projects": project_score,
        "certifications": certification_score
    }


# =========================================================
# JOB MATCHING
# =========================================================

def job_match(resume_skills, jd_skills):

    if not jd_skills:
        return 0, [], []

    matched = [
        skill
        for skill in jd_skills
        if skill in resume_skills
    ]

    missing = [
        skill
        for skill in jd_skills
        if skill not in resume_skills
    ]

    percentage = round(
        len(matched) / len(jd_skills) * 100
    )

    return percentage, matched, missing


# =========================================================
# MATCH STATUS
# =========================================================

def get_match_status(score):

    if score >= 75:
        return "Strong Match", "status-good"

    if score >= 50:
        return "Partial Match", "status-medium"

    return "Low Match", "status-low"


# =========================================================
# PROCESS RESUMES
# =========================================================

def process_resumes(uploaded_files):

    results = []

    for file in uploaded_files:

        text = extract_text(file)

        if not text.strip():
            continue

        skills = find_skills(text)

        results.append({
            "file": file.name,
            "name": extract_name(text),
            "email": extract_email(text),
            "phone": extract_phone(text),
            "skills": skills,
            "experience": extract_experience(text),
            "education": extract_education(text),
            "projects": extract_projects(text),
            "certifications": extract_certifications(text),
            "ats": calculate_ats(text, skills),
            "text": text
        })

    return results


# =========================================================
# SKILL DISPLAY
# =========================================================

def render_skills(skills, css_class=""):

    if not skills:

        st.write("None detected.")

        return

    html = '<div class="skill-container">'

    for skill in skills:

        html += (
            f'<span class="skill {css_class}">'
            f'{skill}'
            f'</span>'
        )

    html += "</div>"

    st.markdown(
        html,
        unsafe_allow_html=True
    )


# =========================================================
# SESSION STATE
# =========================================================

if "results" not in st.session_state:

    st.session_state.results = []

if "job_description" not in st.session_state:

    st.session_state.job_description = ""


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        "## 🤖 AI Resume Screening"
    )

    st.caption(
        "Professional ATS Dashboard"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "📄 Resume Screening",
            "🎯 Job Matching",
            "📋 Candidate Comparison"
        ]
    )

    st.divider()

    st.markdown(
        "### About"
    )

    st.caption(
        "Resume analysis and job requirement "
        "matching prototype."
    )


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">'
    'AI Resume Screening'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Intelligent ATS-style resume analysis and candidate matching'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="section-title">'
        '🎯 Job Requirement'
        '</div>',
        unsafe_allow_html=True
    )

    job_description = st.text_area(
        "Describe the type of candidate required",
        value=st.session_state.job_description,
        height=150,
        placeholder=(
            "Example: Python developer with SQL, "
            "Pandas, Machine Learning, Git and REST API skills."
        )
    )

    st.session_state.job_description = job_description

    st.markdown(
        '<div class="section-title">'
        '📄 Upload Resumes'
        '</div>',
        unsafe_allow_html=True
    )

    uploaded_files = st.file_uploader(
        "Upload one or multiple PDF resumes",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:

        st.session_state.results = process_resumes(
            uploaded_files
        )

        st.success(
            f"{len(st.session_state.results)} resume(s) processed successfully."
        )

    results = st.session_state.results

    if results:

        jd_skills = find_skills(
            job_description
        )

        if jd_skills:

            st.markdown(
                '<div class="section-title">'
                '🔎 Required Skills Detected'
                '</div>',
                unsafe_allow_html=True
            )

            render_skills(jd_skills)

        # =================================================
        # CALCULATE MATCH
        # =================================================

        candidate_data = []

        for r in results:

            match_percentage, matched, missing = job_match(
                r["skills"],
                jd_skills
            )

            candidate_data.append({
                "data": r,
                "match": match_percentage,
                "matched": matched,
                "missing": missing
            })

        if jd_skills:

            candidate_data.sort(
                key=lambda x: x["match"],
                reverse=True
            )

        # =================================================
        # OVERVIEW
        # =================================================

        st.markdown(
            '<div class="section-title">'
            '📊 Screening Overview'
            '</div>',
            unsafe_allow_html=True
        )

        total_candidates = len(
            candidate_data
        )

        average_ats = round(
            sum(
                x["data"]["ats"]["total"]
                for x in candidate_data
            ) / total_candidates
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "👥 Candidates",
            total_candidates
        )

        c2.metric(
            "📊 Average ATS",
            f"{average_ats}/100"
        )

        c3.metric(
            "🎯 Job Skills",
            len(jd_skills)
        )

        c4.metric(
            "📄 Resumes",
            len(results)
        )

        st.divider()

        # =================================================
        # CANDIDATES
        # =================================================

        st.markdown(
            '<div class="section-title">'
            '👥 Candidate Profiles'
            '</div>',
            unsafe_allow_html=True
        )

        if jd_skills:

            st.caption(
                "Candidates are displayed by detected job-skill "
                "match percentage. This is an informational "
                "comparison of resume skills against the "
                "requirements entered."
            )

        for index, item in enumerate(
            candidate_data,
            start=1
        ):

            r = item["data"]

            match_percentage = item["match"]

            matched = item["matched"]

            missing = item["missing"]

            status, status_class = get_match_status(
                match_percentage
            )

            # Candidate card

            st.markdown(
                f"""
                <div class="candidate-card">

                    <div class="profile-name">
                        #{index} 👤 {r["name"]}
                    </div>

                    <div class="profile-contact">
                        📧 {r["email"]}
                        &nbsp;&nbsp;&nbsp;
                        📱 {r["phone"]}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            # Scores

            c1, c2, c3, c4 = st.columns(4)

            c1.metric(
                "🎯 Job Match",
                f"{match_percentage}%"
            )

            c2.metric(
                "📊 ATS Score",
                f'{r["ats"]["total"]}/100'
            )

            c3.metric(
                "🛠️ Skills",
                len(r["skills"])
            )

            with c4:

                if jd_skills:

                    st.markdown(
                        f"""
                        <div class="{status_class}">
                            {status}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    st.write(
                        "Add Job Description"
                    )

            if jd_skills:

                st.progress(
                    match_percentage / 100
                )

            # Information

            c1, c2, c3 = st.columns(3)

            with c1:

                st.markdown(
                    "### 🛠️ Skills"
                )

                render_skills(
                    r["skills"]
                )

            with c2:

                st.markdown(
                    "### 💼 Experience"
                )

                st.write(
                    r["experience"]
                )

                st.markdown(
                    "### 🎓 Education"
                )

                st.write(
                    r["education"]
                )

            with c3:

                st.markdown(
                    "### 🚀 Projects"
                )

                st.write(
                    r["projects"]
                )

                st.markdown(
                    "### 🏆 Certifications"
                )

                st.write(
                    r["certifications"]
                )

            # Job match details

            if jd_skills:

                d1, d2 = st.columns(2)

                with d1:

                    st.markdown(
                        "### ✅ Matched Skills"
                    )

                    render_skills(
                        matched,
                        "matched"
                    )

                with d2:

                    st.markdown(
                        "### ❌ Missing Skills"
                    )

                    render_skills(
                        missing,
                        "missing"
                    )

            # ATS breakdown

            with st.expander(
                "📊 View ATS Score Breakdown"
            ):

                b1, b2, b3, b4, b5 = st.columns(5)

                b1.metric(
                    "Skills",
                    f'{r["ats"]["skills"]}/40'
                )

                b2.metric(
                    "Experience",
                    f'{r["ats"]["experience"]}/25'
                )

                b3.metric(
                    "Education",
                    f'{r["ats"]["education"]}/15'
                )

                b4.metric(
                    "Projects",
                    f'{r["ats"]["projects"]}/10'
                )

                b5.metric(
                    "Certifications",
                    f'{r["ats"]["certifications"]}/10'
                )

            with st.expander(
                "📄 View Resume Text"
            ):

                st.text(
                    r["text"]
                )

            st.divider()

    else:

        st.info(
            "Enter the job requirements above and upload "
            "one or more PDF resumes to start screening."
        )


# =========================================================
# RESUME SCREENING PAGE
# =========================================================

elif page == "📄 Resume Screening":

    st.markdown(
        '<div class="section-title">'
        '📄 Resume Screening'
        '</div>',
        unsafe_allow_html=True
    )

    uploaded_files = st.file_uploader(
        "Upload one or multiple PDF resumes",
        type=["pdf"],
        accept_multiple_files=True,
        key="screening_uploader"
    )

    if uploaded_files:

        st.session_state.results = process_resumes(
            uploaded_files
        )

        st.success(
            f"{len(st.session_state.results)} resume(s) processed successfully."
        )

        st.info(
            "Go to Dashboard to view candidate profiles "
            "and job matching."
        )


# =========================================================
# JOB MATCHING PAGE
# =========================================================

elif page == "🎯 Job Matching":

    st.markdown(
        '<div class="section-title">'
        '🎯 Job Description Matching'
        '</div>',
        unsafe_allow_html=True
    )

    jd = st.text_area(
        "Describe the candidate requirements",
        height=200,
        value=st.session_state.job_description,
        placeholder=(
            "Example: Python developer with SQL, "
            "Pandas, Git, Machine Learning and REST API."
        )
    )

    st.session_state.job_description = jd

    results = st.session_state.results

    if not results:

        st.warning(
            "Please upload resumes first."
        )

    elif not jd:

        st.info(
            "Enter the job requirements above."
        )

    else:

        jd_skills = find_skills(jd)

        st.markdown(
            "### 🔎 Detected Job Skills"
        )

        render_skills(
            jd_skills
        )

        comparison = []

        for r in results:

            percentage, matched, missing = job_match(
                r["skills"],
                jd_skills
            )

            comparison.append({
                "Candidate": r["name"],
                "Job Match": percentage,
                "ATS Score": r["ats"]["total"],
                "Matched Skills": ", ".join(matched),
                "Missing Skills": ", ".join(missing)
            })

        comparison_df = pd.DataFrame(
            comparison
        )

        if not comparison_df.empty:

            comparison_df = comparison_df.sort_values(
                "Job Match",
                ascending=False
            )

        st.divider()

        st.markdown(
            "### 📋 Match Comparison"
        )

        st.dataframe(
            comparison_df,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# CANDIDATE COMPARISON
# =========================================================

else:

    st.markdown(
        '<div class="section-title">'
        '📋 Candidate Comparison'
        '</div>',
        unsafe_allow_html=True
    )

    results = st.session_state.results

    if results:

        table = []

        for r in results:

            table.append({
                "Candidate": r["name"],
                "ATS Score": r["ats"]["total"],
                "Skills": len(r["skills"]),
                "Experience": r["experience"],
                "Education": r["education"],
                "Projects": r["projects"],
                "Certifications": r["certifications"]
            })

        df = pd.DataFrame(
            table
        )

        search = st.text_input(
            "🔎 Search candidate"
        )

        if search:

            df = df[
                df["Candidate"].str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        csv = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "📥 Download Screening Report",
            data=csv,
            file_name="resume_screening_report.csv",
            mime="text/csv"
        )

    else:

        st.info(
            "Upload resumes first."
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🤖 AI Resume Screening • "
    "Built with Python, Streamlit & PDF Analysis"
)