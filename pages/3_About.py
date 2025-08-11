import streamlit as st

# Page configuration
st.set_page_config(page_title="About Akanshu Sonkar", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
    .profile-header {
        text-align: center;
        padding: 2rem;
    }
    .profile-name {
        font-size: 3rem;
        font-weight: 700;
    }
    .profile-title {
        font-size: 1.5rem;
        font-style: italic;
        color: #eee;
    }
    .social-links a {
        margin: 10px 10px;
        text-decoration: none;
    }
    .section-header {
        font-size: 2rem;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #ddd;
        padding-bottom: 0.5rem;
    }
    .card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 8px rgba(
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .project-card {
        padding: 1.5rem;
        border: 1px solid #ddd;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .skill-category {
        font-weight: 600;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Profile Header ---
st.markdown("""
<div class="profile-header">
    <div class="profile-name">Akanshu Sonkar</div>
    <div class="profile-title">Data Scientist</div>
    <div class="social-links">
        <a href="https://www.linkedin.com/in/akanshu11121/" target="_blank">
            <img src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" alt="LinkedIn" width="32">
        </a>
        <a href="https://github.com/akanshu11121" target="_blank">
            <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub" width="32">
        </a>
        <a href="https://medium.com/@akanshu11121" target="_blank">
            <img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%2Fid%2FOIP.QscRyx0N6d9Md0NJ9tnG2gHaHa%3Fpid%3DApi&f=1&ipt=1f4bbfae09b91baece6d90aba96a0040fff024abc8c9bd98b214295a5ea7a88b" alt="Medium" width="32">
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Profile Summary ---
st.markdown('<div class="section-header">Profile</div>', unsafe_allow_html=True)
st.markdown("""
<div class="card">
Data Scientist with 4.5+ years of experience in Machine Learning, Statistical Analysis, Time Series Forecasting, and
Predictive Modeling. Skilled in designing, developing, and productionizing scalable ML and Computer Vision models using
MLOps best practices. Proficient in Generative AI, LLMs, LangChain, and deploying context-aware applications with
MLflow, SageMaker, Docker, and Kubernetes. Adept at building CI/CD pipelines, automating workflows, and ensuring robust
model lifecycle management to drive business impact.
</div>
""", unsafe_allow_html=True)

# --- Professional Experience ---
st.markdown('<div class="section-header">Professional Experience</div>', unsafe_allow_html=True)

with st.expander("Data Scientist @ NAVANC (Apr 2024 – Present)"):
    st.markdown("""
    - Leading a cross-functional team of 5, driving delivery, quality, and production deployment of AI/ML solutions.
    - Designed, trained, and deployed scalable ML and Computer Vision models (85–90% CI) using PyTorch, SageMaker, MLflow.
    - Built and deployed an AI Validation Layer on ECS/EKS, reducing report review time by ~89%.
    - Maintained a centralized Elastic Knowledge Base powering analytics across products.
    - Engineered secure data pipelines, APIs, and aggregation algorithms using Docker, ECR, GitHub Actions, and CI/CD.
    """)

with st.expander("ML Engineer @ NAVANC (Feb 2023 – Mar 2024)"):
    st.markdown("""
    - Owned end-to-end lifecycle of nLite, managing code, deployment, APIs, and production operations.
    - Architected company-wide auth system using JWT, Passwordless, OAuth, Okta (zero downtime).
    """)

with st.expander("NLP Engineer @ Gnani.ai (Sep 2022 – Feb 2023)"):
    st.markdown("""
    - Built omni-channel bot, reducing manual calls by 90% and RNR below 35%.
    - Led Project JARVIS, scaling to 1.2 Cr+ daily calls with high reliability.
    - Improved call duration through churn analysis with A/B testing, chi-square, and hypothesis testing.
    """)

with st.expander("Developer @ Wipro (Nov 2020 – Sep 2022)"):
    st.markdown("""
    - Developed, optimized, and maintained codebases using modern software development practices.
    - Improved SQL query performance by 35%, enhancing data processing speed.
    - Automated routine workflows with scripting, reducing manual effort by 40%.
    """)

# --- Projects ---
st.markdown('<div class="section-header">Projects</div>', unsafe_allow_html=True)

st.markdown("""
<div class="project-card">
    <h5>Lead Assessment using Generative AI</h5>
    <p>Automated lead assessment and policy-aware verification using RAG architecture and LangChain, reducing processing time by 80% and human effort by 85%.</p>
    <p><b>Tech Stack:</b> Python | LLMs | RAG | LangChain | NLP | Docker | Github Actions | MLflow | LangSmith</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="project-card">
    <h5>Property Tranche Qualification</h5>
    <p>Computer Vision model to assess property construction stage (0–100%) for loan underwriting. Achieved ~80% accuracy, significantly reducing manual effort and turnaround time in disbursal qualification.</p>
    <p><b>Tech Stack:</b> Python | CNN | YOLOv8 | PyTorch | Roboflow | Flask | SageMaker | ECS/EKS | CloudWatch</p>
</div>
""", unsafe_allow_html=True)


# --- Skills ---
st.markdown('<div class="section-header">Skills</div>', unsafe_allow_html=True)
st.markdown("""
<div class="card">
    <div class="skill-category">Languages & Frameworks:</div>
    Python, PyTorch, Sklearn, Prophet, LangChain, Flask, SpaCy, Streamlit, Postgres, MogoDB, SHAP
    <div class="skill-category">Models:</div>
    Regression, Classification, Clustering, Forecasting, Ensemble, ARIMA, PCA, GMM, GANs, CNN, YOLO, BERT, LLMs
    <div class="skill-category">Tools & Technology:</div>
    Docker, Git, CI/CD, SageMaker, MLflow, REST API, Lambda, EC2, S3, CloudWatch, GitHub Actions, Jenkins, Kubernetes, Tableau, Elasticsearch, Sentry, Drift Detection, Experiment Tracking, Explainable AI
</div>
""", unsafe_allow_html=True)

# --- Education ---
st.markdown('<div class="section-header">Education</div>', unsafe_allow_html=True)
st.markdown("""
<div class="card">
    <b>Master of Science in Computer Science: AI & ML</b> - Woolf University (2022 – 2024)
    <br>
    <b>Bachelor's of Engineering : Computer Science</b> - Global Engineering College (2016 – 2020)
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("© Financial Analyst • Agentic AI integration demo")
