# Interviewer rubric

Use this rubric to evaluate the candidate's engineering process, not only whether
the final test suite passes. The listed skills are prompts for discussion; an
interview should prioritize the assignment's primary objective.

## Core dimensions

| Dimension | Strong evidence |
| --- | --- |
| Clarification and decomposition | Identifies the observable contract, asks about consequential ambiguity, and narrows the work to a testable invariant. |
| Investigation | Traces the behavior through relevant code and tests; separates observed facts from hypotheses. |
| Correctness | Explains why the change handles the reported case and relevant boundaries without violating nearby behavior. |
| Testing | Adds a deterministic regression assertion against externally visible output or state, and can explain what it does not prove. |
| Implementation judgment | Makes a focused, readable change and names trade-offs or limits such as in-memory versus concurrent behavior. |
| Communication and AI judgment | Explains decisions clearly and independently verifies any AI suggestion with repository evidence, tests, or reasoning. |

## Suggested 45–60 minute flow

1. **Clarify (5–8 min):** candidate restates the symptom and contract; interviewer answers only questions needed to proceed.
2. **Investigate (10–15 min):** candidate reads the prompt, relevant code, and tests; asks them to narrate observations and hypotheses.
3. **Change (15–20 min):** candidate makes the smallest reasonable implementation change.
4. **Prove (8–12 min):** candidate adds or runs focused regression tests and discusses boundaries and limitations.
5. **Reflect (3–5 min):** discuss alternatives, risks, and what additional evidence would be needed in production.

For shorter fundamentals exercises, scale the timing while retaining a chance
to explain reasoning. Do not require every follow-up if the core task is not
complete.

## AI-assisted practice

AI may help explain unfamiliar code, suggest diagnostic questions, or propose
tests. Ask the candidate to state what they verified before accepting a
suggestion. Strong evidence includes rejecting an unsupported suggestion,
checking the relevant contract, and using a test or trace to confirm behavior.
Prompt-writing skill alone is not an evaluation dimension.
