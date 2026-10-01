"""Skill dictionary and skill extraction.

Each skill has a canonical name and a list of aliases. To support a new skill,
just add a line to SKILL_DB.
"""
import re

SKILL_DB: dict[str, list[str]] = {
    # Programming
    "Python": ["python"], "Java": ["java"], "C++": ["c++"], "C#": ["c#"],
    "JavaScript": ["javascript", "js"], "TypeScript": ["typescript"], "R": ["r programming"],
    "HTML": ["html", "html5"], "CSS": ["css", "css3"],
    # Data
    "SQL": ["sql"], "MySQL": ["mysql"], "PostgreSQL": ["postgresql", "postgres"],
    "MongoDB": ["mongodb"], "NumPy": ["numpy"], "Pandas": ["pandas"],
    "Matplotlib": ["matplotlib"], "Seaborn": ["seaborn"], "Excel": ["excel", "microsoft excel"],
    "Power BI": ["power bi", "powerbi"], "Tableau": ["tableau"],
    "Data Analysis": ["data analysis", "data analytics", "data analyst"],
    "Data Visualization": ["data visualization", "data visualisation"],
    "Data Management": ["data management"], "ETL": ["etl"],
    "Statistics": ["statistics", "statistical analysis"],
    # AI / ML / NLP
    "Machine Learning": ["machine learning", "ml"], "Deep Learning": ["deep learning"],
    "NLP": ["nlp", "natural language processing"], "Scikit-learn": ["scikit-learn", "sklearn"],
    "TensorFlow": ["tensorflow"], "PyTorch": ["pytorch"], "Keras": ["keras"],
    "Generative AI": ["generative ai", "gen ai", "genai"],
    "LLM": ["llm", "llms", "large language model", "large language models"],
    "Transformers": ["transformer", "transformers"],
    "Tokenization": ["tokenization", "tokenisation"],
    "Embeddings": ["embedding", "embeddings"],
    "LangChain": ["langchain"], "LlamaIndex": ["llamaindex", "llama index"],
    "Vector Database": ["vector database", "vector databases", "vector db", "chromadb", "faiss", "pinecone"],
    "RAG": ["rag", "retrieval augmented generation", "retrieval-augmented generation"],
    "Prompt Engineering": ["prompt engineering"], "Hugging Face": ["hugging face", "huggingface"],
    "Chatbot": ["chatbot", "chatbots"], "Fine-tuning": ["fine-tuning", "fine tuning", "fine-tuned"],
    "OpenCV": ["opencv"],
    # Tools / engineering
    "Git": ["git"], "GitHub": ["github"], "Docker": ["docker"], "Linux": ["linux"],
    "REST API": ["rest api", "rest apis", "restful"], "Flask": ["flask"], "Django": ["django"],
    "FastAPI": ["fastapi"], "Streamlit": ["streamlit"], "Jupyter": ["jupyter"],
    "Kaggle": ["kaggle"], "Hackathon": ["hackathon", "hackathons"],
    # Cloud
    "AWS": ["aws", "amazon web services"], "Azure": ["azure"], "GCP": ["gcp", "google cloud"],
}


def _pattern(alias: str) -> re.Pattern:
    # Whole-word match that also handles aliases like "c++", "c#" and "scikit-learn".
    return re.compile(r"(?<![A-Za-z0-9+#])" + re.escape(alias) + r"(?![A-Za-z0-9+#])", re.IGNORECASE)


_PATTERNS = {skill: [_pattern(a) for a in aliases] for skill, aliases in SKILL_DB.items()}


def extract_skills(text: str) -> set[str]:
    """Return the set of canonical skills found in `text`."""
    return {skill for skill, pats in _PATTERNS.items() if any(p.search(text) for p in pats)}
