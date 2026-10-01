"""Compare a resume with a job description and produce a report."""
import re
from dataclasses import dataclass, field

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .skills import extract_skills

# How to get each missing skill onto a resume honestly: learn it, then build with it.
LEARNING_TIPS = {
    "LangChain": "Build a small chatbot or document Q&A app with LangChain and put it on GitHub.",
    "RAG": "Build a 'chat with your PDF' app: split text, embed it, retrieve chunks, send them to an LLM.",
    "Vector Database": "Store embeddings in ChromaDB or FAISS in one of your projects.",
    "Embeddings": "Try sentence-transformers to embed sentences and compare them with cosine similarity.",
    "NLP": "Learn tokenization, stop words and TF-IDF, then do a small text-classification project.",
    "Transformers": "Read the 'Attention Is All You Need' summary and try a Hugging Face pipeline.",
    "Generative AI": "Call an LLM API from Python and build one small feature around it.",
    "LLM": "Call an LLM API from Python and build one small feature around it.",
    "Docker": "Containerize one of your projects with a simple Dockerfile.",
    "Machine Learning": "Complete one end-to-end scikit-learn project (data, model, evaluation).",
}


@dataclass
class Report:
    overall_score: float
    skill_score: float
    text_similarity: float
    required_skills: set[str]
    matched: set[str]
    missing: set[str]
    extra: set[str]
    suggestions: list[str] = field(default_factory=list)


def text_similarity(a: str, b: str) -> float:
    """TF-IDF cosine similarity between two texts, from 0 to 1."""
    vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vec.fit_transform([a, b])
    return float(cosine_similarity(matrix[0], matrix[1])[0][0])


def _resume_checks(resume: str) -> list[str]:
    """Simple structure checks that apply to any resume."""
    tips = []
    lower = resume.lower()
    if not re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", resume):
        tips.append("Add a professional email address at the top of the resume.")
    if "project" not in lower:
        tips.append("Add a Projects section; recruiters of freshers look at it first.")
    if "github" not in lower and "linkedin" not in lower:
        tips.append("Add your GitHub and LinkedIn links.")
    if not re.search(r"\d+\s?%|\b\d{2,}\b", resume):
        tips.append("Add numbers to your projects (users, records handled, accuracy, time saved).")
    return tips


def analyze(resume: str, job: str) -> Report:
    required = extract_skills(job)
    have = extract_skills(resume)
    matched = required & have
    missing = required - have
    extra = have - required

    skill_score = len(matched) / len(required) if required else 0.0
    sim = text_similarity(resume, job)
    # Heuristic: skills count for 80%, wording similarity for 20%.
    # TF-IDF similarity is naturally low, so it is scaled: 0.4 already counts as a full score.
    overall = 0.8 * skill_score + 0.2 * min(sim / 0.4, 1.0)

    suggestions = []
    for skill in sorted(missing):
        suggestions.append(f"Missing '{skill}'. " + LEARNING_TIPS.get(
            skill, f"Learn the basics of {skill} and add it to a project before listing it."))
    suggestions += _resume_checks(resume)

    return Report(round(overall * 100, 1), round(skill_score * 100, 1), round(sim, 3),
                  required, matched, missing, extra, suggestions)
