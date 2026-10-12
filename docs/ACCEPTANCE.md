# AI6127 assignment acceptance

Source of truth: ../Assignment(1).pdf in the course root (four pages, 2026). This checklist records requirements, not proof of completion.

| Item | Requirement | Evidence to produce |
|---|---|---|
| Knowledge base, Q1 / 20 points | >=10,000 documents/passages AND >=100,000 words; report documents/chunks/words/types, gathering/cleaning/storage and application examples | corpus.json plus source registry, cleaning configuration, manual QA |
| Retrieval / 40 points | sparse + dense + hybrid; not SQL LIKE search | three separately runnable modes and comparable results |
| Q2 | simple friendly UI, five queries/results and query speed | UI verification and saved five-query runs |
| Q3 | motivated retrieval/ranking improvements, examples, explicit ranked retrieval evaluation | development comparison, pooled qrels, Precision@K, Recall@K, MRR, nDCG |
| Generation / 40 points | task answers conditioned on retrieved evidence, justified method and preprocessing | cited answer traces and method explanation |
| Q4 annotation | >=1,000 manually labelled records; >=80% inter-annotator agreement; 3 recommended, 2 allowed | independent human judgments, coverage, raw agreement and supplementary kappa |
| Q4 quality | task-appropriate quality and answer faithfulness/relevance/context relevance; latency, throughput, cost, scalability | formal results, human/automatic distinction, performance records |
| Q5 | downstream improvement; ablations for multiple innovations | base, A, B, A+B under identical test settings |
| Submission | one PDF named group number, names and matriculation numbers on first page, Q1–Q5, links to data/results and source/library/README archives | checked submission manifest and links |
| Presentation | in-person week 13 | slides and demonstrable application |

Deadline: 7 November 2026 23:59 Singapore. Only first submission counts. Report weight 35%; local assessment_criteria.md separately lists presentation 30%. Late penalty: 5 percentage points per rounded-up day.

## Outstanding course decisions

The brief requires randomly assigned groups of 5–6. The user currently intends to implement alone. We must not represent an exemption as granted.

Ask the instructor: May this project be completed individually? Does model prelabelling followed by record-by-record human correction satisfy “manually labeling”? What independently double-annotated coverage and agreement definition are expected, and may a second person assist only in annotation?

Do not send this question to anyone without explicit messaging authorization. Record the actual response here when provided. Engineering can proceed meanwhile; formal annotation compliance remains pending.

## User-selected implementation deviation (2026-10-10)

The user selected a machine-only evaluation workflow because manual annotation is not feasible: Codex Sol 6.1 and DeepSeek Flash 4.1 independently label the same QA records, followed by model-agreement measurement and separate adjudication. The user accepted describing this accurately as model annotation, not manual annotation. This is a planned implementation choice, not instructor approval or satisfaction of the original Q4 human-labeling requirement. Preserve the requirement above and disclose the deviation in the final report. The dependency-ordered work is in `TASKS.md`; no annotation was launched when recording this decision.
