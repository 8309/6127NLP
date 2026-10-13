# Draft Oil Evidence Coursework Report

Course: AI6127 Natural Language Processing

Group number: ____________________

Student name: ____________________

Matriculation number: ____________________

Status: DRAFT. Not ready for submission until the held-out evaluation, measured results, final demonstration and submission links are complete.

## Abstract

Oil Evidence is a local retrieval augmented generation (RAG) workbench for questions about crude-oil supply, production policies, sanctions and transport disruptions. Its central requirement is to explain what the available evidence establishes at a specified cutoff date, rather than predict prices or provide investment advice. The system combines keyword and semantic retrieval, presents traceable evidence, and optionally generates cited claims with a second support-checking pass.

The verified staging knowledge base contains 11,815 passages, 1,562,715 words and 28,582 unique word types from 1,527 contributing documents. A local 384-dimensional index supports three retrieval modes. Fifty development questions produced 150 rankings and a 973-pair evidence pool, followed by 100 fresh-context machine labels and 50 accepted adjudications. Their frozen development scores favor hybrid retrieval for pooled recall and nDCG, while dense retrieval has slightly higher precision and MRR. A five-case answer experiment completed 30 variant answers. These small machine-derived results do not establish held-out accuracy. Source authoring has reached 205 development questions, but the planned 1,000 accepted test records and full held-out experiments remain incomplete. [1][2][12][18][19]

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

Hybrid retrieval combines the sparse and dense ranks using reciprocal rank fusion (RRF). Each candidate receives a contribution of `1 / (60 + rank)` from each ranking in which it appears. This follows the rank-based fusion formulation of Cormack, Clarke and Buttcher (2009), without assuming that BM25 scores and cosine similarities share a comparable scale. The configured candidate pool is 50 per mode, and the default displayed result count is five. Eligibility filters are applied before final candidate ranking. The development evaluation below measures the lexical/semantic trade-off; it does not establish held-out superiority. [4][18][25]

### User interface and five demonstration questions

The Streamlit interface provides query entry, cutoff and region controls, evidence cards, original-source links, machine-annotation review and passage-label inspection. Evidence cards expose identifiers, source dates and full text so that users can inspect claims rather than rely on a fluent answer alone. The new staging interface defaults to subscription-backed Codex using its existing native ChatGPT login, with no API-key input. It reads the selected 11,815-passage index without changing the historical default library. The application binds to localhost and is not an authenticated public service. [3][17]

Five fresh demonstration queries were run on the verified 11,815-passage staging corpus using hybrid retrieval at depth five. The following questions come from the public seeds; they are demonstration choices, not test-set ground truth. [5][16]

| Question | Cutoff | Demonstration purpose |
|---|---|---|
| What does EIA project for US crude oil production, and in what units? | 2026-10-05 | Preserve quantities, units and forecast periods |
| As of 2025-06-30, what oil supply outlook had EIA published? | 2025-06-30 | Retrieve historical information rather than the latest report |
| What evidence shows that an announced OPEC production adjustment was implemented? | 2026-10-05 | Separate announcement from implementation and possible insufficiency |
| Which sanctions affecting Russian oil were effective as of 2025-02-01? | 2025-02-01 | Inspect legal dates and the scope of the policy evidence |
| What exact Brent price will occur next month, according to verified evidence? | 2026-10-05 | Avoid presenting a forecast as a certain future observation |

The five cases retrieved 25 passages and generated five cited answers in one fresh Codex execution. Retrieval took 0.087971, 0.062281, 0.068672, 0.064153 and 0.081456 seconds respectively, after an excluded warm-up. Shared batch generation took 29.931725 seconds and emitted 27,281 input and 1,240 output tokens. That batch duration is not five independently measured generation latencies; per-query generation and end-to-end values remain unmeasured. All 14 saved artifact hashes matched their receipt. [16]

The first answer cites dated EIA production forecasts and explicitly says they are not a current 2026 outlook. The historical-outlook answer also states that retrieval did not establish the latest June 2025 outlook. The OPEC and Russia-policy answers disclose missing implementation or completeness evidence. The exact future Brent-price question returns no factual claims. These limitations are actual saved generator outputs, not reference labels or independently verified quality scores. In particular, historical-date eligibility alone does not retrieve the newest relevant report. [16]

The new index also passed 24 earlier operational checks, and the English publication passed a synthetic four-tab interface smoke. Five older API examples on a 2,176-passage snapshot remain historical and are not substituted for the new demonstration. No separate verifier or quality judge ran in the new five-case batch. [1][3][6][16]

A separate real in-process Streamlit query exercised all four tabs and the native Codex generation path: five passages, two claims and three exact quotes, with 0.225984 seconds for retrieval/input verification, 15.070134 seconds for native generation and 15.918344 seconds measured end to end. Its execution emitted 18,877 input and 504 output tokens; observed model identity was unavailable and remains null. The generator's sufficient label is not a gold judgment. A background HTTP launch was denied by the execution environment and was not bypassed; this check does not establish that an HTTP server is currently running. [17]

## Q3 Retrieval improvements and ranked evaluation

### Improvement A Temporal eligibility

Improvement A excludes passages whose conservative `available_by` date exceeds the query cutoff. Missing availability fails closed. Month-only dates use month-end upper bounds rather than invented publication days. Filtering occurs before the ranked result set is selected, so later documents cannot occupy result slots and then disappear after ranking. [2][4]

This is an evidence-availability constraint, not a complete historical simulation of model knowledge. BM25 corpus statistics and the embedding index are constructed from the selected corpus, and model pretraining may contain other information. A zero future-evidence count therefore supports only the absence of post-cutoff passages in the returned evidence under the recorded metadata.

### Development and test protocol

Fifty initial development questions contain 16 factual, 14 temporal, 10 comparison and 10 evidence-sufficiency challenges. They use 37 documents across nine source classes and reserve 27 provisional development event groups. Seventy-three authoring anchors stay separate from annotation inputs, including eight future-leakage controls. The categories describe design intent rather than gold labels. Subsequent blinded machine runs assigned pooled qrels and reference points without changing the original question snapshot. [7][18]

All 50 questions ran in each retrieval mode at depth 10, producing 150 rankings and 1,500 returned hits. Their union contains 973 query-evidence pairs, with 13 to 27 passages per question and a mean of 19.46. Annotators saw no ranks, retrieval mode or authoring hints. Every returned hit has a known availability date no later than its cutoff. All original input, ranking and evidence hashes matched. The subsequently annotated pool can still omit relevant passages below the three top-10 lists. [12][18]

The final design targets 200 development records and 1,000 held-out records, split by conservative event families with legacy documents and aliases excluded. Source authoring and admission have produced 205 development questions, including the original 50. This is question coverage, not 205 completed paired/adjudicated records. Test authoring uses source paragraphs unchanged, with no more than two admitted, meaningfully different questions per paragraph. A separate augmentation prompt shows only previous question strings from that same paragraph, never answers or qrels, to seek another genuine research task. It preserves family splits and records rejects rather than padding counts. Semantic uniqueness and event independence remain unverified. [8][12][20]

Exact selection is now locked at 200 development and 1,000 TEST questions before test labeling; 18 unused questions remain as reserves, not post-label replacements. Their 7,200 actual top-five rankings cover three modes with temporal eligibility on/off. Annotators judge only the union of those six lists. Answerability is conditioned on this retrieved pool: a source-grounded question may remain insufficient if retrieval misses its source. Authoring anchors are not injected into the pool or supplied as gold. Fresh labels are required even for the original 50 questions because the evidence input has changed. At the latest clean transport-change boundary, 160 development records have both fresh annotations and 40 have source-based adjudication; no TEST native annotation has started. These progress counts are not a frozen evaluation result. [20]

An immutable seed-6127 uniform sample of 100 of the fixed 1,000 TEST identifiers was sealed before any TEST annotation. The plan binds the question/cohort files and pre/post-seal zero-TEST execution proofs. All 1,000 questions remain required for retrieval labeling and evaluation; answer generation and judging use only the same preselected 100 questions in each of six variants, for 600 planned variant answers. No label, ranking score or answer quality was used to select or replace those identifiers. [23]

### Metrics and current results

Ranked evaluation will report Precision@5, pooled Recall@5, MRR@5, nDCG@5 and the judged fraction of retrieved results. Relevance grades are 0 for irrelevant, 1 for useful background or partial support, and 2 for direct answer support. Recall is relative to the judged pool, not every potentially relevant passage in the corpus. Missing judgments must remain unjudged; any metric convention that treats unjudged hits as nonrelevant must be disclosed. [8][9]

| Retrieval mode | Precision@5 | Pooled Recall@5 | MRR@5 | nDCG@5 | Judged fraction |
|---|---|---|---|---|---|
| BM25 | Not measured | Not measured | Not measured | Not measured | Not measured |
| Dense | Not measured | Not measured | Not measured | Not measured | Not measured |
| Hybrid | Not measured | Not measured | Not measured | Not measured | Not measured |

The table above remains reserved for the full held-out evaluation. The complete 50-question DEVELOPMENT set is separately frozen as machine-only version `97dc75c680bee7fb2c3a9702`. Its measured development results are reported separately below. [18]

For comparison at the interface's default depth five, the same frozen development labels and original rankings give the following separate development scores. These are not values for the still-unfinished held-out table. [18]

| Development mode | Precision@5 | Pooled Recall@5 | MRR@5 | nDCG@5 | Judged fraction |
|---|---:|---:|---:|---:|---:|
| BM25 | 0.456 | 0.400 | 0.754 | 0.561 | 1.000 |
| Dense | 0.532 | 0.428 | 0.850 | 0.645 | 1.000 |
| Hybrid | 0.556 | 0.469 | 0.849 | 0.678 | 1.000 |

Depth-10 development scores preserve the original evaluation depth:

| Development mode | Precision@10 | Pooled Recall@10 | MRR@10 | nDCG@10 | Judged fraction |
|---|---:|---:|---:|---:|---:|
| BM25 | 0.388 | 0.606 | 0.762 | 0.601 | 1.000 |
| Dense | 0.470 | 0.661 | 0.853 | 0.694 | 1.000 |
| Hybrid | 0.468 | 0.691 | 0.849 | 0.729 | 1.000 |

Precision and MRR cover 50 questions. Recall and nDCG cover 49 with positive pooled judgments, excluding one zero-positive pool rather than assigning it artificial recall. Hybrid's higher pooled recall/nDCG accompanies slightly lower precision/MRR than dense retrieval, so the results do not show uniform superiority. Query-paired bootstrap intervals accompany the saved metric artifact. All scores depend on machine-adjudicated relevance, not human gold. [18]

An earlier segmentation candidate failed an unchanged 12-probe source-support comparison: BM25 improved from 4/12 to 6/12, while dense and hybrid each declined from 9/12 to 8/12. Its release gate rejected publication. This small exact-text diagnostic is not the table's formal ranked evaluation and does not establish the newer candidate's quality. The failure shows why increased passage count and successful indexing are insufficient reasons to release a corpus. [2]

## Q4 Evidence conditioned generation and quality assessment

### Generation method and preprocessing

RAG is used instead of fine-tuning because the task depends on inspectable documents, changing report versions and user-selected information cutoffs. Retrieval supplies the evidence explicitly, allowing the answer to cite passage identifiers and expose limits. The query prompt separates crude oil from total liquids, forecasts from reported observations, stock changes from flow rates, and legal announcements from physical production outcomes. Source text is treated as untrusted data rather than executable instructions. [10]

Lewis et al. (2020) combine a sequence generator with an explicit dense document index and fine-tune their RAG architecture. This coursework uses a frozen local retriever and a separately invoked generator instead; it does not reproduce joint RAG training. [24] The BGE author's model card specifies a 384-dimensional English encoder with a 512-token sequence limit. Its cached local execution supports a reproducible, modest-resource implementation, not a claim to current leaderboard superiority. [27] Self-RAG learns special tokens for retrieval decisions and generation critique; Improvement B instead uses a separate prompted source-checking pass, with no learned reflection tokens or adaptive retrieval policy. [26] These are representative research reference points, not an exhaustive survey of the current state of the art. A and B are application-specific controls whose benefit must come from this project's paired experiments; no competitive state-of-the-art QA result is claimed.

The generator returns an answerability decision, atomic claims with citations and limitations. The native Codex path also requires exact source quotations for cited claims and rejects structurally inconsistent responses; the historical API path removes invalidly cited claims. If eligible evidence is empty, the system states that no evidence was found. Extractive preview remains available without a generator: selected source sentences rather than a synthesized or verified answer. It does not itself establish whether the question is answerable. Evidence-insufficient output may quote eligible background but must not invent supported answer points. [10][17]

### Improvement B Claim support checking

Improvement B gives each generated claim and its cited passages to a separate verifier execution. The verifier checks facts, numbers, dates and units; unsupported claims are removed, and the answer may be marked incomplete. The historical API implementation and configuration used `deepseek-flash` for both generation and verification. Those legacy calls do not verify the pending Codex-only experiment workflow. Actual generator and verifier identities must be recorded for the final runs. Separate executions of the same model can share errors. In extractive-preview mode, B checks literal quotation existence only; that setting cannot demonstrate improved semantic faithfulness. [3][10]

### Machine annotation and agreement

The instructor-approved substitution is reported as machine annotation, based on the student's stated approval. The original brief's manual-labeling and human-agreement language remains recorded in the acceptance checklist. The student has replaced the planned Codex/DeepSeek pairing with an all-Codex workflow. Two separate blinded Codex executions receive the same fixed evidence and annotation rules, without authoring answers, prior labels or each other's outputs. Requested and observed model identifiers are recorded; an undisclosed model version is not invented. Agreement is computed on the original outputs before a separate adjudication pass. Separate contexts may use the same model, so this measures agreement between blinded executions, not distinct-model diversity or independent-human agreement.

The archive's 100 older QA records and 4,500 passage metadata labels are separate units and versions, not the new held-out set. The initial development experiment now has 50 outputs in each blinded stream, with no missing qrels or conflicting execution contexts. Before adjudication, answerability agrees 47/50 and event status 47/50. Evidence grades agree 912/973. Fifty subsequent source-based adjudications are accepted in the separate development version. Human-label coverage remains zero. [3][8][18]

| Machine field | Raw agreement | Cohen's kappa | Quadratic weighted kappa |
|---|---:|---:|---:|
| Answerability | 94.00% | 0.881 | 0.952 |
| Event status | 94.00% | 0.909 | Not applicable |
| Evidence relevance | 93.73% | 0.883 | 0.937 |

These are categorical agreement measures between fresh machine contexts. They are not human agreement, factual accuracy or distinct-model diversity. Native metadata did not expose either model identity. The manifest reports `same_requested_model_unverified`, retaining the unresolved default alias. Semantic agreement of free-text answers remains unmeasured rather than using literal wording equality. [18]

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

A separate local concurrency diagnostic runs the first 24 fixed development queries at depth five with temporal filtering. Each timed query performs its own embedding; a shared encoder lock serializes encoder calls. Ranked IDs match across worker conditions. This is a warm, shared-process retrieval burst, not an HTTP load test or concurrent answer-generation capacity. [22]

| Retrieval workers | Worker median seconds | Worker p95 seconds | Queries per wall second |
|---|---:|---:|---:|
| 1 | 0.172091 | 0.206806 | 5.807743 |
| 2 | 0.289578 | 0.364293 | 6.960314 |
| 4 | 0.574690 | 0.692015 | 6.614083 |

The host reports eight logical CPUs, four encoder threads, Windows 11 and Python 3.12.13. Throughput peaks at two workers in this bounded sample; increasing to four does not produce linear scaling. Executor-queue and retrieval-worker durations are stored separately. Sequential condition order and background activity can affect results, so no statistical scaling claim is made. All 43 protected inputs are unchanged and no native or hosted model call is made by this diagnostic. [22]

## Q5 Downstream improvements and ablations

The two implemented innovations address different failure modes. A limits the evidence to material available at the requested cutoff; B removes generated claims that the cited evidence does not support. Their combined benefit is a hypothesis to test, not an inference from operational checks.

The student has explicitly selected full retrieval evaluation on 1,000 TEST questions and answer-generation/ablation evaluation on a fixed uniform sample of 100 TEST questions, and reports instructor approval for this narrower answer-evaluation scope. The sample uses seed 6127 and is locked before any test labels or scores are inspected. This changes answer-experiment coverage, not the 1,000 accepted-label freeze requirement. Sampling and finite-sample uncertainty must be disclosed; 100 answer cases must not be reported as 1,000 measured answers. Approval is based on the student's direct statement, not an independently inspected course document.

The answer ablation compares hybrid base, A only, B only and A plus B on the identical frozen corpus and the same 100 sampled questions, with the same requested generator configuration, retrieval parameters, prompts and scoring protocol. Keyword and dense answer baselines use that same sample, giving six variants and 600 planned evaluated answers. Actual model identity can remain unavailable. Generator randomness and supported decoding controls must be recorded. A's temporal-error effect should be examined alongside relevance and evidence sufficiency, and B's faithfulness effect alongside removed claims, answer completeness, additional latency and cost. [9][10]

| Variant | A | B | Quality and citation results | Temporal errors | Latency and cost |
|---|---|---|---|---|---|
| Hybrid base | Off | Off | Not measured | Not measured | Not measured |
| Hybrid A | On | Off | Not measured | Not measured | Not measured |
| Hybrid B | Off | On | Not measured | Not measured | Not measured |
| Hybrid A plus B | On | On | Not measured | Not measured | Not measured |

No full held-out ablation currently supports an improvement claim. A separate, predetermined five-development-case pilot completed four generation batches and 30 evaluated variant answers. B reuses the exact base answer and A+B the exact A answer, avoiding a regeneration confound. Two fresh support-check batches and one machine-judge batch complete seven successful executions. A schema-interface repair reused the four saved generator responses after verifying exact original input/output bytes, not generating more favorable answers. [19]

| Five-case variant | Automatic correctness | Automatic context precision | Future retrieved passages | Ineligible citations |
|---|---:|---:|---:|---:|
| Hybrid base | 1.000 | 0.440 | 6 | 0 |
| Hybrid A | 1.000 | 0.600 | 0 | 0 |
| Hybrid B | 1.000 | 0.440 | 6 | 0 |
| Hybrid A+B | 1.000 | 0.600 | 0 | 0 |

All automatic answer correctness, relevance and support scores reach a ceiling of 1.000 in this tiny sample. B removes zero claims, so it demonstrates the checking path but provides no measured B benefit. A removes six returned post-cutoff passages in these cases, while all variants already have zero ineligible claim citations. A zero future-evidence count does not establish broader correctness. The combined judge, references and generator may share errors and lack human calibration. [19]

The seven successful executions emit 335,130 input and 11,606 output tokens. The recovery stage takes 128.772097 seconds, excluding the original generator execution time. Batched per-query generation and total latencies remain null, not a divided average. Failed schema and quota attempts remain archived with unknown usage where no usage event was emitted. Subscription dollar cost is unknown; the hosted API ledger did not change. [19]

## Validity limitations and failure analysis

Real failures informed the corpus rules. Survey excerpts sometimes lost the year supplied by an adjacent question; PDF continuations began mid-sentence; a large offshore report mixed public comments with government responses; bibliography titles reappeared after deduplication changed. Uniform source rules corrected or quarantined these cases while preserving original failures. Conservative reference-page quarantine also removed some useful mixed-page body text, a disclosed trade-off rather than an invisible repair. [2]

The legacy paragraph review retained 256 unresolved source checks and 200 overlapping advisory strict-evaluation exclusions. These are not 256 confirmed crude-answer errors or an error-rate estimate. They include source-version, statistical-scope and extraction uncertainty. Crude plus condensate, total liquids, refinery input, stocks and daily rates remain distinct quantities; no missing table columns should be reconstructed by the model. [3][8]

Source coverage is uneven, OPEC access is restricted, and tables are conservatively excluded when layout cannot be trusted. Near-duplicate checking is not exhaustive. Availability metadata cannot prove that every downloaded file is the exact historical version. The English embedding model's Chinese-query quality is unverified, so formal questions use English. Model-generated questions and shared annotation or judging models can bias the benchmark toward the system and overlook shared mistakes. These limitations qualify the eventual scores even if all mechanical checks pass.

Passage construction measures words, not model tokens. The English BGE encoder truncates at its context limit, so unusually long passages need not be represented in full by their embeddings; the complete source text is nevertheless retained for annotation, generation and inspection. The local retrieval receipt already records this limitation. No corpus-wide truncation rate has been measured, and no tokenizer/index change is made after TEST labeling begins. [12][27]

## Reproducibility and submission status

Code, tests, locked dependencies, configuration and aggregate receipts are published in the [repository](https://github.com/8309/6127NLP); newer local additions still require publication. The sampled-scope full engineering-suite checkpoint passes 2,046 tests with zero failures and three documented skips: two Windows symlink permissions and one excluded local PDF fixture. Later wire-driver and historical-pipeline additions have separate targeted checks and are not certified by that earlier checkpoint. The original English publication's 1,415 tests, canonical source-closeout's 1,171 tests and index suite's 268 tests are different snapshots and must not be combined into a total. Engineering tests do not measure RAG accuracy. [1][6][21]

Historical corpus receipts bind the canonical implementation, while the English publication has separate test receipts. Exact historical replay requires the matching local originals, caches, model and source snapshots; a clean clone with no data cannot reproduce the corpus simply by running fixture tests. The default library, old labels and ledgers remain separate from the unpublished staging version. [6][11]

The final submission must replace this draft with a checked PDF named for the group, supply valid data and result links with suitable permissions, and include source/library/README archives and a demonstrable presentation. Identity fields, redistribution clearance, the 1,000-record evaluated retrieval set, 100-case answer experiments and final artifact links remain incomplete. See [the submission checklist](SUBMISSION_CHECKLIST.md) for the actual package state.

A separate official-policy rights preflight retains all corpus text locally and produces a metadata-only source-registry ZIP. It identifies conditional candidates and unresolved document/component checks, not automatic export clearance. The registry includes URLs, identifiers and hashes, not the corpus bodies required for offline replay. Source-family rules and exceptions remain in [DATA_RIGHTS.md](DATA_RIGHTS.md); no raw-data public upload or legal clearance is claimed.

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
16. Retained local five-query demonstration: `data/machine_runs/coursework-demo/2026-10-13T00-37-20.834578+00-00-50342469/result.json`, SHA-256 `e06c5014238183549af92295d6e2167cd922be2db4371f506f4f123a82d6de5f`. [Execution implementation](../scripts/run_coursework_demo.py). The saved HTML, five traces and original batch response are local, not public data links.
17. Retained local actual Streamlit query: `data/machine_runs/workbench_queries/2026-10-13T01-05-21.647873+00-00-56c414dd/ui-check.json`; query result SHA-256 `fae952014496c4c2b5cd02aa3dc74ce069635e8e1985d29b76f5a2bfffa23f26`. [Native runtime implementation](../src/oil_evidence/codex_runtime.py) and [read-only staging launcher](../scripts/start_codex_workbench.py).
18. Local machine-only development version `data/machine_runs/frozen_development/97dc75c680bee7fb2c3a9702/manifest.json` and `retrieval-metrics-at10.json`. The separate depth-five derivative is `data/machine_runs/derived_retrieval/dev50-k5-126a7dfc7757/retrieval-metrics-at5.json`, SHA-256 `bd680be437ad9ad6633a92cf4aaa2f585379306d46fd5d0b1421e42d6bb9d10b`. [Ranked scoring](../scripts/report_machine_retrieval.py) and [machine metrics](../src/oil_evidence/machine_metrics.py). This contains 50 development records, not 1,000 test records or human gold. All original protocol, runtime and ranking input hashes are reverified; the old depth-10 artifact is unchanged.
19. Local five-case ablation receipt: `data/machine_runs/ablations/2026-10-13T01-38-07.663209+00-00-94744afd/result.json`, SHA-256 `cecca5dd3cce5be5725bac3055563e257594094ae0de8886bd72cde3c76220c5`. [Native paired pilot](../scripts/run_codex_ablations.py). Four verified original generator batches plus three fresh support/judge calls, not seven newly generated batches.
20. [Source-first cohort selection](../scripts/prepare_machine_cohort.py) and [actual admission aggregation](../scripts/aggregate_machine_questions.py). Local source/augmentation receipts preserve family reservations and rejected candidates, not proof of independently verified semantic uniqueness.
21. Sampled-scope checkpoint suite receipt `tmp/assignment-sampled-scope-tests.xml`: 2,046 passed, 3 skipped, 0 failures, 306.24 seconds. This ignored local JUnit artifact is not a public dataset or a later-code certification.
22. Local concurrency diagnostic `data/machine_runs/local-retrieval-benchmarks/2026-10-13T02-34-17.879497+00-00-296c7b8f/result.json`, SHA-256 `9600fff888a99c8a6a23ef0a942df25f42ed87dd016da22c7fa66fc0b5e3df44`. [Execution implementation](../scripts/benchmark_local_retrieval.py). Seventy-two timed retrieval queries, no generated answers or HTTP requests.
23. Immutable pre-label answer sample `data/machine_runs/answer-samples/2026-10-13T03-10-54.055066+00-00-94340f33/sample_plan.json`, SHA-256 `079d484d1100f4a62dd9c687f1a0d575bd92bcc87694c58970ab3de84d1f4baf`. [Sampler implementation](../scripts/prepare_answer_sample.py). Exactly 100 TEST questions from the fixed 1,000, seed 6127; this artifact records sampling, not completed answers or measured quality.
24. Lewis, P. et al. (2020). [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401). NeurIPS 2020.
25. Cormack, G. V., Clarke, C. L. A., and Buttcher, S. (2009). [Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf). SIGIR 2009, pp. 758-759.
26. Asai, A. et al. (2024). [Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection](https://arxiv.org/abs/2310.11511). ICLR 2024; original preprint 2023.
27. BAAI. [bge-small-en-v1.5 author model card](https://huggingface.co/BAAI/bge-small-en-v1.5), accessed 13 October 2026. Its historical general-domain benchmark table is not this coursework's oil-QA evaluation.

The final source registry should supply the remaining exact official document URLs, archive hashes and redistribution decisions. The three document examples above do not provide a complete redistributable data package.
