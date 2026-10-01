"""Command-line interface.

Usage:
    python main.py --resume data/sample_resume.txt --job data/sample_job.txt
    python main.py --resume my_resume.pdf --job job_description.txt
"""
import argparse

from matcher import analyze, read_resume


def main() -> None:
    parser = argparse.ArgumentParser(description="Match a resume against a job description.")
    parser.add_argument("--resume", required=True, help="resume file (.pdf or .txt)")
    parser.add_argument("--job", required=True, help="job description file (.txt)")
    args = parser.parse_args()

    report = analyze(read_resume(args.resume), read_resume(args.job))

    print(f"\nOverall match : {report.overall_score}%")
    print(f"Skill coverage: {report.skill_score}%  ({len(report.matched)} of {len(report.required_skills)} required skills)")
    print(f"Text similarity: {report.text_similarity}")
    print(f"\nMatched skills : {', '.join(sorted(report.matched)) or 'none'}")
    print(f"Missing skills : {', '.join(sorted(report.missing)) or 'none'}")
    print(f"Extra skills   : {', '.join(sorted(report.extra)) or 'none'}")
    print("\nSuggestions:")
    for i, tip in enumerate(report.suggestions, 1):
        print(f"  {i}. {tip}")


if __name__ == "__main__":
    main()
