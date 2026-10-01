# Resume Analyzer and Job Matcher

Upload a resume and a job description. The tool shows how well they match, which required skills are
**matched or missing**, and what to improve.

## How it works

1. **Read** the resume (`.pdf` or `.txt`) and the job description.
2. **Extract skills** from both using a skill dictionary with aliases (for example "sklearn" -> Scikit-learn)
   and whole-word matching, so "Java" does not match "JavaScript".
3. **Compare skills:** required skills (from the job) versus skills found on the resume, giving matched, missing and extra.
4. **Compare wording:** TF-IDF vectors and cosine similarity between the two texts.
5. **Score:** `overall = 80% skill coverage + 20% scaled text similarity` (a simple, explainable heuristic).
6. **Suggest:** learning tips for each missing skill plus resume checks (email, projects, links, numbers).

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py --resume data/sample_resume.txt --job data/sample_job.txt
python main.py --resume my_resume.pdf --job job_description.txt
streamlit run app.py          # web interface
python -m pytest              # tests
```

## Example output

```
Overall match : 33.7%
Skill coverage: 38.9%  (7 of 18 required skills)
Matched skills : Git, GitHub, NLP, NumPy, Pandas, Python, SQL
Missing skills : Embeddings, Generative AI, LLM, LangChain, Vector Database, ...
```

## Add your own skills

Open `matcher/skills.py` and add a line to `SKILL_DB`:

```python
"Kubernetes": ["kubernetes", "k8s"],
```

## Limitations and next steps

- Skill matching is dictionary-based, so it only finds skills that are in `SKILL_DB`.
- The score is a guide, not a prediction of any real applicant-tracking system.
- [ ] Use sentence embeddings so "built dashboards" can match "data visualization"
- [ ] Use an LLM to rewrite resume bullet points for a specific job
- [ ] Export the report as a PDF

## Author

Saish Bore, B.Tech Information Technology, Terna Engineering College
