# Draft Oil Evidence Submission Checklist

Status: DRAFT. The implementation and corpus receipts are available, but the formal experiment results and complete submission package are not ready. An unchecked item below is not supplied by a plan, a directory name or an engineering smoke test.

The student reports instructor approval for individual completion and machine annotation in place of manual labeling. Preserve this accepted deviation in the final report and, if available, retain the instructor's confirmation with the private course records. Machine labels and model agreement must remain explicitly named; no human agreement is claimed.

## Cover and course requirements

- [ ] Fill in group number: ____________________.
- [ ] Fill in English student name: ____________________.
- [ ] Fill in matriculation number: ____________________.
- [ ] Include Q1 through Q5 in the final PDF and explain the approved solo and machine-annotation workflow.
- [ ] Name the final PDF using the required group number; do not invent a temporary group identity.
- [ ] Check the course submission portal and final links before submitting. The brief says that only the first submission counts.
- [ ] Prepare the in-person presentation and a working demonstration.

The extracted brief records a deadline of 7 November 2026 at 23:59 Singapore time. The report and presentation have separate assessment requirements; the local [acceptance checklist](ACCEPTANCE.md) is the requirement reference, not evidence that these tasks are complete.

## Verified inputs

| Artifact | Current status | Evidence |
|---|---|---|
| Staging corpus | 11,815 passages, 1,562,715 words, 28,582 types, 1,527 contributing documents | [Aggregate receipt](../reports/progress.json) |
| Segmentation rules | Shared 160 target, 65/240 soft bounds, 480 context cap | [Processing record](UNIFIED_CORPUS.md) |
| Staging vector index | 11,815 by 384 float32, hash and order checks passed | [Aggregate receipt](../reports/progress.json) |
| Real retrieval operational checks | 24 passed; date, region and offsets checked | [Aggregate receipt](../reports/progress.json) |
| Development retrieval | 50 questions, 150 real rankings, 1,500 returned hits, 973 pooled question-evidence pairs; zero returned future/unknown-date hits | Local receipt identified in [the report](FINAL_REPORT.md) |
| Warm development retrieval latency | BM25 median 0.175440 s; dense 0.193433 s; hybrid 0.201786 s; 50 queries per mode at depth 10 | Actual median/p95 table in [the report](FINAL_REPORT.md) |
| English publication fixture suite | 1,415 passed, zero failed, three documented skips | [Publication receipt](../reports/english_publication.json) |
| Initial development questions | 50 fixed questions; no reference answers or qrels yet | [Preparation record](DEVELOPMENT_QUESTIONS.md) |
| Existing machine archives | 100 QA records, 4,500 legacy paragraph labels and 728 targeted reviews | [Implementation record](IMPLEMENTATION_REPORT.md) |
| Held-out evaluation | Not frozen or evaluated | [Annotation protocol](ANNOTATION.md) |

The staged corpus has not been released as the default library. The existing 10,079-passage library and the archived annotation corpus must not be silently mixed with new-version experiments. Historical private receipts do not certify translated public source hashes.

## Experimental completion gates

- [ ] Fix 200 development and 1,000 held-out QA records with event-group isolation, duplicate checks and legacy-exposure exclusions.
- [x] Save the initial 50-question shared pool with mode/rank and authoring hints hidden: 973 question-evidence pairs, matching artifact hashes.
- [ ] Complete identical pooled inputs for all 200 development and 1,000 held-out questions, hiding prior labels and the other execution's output.
- [ ] Record requested and observed model identity, prompt and input hashes, decoding settings, raw responses and usage for each run.
- [ ] Complete two separately blinded Codex annotation executions and schema, quotation, date and statistical-scope validation. The student selected all-Codex annotation; same-model executions do not establish different-model diversity or human agreement.
- [ ] Compute original-output agreement before adjudication, including coverage, missing records, class distributions, raw agreement and appropriate kappa measures.
- [ ] Keep unresolved cases and separate adjudication outputs; inspect reproducible consensus samples for shared errors.
- [ ] Freeze a distinct machine-only evaluation version without altering the human-only freezing gate or old archives.
- [ ] Report BM25, dense and hybrid Precision@5, pooled Recall@5, MRR@5, nDCG@5 and judged fraction.
- [ ] Run base, A, B and A plus B under identical frozen test settings; retain all outputs and failures.
- [ ] Report answer quality, citation support, time errors and insufficiency handling with evaluator provenance.
- [x] Measure warm sequential retrieval median and p95 on the initial 50 questions in all three modes at depth 10. This is development-only operational latency.
- [ ] Measure final held-out retrieval and end-to-end latency, concurrent throughput and actual run costs on recorded hardware; distinguish recorded CLI token usage from unmeasured subscription-credit consumption.
- [ ] Save five fresh UI query outputs with corpus identity, citations, cutoff, source links and speed.
- [ ] Pass the applicable source and retrieval release gates before connecting the staging library to the default workbench.

The earlier hybrid-support decline from 9/12 to 8/12 remains a failed diagnostic, not a passing new-version result. A successful fixture suite cannot replace the ranked or downstream evaluation.

## Submission manifest

This manifest distinguishes files that exist from artifacts that still need to be created. Names below are package roles, not promises of completed archives.

| Deliverable | Actual artifact or required content | State |
|---|---|---|
| Final report PDF | Group-named PDF with cover, Q1 to Q5, actual results, failures and references | Not produced |
| Report source | [FINAL_REPORT.md](FINAL_REPORT.md) | Draft exists |
| Source code archive | Versioned `src/`, `scripts/`, `app.py`, configuration, tests and licenses | Not packaged |
| Library and environment archive | Dependency manifest, `uv.lock`, runtime/version instructions and permitted dependencies | Not packaged; do not assume model-weight redistribution rights |
| README archive | Startup, reconstruction prerequisites, experiments and package navigation | Not packaged; current [README](../README.md) exists |
| Data link | Exact corpus registry, allowed cleaned data, QA dataset and documented licensing exclusions | Not supplied; raw-data redistribution unresolved |
| Results link | Rankings, qrels, original annotations, agreement, ablations, timings, cost and hashes | Not supplied; final experiments incomplete |
| Presentation | Slides with actual results plus verified demo or fallback | Not produced; [outline](PRESENTATION_OUTLINE.md) exists |
| Submission manifest | Final file inventory, byte sizes, SHA-256 values, commit, access permissions and checked links | Draft only |

## Data access and privacy

Public access to an official webpage does not establish whole-corpus redistribution permission. Review each source family's terms and third-party exceptions before packaging source text, original PDFs, charts or model weights. Retain a rights manifest with inclusion or exclusion decisions. When a document cannot be redistributed, provide the exact official URL, acquisition metadata and permitted reconstruction instructions rather than adding it to a public archive by default.

The public Git repository excludes raw files, corpus text, model weights, annotation histories, databases, secrets and private local paths. The final package must likewise omit API keys, environment-variable files, cost-ledger credentials, unrelated coursework materials and personal data not required by the course. Do not delete uncertain cost reservations to lower reported spending.

The all-Codex workflow supersedes the previous planned DeepSeek annotation pairing. The historical hosted API ledger remains intact; it is not the budget or cost record of new Codex executions. Record subscription and CLI usage honestly without deriving task cost from the user's account quota percentage.

## Final verification

- [ ] Ensure every reported count comes from the exact submitted corpus version.
- [ ] Ensure every table contains measured values or an explicit unavailable value, not fabricated success.
- [ ] Check that original independent labels, final adjudication and human labels are distinguishable.
- [ ] Verify archive contents against an allowlist and scan public text for language and secret leaks.
- [ ] Build and run fixture tests from a clean source checkout with the locked project environment.
- [ ] Replay representative queries with the submitted data and model prerequisites; an empty public clone is not a complete historical replay.
- [ ] Recompute submitted file hashes and validate dataset, corpus, model and index bindings.
- [ ] Open the final PDF and inspect its cover, tables, plots, references, pagination and clickable links.
- [ ] Open the presentation, verify result figures and rehearse the actual demonstration.
- [ ] Test every data and result link with the intended course access permissions.
- [ ] Fill in the final manifest and preserve the exact submission snapshot before the first submission.

Do not mark this checklist complete until the actual PDF, archives, data/results links, frozen evaluation and presentation have been checked.
