# Agent verification results

Live route smoke checks: 11/11 returned responses. Offline regressions: 12/12 passed.

These are connectivity and execution checks, not proof that every generated answer is correct.

| Agent | Live execution | Answer review |
|---|---|---|
| general | PASS | Response received; no exhaustive factual audit performed. |
| code | PASS | Explains main.py functions, but incorrectly expands the EEIA acronym and ignores the request for brevity. |
| documentation | PASS | Needs improvement: returned insufficient evidence for a broad request-lifecycle documentation question. |
| bug | PASS | Response received; no exhaustive factual audit performed. |
| github | PASS | Commit hash and single-commit history matched git log -3. Summarize also selected documentation. |
| architecture | PASS | Response received; no exhaustive factual audit performed. |
| security | PASS | Needs review: suggested a speculative subprocess injection concern although GitHubService uses argument lists without shell=True. |
| review | PASS | Response received; no exhaustive factual audit performed. |
| devops | PASS | Suggested configuration only; Docker build was not executed and proposed Python version/dependency compatibility was not verified. |
| testing | PASS | Needs improvement: broad input-validation prompt focused on LLMService instead of app.main.chat; generated tests were not executed. |
| research | PASS | Returned a useful comparison, but cited agent findings rather than external primary sources. No web search took place. |

## Practical next checks

Use explicit file/function names for source-grounded requests. For example: Write documentation for app/main.py, or Generate unit tests for app/main.py chat() rejecting empty questions and questions over 16000 characters. Such requests can correctly select both code and the requested specialist.

Full prompts, answers, plans and timings are in agent-smoke-results.json. The repeatable run instructions and PDF/memory checks are in TESTING_GUIDE.md.

The current project has one commit, 5faaa63; the GitHub response correctly reported that three commits were unavailable.
