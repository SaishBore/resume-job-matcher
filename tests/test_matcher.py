from matcher import analyze, extract_skills
from matcher.scoring import text_similarity


def test_extract_skills_handles_symbols_and_case():
    found = extract_skills("Worked with C++, POWER BI and scikit-learn. Also Java.")
    assert {"C++", "Power BI", "Scikit-learn", "Java"} <= found


def test_java_does_not_match_javascript():
    assert "Java" not in extract_skills("I know JavaScript only")


def test_perfect_match_scores_high():
    text = "Python SQL Pandas project github@example.com github"
    r = analyze(text, "Python SQL Pandas")
    assert r.skill_score == 100.0 and not r.missing


def test_missing_skill_is_reported_with_tip():
    r = analyze("I know Python. project github a@b.com", "Python and LangChain")
    assert r.missing == {"LangChain"}
    assert any("LangChain" in s for s in r.suggestions)


def test_similarity_is_between_zero_and_one():
    assert 0 <= text_similarity("python code", "python data") <= 1
