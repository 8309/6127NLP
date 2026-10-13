# Oil Evidence current progress

Source acquisition and uniform cleaning are closed out. The 11,815-passage staging corpus has a local index that passed integrity checks. The default knowledge base is unchanged. The initial 50-record machine-only DEVELOPMENT evaluation is complete; full held-out comparison and default-library release remain pending. This repository publishes implementation and progress, not the complete local data.

This is the English publication edition. Historical private receipts verify the preserved canonical bilingual implementation, not the newly translated public code or interface. Exact historical replay requires the matching original implementation and the excluded raw-data snapshot. The English edition does not rebuild or certify a new corpus.

The publication checkout passed 1,415 fixture tests, with zero failures and three skips (two host symlink-permission limitations and one excluded-data sample test). A separate read-only check against the retained official PDF samples passed, as did a synthetic English workbench smoke. The public language check found no literal Han text. The initial non-hermetic test failure and its isolated fixture repair remain recorded in [the publication receipt](../reports/english_publication.json); this is not a new formal retrieval evaluation. See [publication edition boundaries](PUBLICATION_EDITION.md).

## Verified results

- The staging corpus contains 11,815 de-duplicated passages, 1,562,715 words and 28,582 unique words from 1,527 contributing documents and 5,703 cleaned source pages. It exceeds the 10,000-passage requirement by 1,815 passages, or 18.15%.
- All sources use one segmentation policy: a 160-word target, soft bounds of 65/240 words and a 480-word context cap. Mixed public comments/government responses, references and unverifiable tail pages are conservatively held out. Originals and failure cases remain local.
- The historical local source-closeout full suite passed 1,171 tests, with one Windows symlink-permission skip and zero failures. Source-reconstruction audit exited 0; four principal artifacts reproduced byte for byte and the 19 implementation hashes matched. These are recorded local results, not GitHub Actions results.
- The same 66 fixed machine source-review cases and two additional diagnostics are preserved. Known critical defects were excluded and 34 warnings remain. This is not corpus-wide human review or human ground truth.
- The default library remains at 10,079 passages. The original 4,500 machine paragraph labels, 100 QA records and 728 machine reviews retain their original versions. New passage IDs do not inherit labels.
- The new index contains an 11,815 x 384 float32 matrix produced by the cached local English BGE model. Source reconstruction before and after indexing and vector/corpus/ID-order/model hashes passed. Related tests passed 268 checks, and 24 real retrieval runs passed date, region and source-offset checks. These do not establish retrieval accuracy or release-gate acceptance.
- Fifty initial bilingual development questions are fixed: 16 factual, 14 temporal, 10 comparison and 10 evidence-sufficiency challenges. They use 37 other source documents, with authoring anchors separate from annotator inputs. They produced 150 real rankings and 973 pooled query-evidence pairs. Both fresh-context Codex annotation streams and all 50 source-based machine adjudications are complete and separately frozen. Raw answerability/event agreement is 94.00%; evidence-grade agreement is 93.73%. Neither score is human agreement or accuracy. See [the draft report](FINAL_REPORT.md).
- Actual development @5 metrics favor hybrid precision, pooled recall and nDCG (0.556, 0.469 and 0.678); dense MRR is 0.850 versus hybrid 0.849. At @10, dense has higher precision/MRR, while hybrid has higher pooled recall/nDCG. Recall is relative to the judged pool; one zero-positive pool is excluded from recall/nDCG. No held-out superiority is claimed.
- A five-case development ablation completes four saved generation executions plus three fresh support/judge calls. A removes six future retrieved passages; B removes zero claims, so the automatic score ceilings do not demonstrate a B benefit. All failures and unknown usage are retained.
- The Codex-default staging UI passes one actual in-process query, with five evidence passages and 15.918344 seconds end to end. Background HTTP launch was blocked and not bypassed. An editable 12-slide presentation and visually checked Q1-Q5 PDF draft exist locally, but no final submission is certified.
- The latest full engineering-suite checkpoint passes 1,914 tests with zero failures and three documented skips in 283.64 seconds. Later code additions require their own verification; these tests are not RAG quality scores.
- Exact question selection is now locked at 200 development and 1,000 TEST questions, with 18 unused reserves preserved. Their top-five, six-condition retrieval produces 7,200 rankings. Fresh paired annotations are still running; source-authored question counts do not establish accepted labels, a final dataset freeze or complete held-out experiments.

[reports/progress.json](../reports/progress.json) contains aggregate results and hashes of the corresponding private local reports. See [UNIFIED_CORPUS.md](UNIFIED_CORPUS.md) for processing and failure records and [TASKS.md](../TASKS.md) for the full task list.

## Remaining tasks

1. Finish source-authored question selection for 200 development and 1,000 held-out records without changing source passages, weakening family reservations or padding with paraphrases.
2. Retrieve identical blind evidence pools, complete both fresh machine annotation streams and source-based adjudication, and bind the actual formal runtime before the final machine-only freeze.
3. Complete formal retrieval/answer evaluation, both improvement ablations, performance measurements and usage reporting on the frozen held-out cohort.
4. Finalize the report, presentation and permitted data/code/results packages, validate submission links and preserve the exact submission snapshot.

The earlier smaller uniform corpus's hybrid-support regression remains failure evidence; it does not establish whether the current candidate passes. Instructor approval for solo completion and the machine-annotation substitute is user-reported. Cover identifiers stay blank by request. Machine agreement is not human agreement, and unknown native model identity does not establish model diversity. The 1,000 accepted test-record gate remains unchanged.

## Included and excluded materials

The repository includes `src/`, `scripts/`, `tests/`, `seeds/`, `docs/`, the local workbench entry point, locked dependencies and an aggregate public progress summary. Service endpoints and model roles in configuration contain no API keys.

`data/`, `models/`, `tmp/`, `.venv/`, environment-variable files, logs, databases and private keys are excluded. The original coursework assignment PDF is also excluded; [ACCEPTANCE.md](ACCEPTANCE.md) contains the extracted requirements.

A fresh clone can install dependencies with `uv sync --locked --group dev` and run fixture-based tests with `uv run --locked python -m pytest -q`. Historical source reconstruction, queries against an existing knowledge base and annotation replay require the matching local originals, caches, ledgers and frozen snapshots. The public summary supplies status and hashes, not those data; it does not claim that an empty `data/` directory can reproduce historical results.

## Exporting the public progress summary

In the canonical working directory retaining the complete private closeout artifacts, run:

```powershell
.\.venv\Scripts\python.exe -X utf8 scripts/export_public_progress.py
```

The exporter reads local closeout and subsequent index receipts and validates bindings among the corpus, reports, implementation, JUnit XML, actual vectors and model files before updating `reports/progress.json`. Historical source audit and current index verification are separate. Without an index receipt it retains the older state; invalid receipts fail closed. It does not acquire sources, invoke models, rebuild an index or export text, questions, evidence or annotations. Updating the summary does not automatically commit or push to GitHub. The translated publication checkout is not a substitute for the canonical implementation required by those historical guards.
