import re


class PlannerService:
    # Match words, not substrings: "digital" must not route to Git.
    PATTERNS = {
        'documentation': r'\b(pdf|document|documents|documentation|manual|chapter|summarize|summary)\b',
        'devops': r'\b(devops|deploy|deployment|docker|dockerfile|kubernetes|ci/cd|github actions)\b',
        'github': r'\b(git|github|commits?|branches|branch|diff|blame|contributors?|changelog|release notes)\b',
        'bug': r'\b(bugs?|errors?|exception|traceback|debug|debugging|crash|failed|failure)\b',
        'security': r'\b(security|vulnerabilit\w*|secrets?|sql injection|xss|csrf)\b',
        'review': r'\b(code review|review code|code quality|code smells|maintainability)\b',
        'testing': r'\b(tests?|testing|pytest|coverage)\b',
        'architecture': r'\b(architecture|system design|data flow|request flow|project structure)\b',
        'code': r'\.(py|js|ts|java|cpp)\b|\b(source code|functions?|classes?|methods?|explain code|explain project)\b',
        'research': r'\b(research|compare|trade-offs|tradeoffs)\b',
    }

    @classmethod
    def detect_agents(cls, question):
        matches = [name for name, pattern in cls.PATTERNS.items() if re.search(pattern, question, re.I)]
        if 'devops' in matches and 'github' in matches and 'github actions' in question.lower():
            matches.remove('github')
        return matches

    @classmethod
    def detect_agent(cls, question):
        matches = cls.detect_agents(question)
        return matches[0] if matches else None
