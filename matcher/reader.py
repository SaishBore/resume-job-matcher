"""Read resume text from a .pdf or .txt file."""
from pathlib import Path


def read_resume(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if p.suffix.lower() == ".pdf":
        from pypdf import PdfReader  # lazy import: not needed for .txt
        reader = PdfReader(str(p))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return p.read_text(encoding="utf-8", errors="ignore")
