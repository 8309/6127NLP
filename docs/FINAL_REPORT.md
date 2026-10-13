# Draft Oil Evidence Coursework Report

Course: AI6127 Natural Language Processing

Group number: ____________________

Student name: ____________________

Matriculation number: ____________________

Status: DRAFT. Not ready for submission until the held-out evaluation, measured results, final demonstration and submission links are complete.

## Abstract

Oil Evidence is a local retrieval augmented generation (RAG) workbench for questions about crude-oil supply, production policies, sanctions and transport disruptions. Its central requirement is to explain what the available evidence establishes at a specified cutoff date, rather than predict prices or provide investment advice. The system combines keyword and semantic retrieval, presents traceable evidence, and optionally generates cited claims with a second support-checking pass.

The verified staging knowledge base contains 11,815 passages, 1,562,715 words and 28,582 unique word types from 1,527 contributing documents. A local 384-dimensional vector index and three retrieval modes passed operational checks. Fifty fixed development questions produced 150 actual retrieval runs and 1,500 ranked hits, merged into 973 question-evidence pairs for annotation. These results establish corpus size, provenance and functioning retrieval, not answer accuracy. The planned 200 development and 1,000 held-out machine-annotated question records, ranked retrieval metrics, answer-quality measurements and innovation ablations are not complete at this draft snapshot. Their result fields therefore remain unreported. [1][2][12]

The student reports instructor approval for individual completion and for machine annotation in place of manual labeling. Model outputs remain identified as machine annotations; model agreement will not be described as agreement between human annotators. Group number, name and matriculation number are intentionally blank until the student supplies them.

## Q1 Knowledge base and application

### Application scope

The workbench supports factual, temporal, comparative and evidence-sufficiency questions. Example tasks include retrieving an official production outlook, separating an announced policy from evidence of implementation, comparing supply disruptions, and identifying when the documents cannot support a causal or quantitative conclusion. A query includes an English question, an optional region filter and an information cutoff date.

The fixed collection window is 1 January 2018 through 5 October 2026. Publication date, conservative availability date, event date and the period described by a statistic are separate fields. This distinction is important because a forecast for a future year can be legitimate evidence before that year, whereas a later publication cannot establish what was available at an earlier cutoff. [2]

### Sources and collection

The corpus draws on official energy and policy material. Its source families include the US Energy Information Administration's outlooks, oil articles, country analyses and methodology; US Treasury and Office of Foreign Assets Control policy announcements; Strategic Petroleum Reserve material; offshore policy and production reports; Dallas Federal Reserve energy surveys; UK and Australian oil statistics; and World Bank commodity reports. Different source families provide outlooks, reported observations, legal actions and mechanism background; these roles are not interchangeable. Exact current contribution counts by source should accompany the final source-registry export, rather than be inferred from earlier expansion counts. [2][3]

Three source-registry examples are EIA's crude-price and refinery-margin article dated 5 October 2026, Treasury's announcement concerning an oil-smuggling network dated 26 February 2018, and DOE's Strategic Petroleum Reserve crude-sale notice dated 28 February 2019. Their exact official URLs are retained below. They identify actual documents admitted to the selected corpus, not examples of completed answer evaluation. [13][14][15]

Collection records the requested URL, source identity, title, publication and availability evidence, collection time, bytes and SHA-256 hash. Requests respect robots restrictions, a one-second minimum interval per host, a 25 MB document limit, a 300 MB invocation limit and limited retries. Forbidden and failed responses remain recorded without being counted as acquired evidence. OPEC access restrictions and EU Council robots failures were not bypassed. Original files and acquisition manifests remain local. [2]

### Cleaning and passage construction

Cleaning extracts approved article bodies and oil-related PDF sections, removes repeated navigation and obvious nonbody content, and quarantines uncertain tables, charts, reference lists and source versions. Every admitted body uses the same complete-sentence segmentation policy: a 160-word target, soft bounds of 65 and 240 words, and a 480-word context safety ceiling. These are structural targets rather than a requirement that every passage have the same length. Short complete statements and long indivisible sentences can differ in length while retaining consistent admission rules. [2]

Passages do not overlap. Each passage retains its document and source-page identifiers, physical page or article body, exact character offsets, text, source URL, dates and regions. Original text is preserved separately from exclusions and quarantine reasons. Exact deduplication is performed; semantic near-duplicate review remains limited. Historical parent passages are not indexed or counted alongside their replacement children. Newly created passage IDs do not inherit old machine labels. [2]

### Corpus statistics

| Quantity | Verified staging value |
|---|---:|
| Admitted passages | 11,815 |
| Word tokens | 1,562,715 |
| Unique word types | 28,582 |
| Contributing documents | 1,527 |
| Cleaned source pages | 5,703 |
| Passage margin above 10,000 | 1,815, or 18.15% |
| Vector dimensions | 384 |

Word statistics use the project's lowercased alphanumeric tokenizer, which retains selected internal punctuation. The unique-type count is a tokenizer-dependent vocabulary statistic, not the number of distinct concepts. The passage and word thresholds are met numerically. Fixed machine source checks preserve 68 original cases and diagnostics, with no remaining known critical issue in that sample and 34 retained warnings; this does not establish a corpus-wide error rate. [1][2]

The 11,815-passage corpus is a verified staging candidate and has not replaced the 10,079-passage default workbench library. Corpus-size claims, demonstration outputs and experimental results must name the corpus they actually use. Raw-document redistribution rights remain unresolved, so this draft does not provide a public raw-data archive. [1]

## Q2 Retrieval system and interface

### Retrieval methods

The sparse baseline uses BM25 keyword retrieval over tokenized passage text. This provides inspectable matches for names, units and policy terms. The dense baseline uses the local English model `BAAI/bge-small-en-v1.5`. Passage and query vectors are normalized, and their dot product supplies cosine-similarity ranking. The verified index stores an 11,815 by 384 float32 matrix; model-file, corpus, vector and passage-order hashes guard against stale or mismatched indexes. [1][2]

Hybrid retrieval combines the sparse and dense ranks using reciprocal rank fusion (RRF). Each candidate receives a contribution of `1 / (60 + rank)` from each ranking in which it appears. This avoids assuming that BM25 scores and cosine similarities share a comparable scale. The configured candidate pool is 50 per mode, and the default displayed result count is five. Eligibility filters are applied before final candidate ranking. This combination is motivated by complementary lexical and semantic matching; superiority has not yet been established by a ranked evaluation. [4]

### User interface and five demonstration questions

The Streamlit interface provides query entry, cutoff and region controls, evidence cards, original-source links, machine-annotation review and passage-label inspection. Evidence cards expose identifiers, source dates and full text so that users can inspect claims rather than rely on a fluent answer alone. The application binds to localhost and is not an authenticated public service. [3]

The final demonstration should save five fresh runs on one explicitly selected corpus. The following questions come from the public question seeds; they are demonstration choices, not test-set ground truth. [5]

| Question | Cutoff | Demonstration purpose |
|---|---|---|
| What does EIA project for US crude oil production, and in what units? | 2026-10-05 | Preserve quantities, units and forecast periods |
| As of 2025-06-30, what oil supply outlook had EIA published? | 2025-06-30 | Retrieve historical information rather than the latest report |
| What evidence shows that an announced OPEC production adjustment was implemented? | 2026-10-05 | Separate announcement from implementation and possible insufficiency |
| Which sanctions affecting Russian oil were effective as of 2025-02-01? | 2025-02-01 | Inspect legal dates and the scope of the policy evidence |
| What exact Brent price will occur next month, according to verified evidence? | 2026-10-05 | Avoid presenting a forecast as a certain future observation |

The new index passed 24 real operational checks across BM25, dense and hybrid modes, including cutoff, region and exact source-offset checks. The English publication edition separately passed a synthetic four-tab interface smoke test. Five historical API answer examples exist on an earlier 2,176-passage snapshot, but they are not fresh outputs or quality measurements for the current staging corpus. Fresh five-query results and their retrieval and end-to-end latency values remain required. [1][3][6]

## Q3 Retrieval improvements and ranked evaluation

### Improvement A Temporal eligibility

Improvement A excludes passages whose conservative `available_by` date exceeds the query cutoff. Missing availability fails closed. Month-only dates use month-end upper bounds rather than invented publication days. Filtering occurs before the ranked result set is selected, so later documents cannot occupy result slots and then disappear after ranking. [2][4]

This is an evidence-availability constraint, not a complete historical simulation of model knowledge. BM25 corpus statistics and the embedding index are constructed from the selected corpus, and model pretraining may contain other information. A zero future-evidence count therefore supports only the absence of post-cutoff passages in the returned evidence under the recorded metadata.

### Development and test protocol

Fifty fixed initial development questions are available: 16 factual, 14 temporal, 10 comparison and 10 evidence-sufficiency challenges. They use 37 source documents across nine source classes and reserve 27 provisional development event groups. Seventy-three authoring anchors are stored separately from annotation inputs, including eight future-leakage controls that are not positive evidence at their cutoffs. The categories describe question design, not answerability labels. No qrels have been assigned to this batch. [7]

All 50 questions have now been run in each retrieval mode at depth 10, producing 150 actual rankings and 1,500 returned hits. Their union contains 973 question-evidence pairs, with 13 to 27 distinct evidence passages per question and a mean of 19.46. Annotation inputs expose neither retrieval mode or rank nor authoring hints. Every returned hit has a known availability date no later than its cutoff; exact offsets and separate date/region controls passed. The stored inputs, rankings and annotation pool match their receipt hashes. This pool has no relevance labels yet and may omit relevant passages below the three top-10 lists. [12]

The final design targets 200 development records and 1,000 held-out records, split by event group with related documents and legacy exposures excluded from the test partition. Retrieval parameters and prompts must be fixed using development data only. The completed 50-question pool is the initial development subset, not an independent test set or 973 QA records. Each question receives one shared evidence input for blinded annotation; authoring quotations are not an exhaustive relevance set. [8][12]

### Metrics and current results

Ranked evaluation will report Precision@5, pooled Recall@5, MRR@5, nDCG@5 and the judged fraction of retrieved results. Relevance grades are 0 for irrelevant, 1 for useful background or partial support, and 2 for direct answer support. Recall is relative to the judged pool, not every potentially relevant passage in the corpus. Missing judgments must remain unjudged; any metric convention that treats unjudged hits as nonrelevant must be disclosed. [8][9]

| Retrieval mode | Precision@5 | Pooled Recall@5 | MRR@5 | nDCG@5 | Judged fraction |
|---|---|---|---|---|---|
| BM25 | Not measured | Not measured | Not measured | Not measured | Not measured |
| Dense | Not measured | Not measured | Not measured | Not measured | Not measured |
| Hybrid | Not measured | Not measured | Not measured | Not measured | Not measured |

An earlier segmentation candidate failed an unchanged 12-probe source-support comparison: BM25 improved from 4/12 to 6/12, while dense and hybrid each declined from 9/12 to 8/12. Its release gate rejected publication. This small exact-text diagnostic is not the table's formal ranked evaluation and does not establish the newer candidate's quality. The failure shows why increased passage count and successful indexing are insufficient reasons to release a corpus. [2]

## Q4 Evidence conditioned generation and quality assessment

### Generation method and preprocessing

RAG is used instead of fine-tuning because the task depends on inspectable documents, changing report versions and user-selected information cutoffs. Retrieval supplies the evidence explicitly, allowing the answer to cite passage identifiers and expose limits. The query prompt separates crude oil from total liquids, forecasts from reported observations, stock changes from flow rates, and legal announcements from physical production outcomes. Source text is treated as untrusted data rather than executable instructions. [10]

The generator returns an answerability decision, atomic claims with citations and limitations. A structural validator removes claims without valid evidence identifiers. If the eligible evidence is empty, the system states that no evidence was found. Without an API, the application offers an extractive preview: selected source sentences rather than a synthesized or verified answer. Extractive retrieval does not itself establish whether the question is answerable. [10]

### Improvement B Claim support checking

Improvement B gives each generated claim and its cited passages to a separate verifier execution. The verifier checks facts, numbers, dates and units; unsupported claims are removed, and the answer may be marked incomplete. The historical API implementation and configuration used `deepseek-flash` for both generation and verification. Those legacy calls do not verify the pending Codex-only experiment workflow. Actual generator and verifier identities must be recorded for the final runs. Separate executions of the same model can share errors. In extractive-preview mode, B checks literal quotation existence only; that setting cannot demonstrate improved semantic faithfulness. [3][10]

### Machine annotation and agreement

The instructor-approved substitution is reported as machine annotation, based on the student's stated approval. The original brief's manual-labeling and human-agreement language remains recorded in the acceptance checklist. The student has replaced the planned Codex/DeepSeek pairing with an all-Codex workflow. Two separate blinded Codex executions will receive the same fixed evidence and annotation rules, without authoring answers, prior labels or each other's outputs. Actual requested and observed model identifiers must be recorded; an undisclosed model version cannot be invented. Agreement must be computed on the original outputs before a separate adjudication pass. Separate contexts may use the same model, so this measures agreement between blinded executions, not distinct-model diversity or independent-human agreement.

The archive contains 100 machine QA records and 4,500 original passage metadata labels, with 728 targeted machine reviews. These differ in unit, corpus version and selection conditions from the intended 1,000 held-out QA records and are not counted toward that held-out set. There are zero human labels in the recorded archive. Raw agreement, categorical Cohen's kappa and ordinal weighted kappa remain unmeasured for the new paired QA annotation. Model-scored fact alignment, if used, must be reported separately from categorical agreement. [3][8]

### Quality and performance measures

The held-out evaluation must distinguish answer correctness, claim faithfulness to cited evidence, answer relevance, context relevance, citation support, temporal errors and appropriate evidence-insufficiency handling. Lexical token F1 and exact match are supplementary measures, not substitutes for factual correctness. A model judge is an automatic evaluator, not human ground truth; overlap between the generator, verifier, annotators and judge must be disclosed. [9]

The completed development run measured retrieval latency at depth 10 after one separate warm-up per mode. Encoder and BM25 initialization took 0.941 seconds and is excluded from the table. Each row covers 50 sequential queries against the same staged corpus using the cached local encoder. These are retrieval measurements only, not generated-answer latency or a held-out benchmark. [12]

| Retrieval mode | Median seconds | p95 seconds | Sequential queries per second |
|---|---:|---:|---:|
| BM25 | 0.175440 | 0.254552 | 5.443 |
| Dense | 0.193433 | 0.244063 | 5.168 |
| Hybrid | 0.201786 | 0.283275 | 4.928 |

The receipt verifies zero generated answers, new QA annotations, human labels and hosted model calls for this run. It does not supply a complete hardware profile. End-to-end latency and concurrent throughput require separate measurements; sequential queries per second does not establish concurrency capacity. Token usage, completed costs and uncertain reservations should be reported for the exact final experiments. Hosted API cost is separate from local computation and Codex subscription consumption, which remains unmeasured until recorded by the relevant executions. [12]

The historical API ledger recorded 112 completed calls estimated at USD 0.077747, plus an uncertain USD 0.002749 reservation, for USD 0.080496 accounted against the USD 5 ceiling. These are historical configured-rate estimates, not current prices or the cost of a completed final evaluation. Source closeout and English publication added no hosted model calls; Codex subscription use was not measured. Current held-out quality, latency, concurrent throughput and experiment costs remain unreported. [3][6]

## Q5 Downstream improvements and ablations

The two implemented innovations address different failure modes. A limits the evidence to material available at the requested cutoff; B removes generated claims that the cited evidence does not support. Their combined benefit is a hypothesis to test, not an inference from operational checks.

The ablation compares hybrid base, A only, B only and A plus B on the identical frozen corpus and held-out questions, with the same generator, retrieval parameters, prompts and scoring protocol. Generator randomness and supported decoding controls must be recorded. A's temporal-error effect should be examined alongside relevance and evidence sufficiency, and B's faithfulness effect alongside removed claims, answer completeness, additional latency and cost. [9][10]

| Variant | A | B | Quality and citation results | Temporal errors | Latency and cost |
|---|---|---|---|---|---|
| Hybrid base | Off | Off | Not measured | Not measured | Not measured |
| Hybrid A | On | Off | Not measured | Not measured | Not measured |
| Hybrid B | Off | On | Not measured | Not measured | Not measured |
| Hybrid A plus B | On | On | Not measured | Not measured | Not measured |

No completed held-out ablation currently supports an improvement claim. The final report must include actual values, evaluation coverage and failure cases, even if an innovation reduces quality or provides no measurable benefit.

## Validity limitations and failure analysis

Real failures informed the corpus rules. Survey excerpts sometimes lost the year supplied by an adjacent question; PDF continuations began mid-sentence; a large offshore report mixed public comments with government responses; bibliography titles reappeared after deduplication changed. Uniform source rules corrected or quarantined these cases while preserving original failures. Conservative reference-page quarantine also removed some useful mixed-page body text, a disclosed trade-off rather than an invisible repair. [2]

The legacy paragraph review retained 256 unresolved source checks and 200 overlapping advisory strict-evaluation exclusions. These are not 256 confirmed crude-answer errors or an error-rate estimate. They include source-version, statistical-scope and extraction uncertainty. Crude plus condensate, total liquids, refinery input, stocks and daily rates remain distinct quantities; no missing table columns should be reconstructed by the model. [3][8]

Source coverage is uneven, OPEC access is restricted, and tables are conservatively excluded when layout cannot be trusted. Near-duplicate checking is not exhaustive. Availability metadata cannot prove that every downloaded file is the exact historical version. The English embedding model's Chinese-query quality is unverified, so formal questions use English. Model-generated questions and shared annotation or judging models can bias the benchmark toward the system and overlook shared mistakes. These limitations qualify the eventual scores even if all mechanical checks pass.

## Reproducibility and submission status

Code, tests, locked dependencies, configuration and aggregate receipts are available in the [public repository](https://github.com/8309/6127NLP). The English publication edition passed 1,415 fixture tests with zero failures and three documented skips. Two skips involve Windows symlink-creation permission; the third requires excluded local PDFs, which passed a separate read-only sample check. These are engineering verification results, not RAG accuracy results. The canonical corpus's earlier source-closeout suite passed 1,171 tests with one permission skip, and index-related checks passed 268 tests. Those different suites and historical implementations must not be combined into one count. [1][6]

Historical corpus receipts bind the canonical implementation, while the English publication has separate test receipts. Exact historical replay requires the matching local originals, caches, model and source snapshots; a clean clone with no data cannot reproduce the corpus simply by running fixture tests. The default library, old labels and ledgers remain separate from the unpublished staging version. [6][11]

The final submission must replace this draft with a checked PDF named for the group, supply valid data and result links with suitable permissions, and include source/library/README archives and a demonstrable presentation. Identity fields, redistribution clearance, the 1,000-record evaluated QA set, full results and final artifact links remain incomplete. See [the submission checklist](SUBMISSION_CHECKLIST.md) for the actual package state.

## References

1. [Verified aggregate corpus and index progress](../reports/progress.json).
2. [Unified corpus processing and historical failure record](UNIFIED_CORPUS.md).
3. [Implementation, model trials and archived annotation results](IMPLEMENTATION_REPORT.md).
4. [Retrieval implementation](../src/oil_evidence/retrieval.py) and [configuration](../config.toml).
5. [Public representative question seeds](../seeds/questions.json).
6. [English publication verification receipt](../reports/english_publication.json).
7. [Fixed development question preparation](DEVELOPMENT_QUESTIONS.md).
8. [Annotation protocol and provenance](ANNOTATION.md).
9. [Experiment runner and metric definitions](../src/oil_evidence/evaluation.py).
10. [Evidence conditioned query and claim support implementation](../src/oil_evidence/query.py).
11. [English publication and historical replay boundaries](PUBLICATION_EDITION.md).
12. Retained local development retrieval receipt: `data/development_runs/oil-dev50-v1/retrieval/2026-10-12T20-44-48.032312+00-00-64f7e748/result.json`, SHA-256 `6f90350dded13d4be58236cca2c9a3c1e420a26b632c1a930cad595865d70f15`. [Execution implementation](../scripts/run_development_retrieval.py). The receipt and evidence pool remain excluded local artifacts, not public download links.
13. [EIA Crude oil prices and refinery margins generally increased throughout the third quarter](https://www.eia.gov/todayinenergy/detail.php?id=68245), source-registry publication date 2026-10-05.
14. [Treasury Sanctions International Network Smuggling Oil from Libya to Europe](https://home.treasury.gov/news/press-releases/sm0298/), source-registry publication date 2018-02-26.
15. [DOE Announces Notice of Sale of Crude Oil from the Strategic Petroleum Reserve](https://www.energy.gov/articles/doe-announces-notice-sale-crude-oil-strategic-petroleum-reserve), source-registry publication date 2019-02-28.

The final source registry should supply the remaining exact official document URLs, archive hashes and redistribution decisions. The three document examples above do not provide a complete redistributable data package.
