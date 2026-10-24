"""Explicit live smoke test: sends repository evidence to the configured Azure deployment."""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.main import chat

CASES = [
    ('general', 'hello'),
    ('code', 'Explain app/main.py briefly.'),
    ('documentation', 'Write concise documentation for the EEIA request lifecycle.'),
    ('bug', 'Find a possible bug in the request validation logic. Cite evidence and distinguish suspicion from confirmed behavior.'),
    ('github', 'Summarize the last three commits briefly.'),
    ('architecture', 'Explain the architecture of EEIA briefly.'),
    ('security', 'Assess security of source access boundaries. Give at most two evidence-based findings.'),
    ('review', 'Perform a code review of request handling. Give at most two actionable findings with evidence.'),
    ('devops', 'Suggest a minimal Docker deployment approach for EEIA. Do not claim deployment was executed.'),
    ('testing', 'Suggest two unit tests for input validation. Do not claim they were executed.'),
    ('research', 'Compare lexical retrieval versus semantic retrieval for engineering documents. Keep it brief.'),
]


def main():
    rows = []
    output = Path(__file__).resolve().parents[1] / 'outputs' / 'agent-smoke-results.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    for expected, prompt in CASES:
        started = time.monotonic()
        try:
            result = chat(prompt, return_details=True)
            plan = result['plan']
            passed = expected in plan and bool(result['answer'].strip()) and not result.get('errors')
            row = {'agent': expected, 'prompt': prompt, 'status': 'PASS' if passed else 'FAIL',
                   'plan': plan, 'answer': result['answer'], 'errors': result.get('errors', [])}
        except Exception as exc:
            row = {'agent': expected, 'prompt': prompt, 'status': 'FAIL', 'error': str(exc)}
        row['seconds'] = round(time.monotonic() - started, 2)
        rows.append(row)
        output.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding='utf-8')
        print(f"{expected}: {row['status']} ({row['seconds']}s)", flush=True)
    print(f'Results: {output}', flush=True)
    return int(any(row['status'] != 'PASS' for row in rows))


if __name__ == '__main__':
    raise SystemExit(main())
