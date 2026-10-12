# Oil Evidence current progress

As of 2026-10-12, source acquisition and uniform cleaning are closed out. The 11,815-passage staging corpus has a local index that passed integrity checks. The default knowledge base is unchanged; formal retrieval comparison and release remain pending. This repository publishes implementation and progress, not the complete local data.

This is the English publication edition. Historical private receipts verify the preserved canonical bilingual implementation, not the newly translated public code or interface. Exact historical replay requires the matching original implementation and the excluded raw-data snapshot. The English edition does not rebuild or certify a new corpus.

The publication checkout passed 1,415 fixture tests, with zero failures and three skips (two host symlink-permission limitations and one excluded-data sample test). A separate read-only check against the retained official PDF samples passed, as did a synthetic English workbench smoke. The public language check found no literal Han text. The initial non-hermetic test failure and its isolated fixture repair remain recorded in [the publication receipt](../reports/english_publication.json); this is not a new formal retrieval evaluation. See [publication edition boundaries](PUBLICATION_EDITION.md).

## Verified results

- The staging corpus contains 11,815 de-duplicated passages, 1,562,715 words and 28,582 unique words from 1,527 contributing documents and 5,703 cleaned source pages. It exceeds the 10,000-passage requirement by 1,815 passages, or 18.15%.
- All sources use one segmentation policy: a 160-word target, soft bounds of 65/240 words and a 480-word context cap. Mixed public comments/government responses, references and unverifiable tail pages are conservatively held out. Originals and failure cases remain local.
- The historical local source-closeout full suite passed 1,171 tests, with one Windows symlink-permission skip and zero failures. Source-reconstruction audit exited 0; four principal artifacts reproduced byte for byte and the 19 implementation hashes matched. These are recorded local results, not GitHub Actions results.
- The same 66 fixed machine source-review cases and two additional diagnostics are preserved. Known critical defects were excluded and 34 warnings remain. This is not corpus-wide human review or human ground truth.
- The default library remains at 10,079 passages. The original 4,500 machine paragraph labels, 100 QA records and 728 machine reviews retain their original versions. New passage IDs do not inherit labels.
- The new index contains an 11,815 x 384 float32 matrix produced by the cached local English BGE model. Source reconstruction before and after indexing and vector/corpus/ID-order/model hashes passed. Related tests passed 268 checks, and 24 real retrieval runs passed date, region and source-offset checks. These do not establish retrieval accuracy or release-gate acceptance.
- Fifty new bilingual development questions are fixed: 16 factual, 14 temporal, 10 comparison and 10 evidence-sufficiency challenges. They use 37 other source documents, with authoring anchors separate from unlabelled query inputs. Related tests passed 141 checks with one host-permission skip. Design categories are not answer labels; retrieval and independent annotation have not been run on these 50 questions. See [development question preparation](DEVELOPMENT_QUESTIONS.md).

[reports/progress.json](../reports/progress.json) contains aggregate results and hashes of the corresponding private local reports. See [UNIFIED_CORPUS.md](UNIFIED_CORPUS.md) for processing and failure records and [TASKS.md](../TASKS.md) for the full task list.

## Remaining tasks

1. Run the fixed 50 development questions through keyword, dense and hybrid retrieval and create a shared candidate evidence pool.
2. Independently annotate relevance and answers, compare retrieval quality, address defects and pass source/release gates before connecting the new library to the workbench.
3. Prepare 200 development and 1,000 event-isolated test records, independently machine-annotate them, and preserve disagreements and usage records.
4. Complete retrieval/answer evaluation, ablations of both improvements, performance measurements, the report and submission materials.

The earlier smaller uniform corpus's hybrid-support regression remains failure evidence; it does not establish whether the current candidate passes. Instructor confirmation is still needed for formal human annotation, independent-human agreement and solo completion requirements. Machine agreement is not human acceptance.

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
