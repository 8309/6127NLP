# Oil Evidence development question preparation

Fifty bilingual development questions are fixed for the next retrieval-debugging round: 16 factual, 14 temporal, 10 comparison and 10 evidence-sufficiency challenges. These categories describe design intent, not answerability labels. There are no reference answers, relevance judgments or human ground truth, and no formal test set has been frozen.

## Question list and inputs

Local artifacts are under `data/development_runs/oil-dev50-v1/`; `current.json` points to the verified fixed version:

- `preview.md`: each question in Chinese and English with its query cutoff date, for local review.
- `questions.json`: questions, development-only purpose, provisional event groups and design categories.
- `annotation_queries.jsonl`: only the question ID, English text, Chinese text and cutoff date. It includes no authoring evidence, category priors, answers or old model suggestions. A shared candidate evidence pool is still required to create a complete independent annotation input.
- `authoring_anchors.jsonl`: 73 separately stored exact authoring quotations with sources and offsets. These are not an exhaustive relevance set or qrels. Eight post-cutoff quotations are future-leakage controls only, not positive evidence available at that cutoff.
- `heldout_exclusions.json`: development event groups, the 37 selected documents, and URL/raw-hash aliases. Future test questions must also exclude exposures recorded in `legacy_inventory.json` and related reports from the same event.
- `manifest.json`: hashes and usage restrictions for questions, sources, code, index and artifacts.

The physical question-file SHA-256 is `52ab087fbb60c9ede20e0da7e97d600d69ac6cc9b93202ce96b8c446aa039926`. The snapshot is in `frozen/<that SHA>/`. Local data are excluded from the GitHub repository; the English publication edition does not change that scope or translate the frozen inputs. Historical receipts remain bound to the canonical bilingual implementation and local snapshot, not the translated public code.

## Completed checks

The existing 30 seed questions all repeat items in the old 100 QA records and were not counted as new. The exclusion inventory was reconstructed from complete old candidate pools, evidence, quotations and frozen probes, covering 124 previously exposed documents plus URL/raw-byte aliases. The new questions use 37 other documents across nine source classes. Exact English/Chinese duplicates, known legacy-document reuse and quotation-date violations are zero.

All authoring quotations were checked against accepted passages and exact character offsets in cleaned source pages; hashes of the 37 originals also matched. Subjects, units, statistical periods, forecast versus observation, and legal effect versus physical flows remain distinct. Machine semantic review corrected confusion between Trans Mountain completion and operation, between the Sovcomflot company designation and vessel-property identification, and event grouping within the same Ida impact chain. Two English evidence-sufficiency questions were aligned with their Chinese counterparts. Questions using a common refining-capacity report share a conservative group.

The questions reserve 27 development event groups; these are not 27 verified independent events. Two BOEM questions may share a policy lineage with the old national program and retain a verification warning. Future tests must exclude the entire related lineage. Exact programmatic de-duplication and machine review do not establish exhaustive semantic independence.

The related test command exited 0: 141 passed and one Windows symlink-permission skip. The fixed version supports repeatable readback. Existing corpus, vectors, labels, ledgers and all 19 core implementation files are unchanged. The earlier mismatch between LF logical hashes and Windows CRLF physical-file hashes was corrected. The previous snapshot and `preparation_hash_correction.json` remain; question contents were not changed or replaced using retrieval outcomes.

## Next step

Run the fixed questions through BM25, dense and hybrid retrieval, retaining complete rankings and one merged candidate evidence pool. Independently annotate under the agreed protocol, record disagreements before a separate adjudication pass, and preserve the original outputs. Without qrels, authoring-anchor hit rates must not be called accuracy or comprehensive recall. The eventual 200 development and 1,000 independent test records remain future targets; these 50 questions are an initial development subset.

To verify existing local inputs and fixed artifacts in the matching canonical checkout, run:

```powershell
.\.venv\Scripts\python.exe -X utf8 scripts/prepare_development_questions.py
```

This command does not retrieve evidence, generate answers or annotations, invoke paid APIs, change the workbench library or push to GitHub. Codex subscription usage is unmeasured. Instructor confirmation of human-annotation and independent-human agreement requirements remains pending.
