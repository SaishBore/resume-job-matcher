"""Streamlit web app.  Run with:  streamlit run app.py"""
import tempfile
from pathlib import Path

import pandas as pd
import streamlit as st

from matcher import analyze, read_resume

st.set_page_config(page_title="Resume Job Matcher", page_icon="📄")
st.title("📄 Resume Analyzer and Job Matcher")
st.write("Upload your resume, paste a job description, and see how well they match.")

uploaded = st.file_uploader("Resume (PDF or TXT)", type=["pdf", "txt"])
job_text = st.text_area("Job description", height=250)

if st.button("Analyze") and uploaded and job_text.strip():
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded.name).suffix) as tmp:
        tmp.write(uploaded.getvalue())
    resume_text = read_resume(tmp.name)
    report = analyze(resume_text, job_text)

    c1, c2, c3 = st.columns(3)
    c1.metric("Overall match", f"{report.overall_score}%")
    c2.metric("Skill coverage", f"{report.skill_score}%")
    c3.metric("Text similarity", report.text_similarity)
    st.progress(min(report.overall_score / 100, 1.0))

    rows = [(s, "Matched") for s in sorted(report.matched)] + [(s, "Missing") for s in sorted(report.missing)]
    if rows:
        st.subheader("Required skills")
        st.dataframe(pd.DataFrame(rows, columns=["Skill", "Status"]), use_container_width=True)

    st.subheader("Suggestions")
    for tip in report.suggestions:
        st.write("- " + tip)
elif uploaded is None:
    st.info("Upload a resume and paste a job description, then click Analyze.")
