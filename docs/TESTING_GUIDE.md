# EEIA: practical checking guide

## Start

From D:\PythonProject1\EEIA:

```powershell
.\myenv\Scripts\python.exe -m streamlit run app.py
```

Open the Local URL printed by Streamlit. Choose Repository / general in the sidebar for the agent checks below. Clear Chat between independent checks to avoid prior context affecting answers.

## Agent prompts

| Expected agent | Paste this prompt | What to verify |
|---|---|---|
| general | hello | Nonempty greeting; Agents: general |
| code | Explain app/main.py briefly. | Explains validation, graph.invoke and return_details from actual code |
| documentation | Write concise documentation for the EEIA request lifecycle. | Grounded lifecycle documentation; no invented modules |
| bug | Find a possible bug in the request validation logic. Cite evidence and distinguish suspicion from confirmed behavior. | Evidence and uncertainty; no claim tests ran |
| github | Summarize the last three commits briefly. | Hashes/messages agree with git log -3; if fewer commits exist, says so |
| architecture | Explain the architecture of EEIA briefly. | UI -> main -> planner -> retrieval -> agents -> report |
| security | Assess security of source access boundaries. Give at most two evidence-based findings. | Refers to actual path/secret checks; does not invent confirmed exploits |
| review | Perform a code review of request handling. Give at most two actionable findings with evidence. | File-specific actionable review, or acknowledges insufficient evidence |
| devops | Suggest a minimal Docker deployment approach for EEIA. Do not claim deployment was executed. | Suggested commands/configuration; no claim actual deployment occurred |
| testing | Suggest two unit tests for input validation. Do not claim they were executed. | Test cases for empty/oversized questions; no fabricated pass results |
| research | Compare lexical retrieval versus semantic retrieval for engineering documents. Keep it brief. | Comparison, source/knowledge distinction; no claim live web search occurred |

The router can select multiple agents for a prompt containing multiple intents. Research is a router-backed mode rather than a separate research-agent directory. Planner and report are workflow stages rather than selectable chat agents.

## Multi-agent workflow

Paste: Explain app/main.py, identify a potential bug, assess security, and write documentation.

Expected selected agents include code, bug, security and documentation. A combined report should preserve uncertainties. A visible partial-result warning means an agent failed; a nonempty final answer alone does not mean every stage passed.

## PDF / RAG

1. Upload EEIA_Complete_Architecture_Guide.pdf and select Uploaded documents.
2. Ask: What is the role of the Planner Agent? Cite the PDF.
3. Expand Retrieved evidence. Check that source filename, page numbers and excerpts support the answer and its [S1] style labels.
4. Ask: How is it different from the orchestrator? The follow-up should retain the Planner topic.
5. Ask: What was this company's exact revenue in 2025? The guide does not establish that figure: the answer should acknowledge insufficient evidence, not invent a number.
6. Upload the same PDF again: chunk records should not duplicate. Upload a second PDF: both can supply evidence. Remove one from the uploader: it should no longer be an active source.
7. For architecture/security questions about the PDF, keep Uploaded documents selected. Repository / general instead analyzes the local project and may supplement it with selected documents.

## Conversation and isolation

- Send hello, then interact with a sidebar widget. Both messages should remain visible after rerun.
- Tell the assistant: My preferred answer language is Hindi. Then ask a short follow-up. It should use the recent conversation.
- Clear Chat: visible history and backend conversation memory should reset.
- Open a separate browser session/tab: its conversation and uploaded sources should be separate.
- Delete session documents: deletes that session's index and resets the conversation. Do this before closing if you do not want persisted chunks left on disk.
- Download conversation / report: open the Markdown file and compare with displayed conversation.

## Automated checks

Offline regression suite (no Azure calls):

```powershell
.\myenv\Scripts\python.exe -m unittest discover -s tests -p test_regressions.py -v
```

Explicit live smoke run (uses configured Azure credentials, makes billable model calls and sends relevant project evidence):

```powershell
.\myenv\Scripts\python.exe -u tests/smoke_agents.py
```

Read docs/agent-smoke-results.json for each prompt, selected agents, response and timing. PASS means the expected agent was selected, a nonempty answer returned, and no agent error was reported. It does not certify every factual statement, citation or proposed fix. Inspect the actual answers against source files and PDF excerpts.

## Failures to recognize

- Unable to answer: visible failure; inspect model configuration/network or supplied input.
- No retrieved evidence: question may not be supported by selected documents.
- Git Error: check repository access and git log locally.
- Empty/unrelated answer or wrong Agents list: record the exact prompt, selected mode and response for a reproducible bug report.

No autonomous code editing, real test execution, deployment, OCR or live external web research is implemented by these chat agents. They provide analysis/suggestions; run proposed tests separately to verify them.
