"""Check required documents, portable relative links, and source provenance."""

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_DOCS = [
    "START_HERE",
    "PRD",
    "PROBLEM_ANALYSIS",
    "RESEARCH",
    "IDEA_EVALUATION",
    "REQUIREMENTS_TRACEABILITY",
    "ARCHITECTURE",
    "TECH_STACK",
    "INTERFACES",
    "IMPLEMENTATION_PLAN",
    "TESTING_STRATEGY",
    "EXPERIMENT_PLAN",
    "EVALUATION",
    "DECISIONS",
    "RISK_REGISTER",
    "CURRENT_STATE",
    "HANDOFF_PROTOCOL",
    "DEMO_PLAN",
    "PRESENTATION_PLAN",
    "SUBMISSION_CHECKLIST",
    "QUESTIONS_FOR_ORGANIZERS",
]
REQUIRED_TASKS = [
    "AYUSH",
    "KAUSTUBH",
    "MANAS",
    "MAYANK",
    "TASK_BOARD",
    "INTEGRATION",
    "MILESTONES",
    "AGENT_PROMPTS",
]


def main() -> None:
    required = ["README.md", "AGENTS.md", "docs/HANDOFFS/TEMPLATE.md"]
    required += [f"docs/{name}.md" for name in REQUIRED_DOCS]
    required += [f"tasks/{name}.md" for name in REQUIRED_TASKS]
    errors = []
    for name in required:
        path = ROOT / name
        if not path.is_file() or len(path.read_text(encoding="utf-8").strip()) < 100:
            errors.append(f"Missing or empty required document: {name}")
    documents = [ROOT / "README.md", ROOT / "AGENTS.md"]
    documents += list((ROOT / "docs").rglob("*.md")) + list((ROOT / "tasks").glob("*.md"))
    links = 0
    for document in documents:
        text = document.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if "://" in target or target.startswith("#"):
                continue
            target = target.split("#")[0].strip("<>")
            if not (document.parent / target).exists():
                errors.append(f"Broken relative link in {document.relative_to(ROOT)}: {target}")
            links += 1
    pdf = ROOT / "Utkrishta 2026 Participant Problem Statements.pdf"
    expected = "b93d18863425418a296cdbfe14335de73a69761f69d537d88fddb72b917f3ef0"
    if hashlib.sha256(pdf.read_bytes()).hexdigest() != expected:
        errors.append("Official PDF changed; investigate source provenance")
    task_ids = []
    for developer, prefix in (
        ("AYUSH", "AY"),
        ("KAUSTUBH", "KS"),
        ("MANAS", "MN"),
        ("MAYANK", "MY"),
    ):
        text = (ROOT / "tasks" / f"{developer}.md").read_text(encoding="utf-8")
        found = re.findall(rf"^\| ({prefix}-\d{{2}}) \|", text, flags=re.MULTILINE)
        expected_ids = [f"{prefix}-{index:02d}" for index in range(1, 7)]
        if found != expected_ids:
            errors.append(f"Task IDs missing/duplicated/out of order for {developer}: {found}")
        task_ids.extend(found)
    if len(task_ids) != len(set(task_ids)):
        errors.append("Duplicate team task IDs")
    if errors:
        raise SystemExit("\n".join(errors))
    print(
        f"OK: {len(required)} mandatory documents, {links} relative links, "
        f"{len(task_ids)} unique team tasks, official PDF hash"
    )


if __name__ == "__main__":
    main()
