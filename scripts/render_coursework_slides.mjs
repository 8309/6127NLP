/** English academic deck from hash-bound local receipts, never API calls.
 * Run a mechanical copy inside an ignored build folder whose node_modules
 * junction points at the documented bundled runtime. Sources remain read-only.
 * Set RUNTIME_NODE_MODULES to that same bundled path for finalizer subprocesses.
 * Finalization runs without raster rendering. Use the skill's separate renderer
 * for preview PNGs so a native raster teardown fault cannot hide export status.
 * The presentation-operation marker belongs to the parent task and runs once.
 */
import fs from 'node:fs/promises';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { pathToFileURL } from 'node:url';
import { Presentation, PresentationFile, FileBlob } from '@oai/artifact-tool';

if (!process.env.RUNTIME_NODE_MODULES) throw new Error('Set the documented bundled RUNTIME_NODE_MODULES for validation');

const args = {};
for (let index = 2; index < process.argv.length; index += 2) {
  const key = process.argv[index];
  if (!key?.startsWith('--') || !process.argv[index + 1]) throw new Error('Use named argument/value pairs');
  args[key.slice(2)] = process.argv[index + 1];
}
for (const key of ['workspace', 'build-dir', 'source-config', 'skill-dir', 'runtime-python']) {
  if (!args[key]) throw new Error(`Missing --${key}`);
}
const workspaceDir = path.resolve(args.workspace);
const buildDir = path.resolve(args['build-dir']);
const skillDir = path.resolve(args['skill-dir']);
const finalPath = path.resolve(args['final-path'] ?? path.join(workspaceDir, 'output/pptx/oil-evidence-presentation-draft-v1.pptx'));
if (!buildDir.startsWith(workspaceDir + path.sep) || !finalPath.startsWith(workspaceDir + path.sep)) {
  throw new Error('Keep build and deliverable inside the task workspace');
}
const utils = await import(pathToFileURL(path.join(skillDir, 'container_tools/artifact_tool_utils.mjs')).href);
const font = utils.resolvePresentationFont({fontFamily: 'Arial', availableFonts: ['Arial']});
const sources = JSON.parse(await fs.readFile(args['source-config'], 'utf8'));
const hashes = {};
async function readSource(key, required = true) {
  if (!sources[key]) {
    if (required) throw new Error(`Missing actual source ${key}`);
    return null;
  }
  const file = path.resolve(sources[key]);
  if (/auth|credential|api[_-]?key|\.env(?:\.|$)/i.test(path.basename(file))) throw new Error('Refuse credential-like source');
  const bytes = await fs.readFile(file);
  hashes[file] = createHash('sha256').update(bytes).digest('hex');
  return JSON.parse(bytes);
}
const corpus = await readSource('corpus_report');
const quality = await readSource('quality_report');
const retrieval = await readSource('retrieval_receipt');
const agreement = await readSource('agreement_receipt');
const ui = await readSource('workbench_receipt');
const uiResult = await readSource('workbench_result');
const metrics = await readSource('retrieval_metrics', args['draft-only'] !== 'true');
const ablation = await readSource('ablation_result', args['draft-only'] !== 'true');
if (corpus.passages !== 11815 || agreement.paired_records !== 50 || retrieval.retrieval_runs !== 150
    || quality.exact_source_offsets !== true || ui.no_api_key_input !== true) {
  throw new Error('Source coverage differs from the requested draft');
}
if (metrics && (metrics.questions !== 50 || metrics.ranked_runs !== 150 || metrics.k !== 10 || metrics.formal_heldout_test !== false)) {
  throw new Error('Only the actual complete 50-question development result belongs in this draft');
}
if (ablation && (ablation.questions !== 5 || ablation.status !== 'completed_development_pilot_not_formal_heldout_experiment')) {
  throw new Error('Use the actual complete five-case pilot, never inferred experiment results');
}
await fs.mkdir(buildDir, {recursive: true});
await fs.mkdir(path.dirname(finalPath), {recursive: true});
const presentation = Presentation.create({slideSize: {width: 1280, height: 720}});
presentation.theme.defaultFont = font;
const color = {ink: '#172C3B', muted: '#4D606C', accent: '#184E6A', grid: '#CFD9DF'};
const nativeTables = [];
const nativeCharts = [];
const slideText = [];
const sourceNote = (...keys) => keys.filter(key => sources[key]).map(key => {
  const file = path.resolve(sources[key]);
  return `${key}: ${file}\nSHA256: ${hashes[file]}`;
}).join('\n\n');
const fmt = (value, digits = 3) => value === null || value === undefined ? 'Undefined' : Number(value).toFixed(digits);
const pct = (value, digits = 2) => value === null || value === undefined ? 'Undefined' : `${(100 * value).toFixed(digits)}%`;
const num = value => Number(value).toLocaleString('en-US');
function text(slide, value, x, y, w, h, size = 28, bold = false, fill = color.ink) {
  const shape = slide.shapes.add({geometry: 'textbox', position: {left: x, top: y, width: w, height: h},
    fill: 'none', line: {style: 'solid', fill: 'none', width: 0}});
  shape.text = value;
  shape.text.style = {typeface: font, fontSize: size, bold, color: fill, autoFit: 'none', wrap: 'square', insets: 0};
  slideText.push(value);
  return shape;
}
function page(title, notes, footer = 'Development draft') {
  const slide = presentation.slides.add();
  slide.background.fill = '#FFFFFF';
  text(slide, title, 72, 52, 1136, 96, 44, true);
  text(slide, `${footer}     ${presentation.slides.items.length}/12`, 72, 669, 1136, 28, 24, false, color.muted);
  slide.speakerNotes.text = notes;
  return slide;
}
function table(slide, values, top, height, widths, size = 26) {
  const tab = slide.tables.add({rows: values.length, columns: values[0].length, left: 72, top,
    width: 1136, height, values, columnWidths: widths});
  tab.styleOptions = {headerRow: true, bandedRows: false};
  tab.borders.assign({style: 'solid', fill: color.grid, width: 1});
  tab.cells.block({row: 0, column: 0, rowCount: values.length, columnCount: values[0].length}).assign({
    fill: '#FFFFFF', textStyle: {typeface: font, fontSize: size, color: color.ink},
    margins: {left: 12, right: 12, top: size <= 25 ? 4 : 8, bottom: size <= 25 ? 4 : 8}, anchor: 'center'});
  for (let col = 0; col < values[0].length; col++) {
    tab.getCell(0, col).text.style = {typeface: font, fontSize: size, bold: true, color: color.accent};
  }
  nativeTables.push(presentation.slides.items.length);
  return tab;
}
function paragraphs(slide, items, top = 184, fontSize = 30) {
  const shape = text(slide, '', 72, top, 1136, 650 - top, fontSize);
  shape.text = utils.makeNativeBulletParagraphs(items, {marginLeftPoints: 20, hangingPoints: 10, spaceAfterPoints: 18});
  shape.text.style = {typeface: font, fontSize, color: color.ink, autoFit: 'none', insets: 0};
  slideText.push(...items);
}

// 1. Plain cover. Requested identity blanks remain intentionally unfilled.
{
  const slide = presentation.slides.add();
  slide.background.fill = '#FFFFFF';
  text(slide, 'Oil Evidence', 72, 110, 1136, 110, 72, true);
  text(slide, 'Evidence-grounded question answering for crude oil research', 72, 245, 1110, 100, 34);
  text(slide, 'AI6127 NLP assignment', 72, 370, 1110, 54, 30, false, color.muted);
  text(slide, 'Group: __________     Name: __________     Matriculation: __________', 72, 472, 1136, 80, 26);
  text(slide, 'DRAFT', 72, 622, 1136, 40, 26, true, color.accent);
  slide.speakerNotes.text = 'English academic draft. User requested blank group, name and matriculation fields. '
    + 'The user reports instructor approval for solo completion and model-assisted annotation. '
    + 'No written course-side approval artifact has been inspected.';
}
// 2. Scope and the query date.
{
  const slide = page('Research question and cutoff date', sourceNote('retrieval_receipt'));
  text(slide, 'What evidence available by a chosen date supports an answer about crude oil supply?', 72, 184, 1110, 132, 36, true);
  paragraphs(slide, ['Scope covers supply disruptions, production policy, sanctions and transport events.',
    'Each query includes a cutoff date and an optional region filter.',
    'Answers cite source passages and disclose insufficient evidence.'], 353, 30);
}
// 3. Original unified corpus statistics.
{
  const slide = page('Corpus coverage', sourceNote('corpus_report', 'quality_report'));
  table(slide, [['Measure', 'Verified staging corpus'], ['Evidence passages', num(corpus.passages)],
    ['Words', num(corpus.words)], ['Unique word types', num(corpus.unique_words)],
    ['Source documents', num(corpus.documents)], ['Source pages', num(corpus.source_pages)]], 176, 390, [620, 516], 30);
  text(slide, 'Official sources include EIA, Treasury, DOE, BSEE and BOEM.', 72, 599, 1136, 50, 26, false, color.muted);
}
// 4. Same policy, variable passage length.
{
  const slide = page('Uniform segmentation and provenance', sourceNote('corpus_report', 'quality_report'));
  const policy = corpus.chunk_policy;
  table(slide, [['Policy', 'Words', 'Role'], ['Target passage length', String(policy.target_words), 'Preferred length'],
    ['Minimum passage length', String(policy.minimum_words), 'Soft bound'],
    ['Maximum passage length', String(policy.maximum_words), 'Soft bound'],
    ['Maximum contextual span', String(policy.maximum_context_words), 'Context cap']], 173, 330, [506, 180, 450], 28);
  text(slide, 'Sentence boundaries and local context govern exceptions.', 72, 537, 1136, 45, 28);
  text(slide, 'Every selected staging passage retains its source page and exact native offsets.', 72, 595, 1136, 52, 28);
}
// 5. Native editable method comparison.
{
  const slide = page('Keyword, dense and hybrid retrieval', sourceNote('retrieval_receipt'));
  table(slide, [['Method', 'Representation', 'Ranking'], ['BM25', 'Keyword statistics', 'Lexical relevance'],
    ['Dense', `${retrieval.embedding_model}\n${retrieval.index_dimension} dimensions`, 'Vector similarity'],
    ['Hybrid', 'BM25 and dense candidates', 'Reciprocal rank fusion']], 176, 305, [255, 540, 341], 28);
  text(slide, 'RRF score(d) = sum 1 / (60 + rank_m(d))', 72, 526, 1136, 65, 32, true);
  text(slide, 'The union of three top-10 lists creates an unranked annotation pool.', 72, 605, 1136, 48, 26);
}
// 6. Innovation A.
{
  const slide = page('A: Evidence available by the cutoff', sourceNote('retrieval_receipt', 'corpus_report'));
  text(slide, 'available_by <= query cutoff', 72, 177, 1136, 75, 40, true, color.accent);
  paragraphs(slide, ['Retrieval filters sources using publication availability, not the event date alone.',
    'Month and year precision use conservative upper bounds.',
    'Undated or future evidence cannot support a positive annotation or a quoted answer.',
    'An earlier-than-corpus control returns zero results in all three modes.'], 290, 29);
}
// 7. Actual raw pre-adjudication agreement.
{
  const slide = page('Machine annotation agreement', sourceNote('agreement_receipt'));
  table(slide, [['Field', 'Judgment pairs', 'Raw agreement', 'Cohen kappa'],
    ['Answerability', '50', pct(agreement.fields.answerability.raw_agreement), fmt(agreement.fields.answerability.cohens_kappa)],
    ['Event status', '50', pct(agreement.fields.event_status.raw_agreement), fmt(agreement.fields.event_status.cohens_kappa)],
    ['Evidence relevance', '973', pct(agreement.fields.relevance.raw_agreement), fmt(agreement.fields.relevance.cohens_kappa)]],
    180, 285, [380, 245, 265, 246], 28);
  text(slide, 'Two annotation runs use fresh contexts with identical input bytes.', 72, 511, 1136, 47, 28);
  text(slide, 'Native metadata does not expose the model identity. Human agreement remains unmeasured.',
    72, 571, 1136, 74, 27, false, color.muted);
}
// 8. Measured latency and machine-adjudicated pooled retrieval quality.
{
  const slide = page('Retrieval on 50 development questions', sourceNote('retrieval_receipt', 'retrieval_metrics'));
  const modes = ['bm25', 'dense', 'hybrid'];
  const chart = slide.charts.add('bar', {position: {left: 74, top: 155, width: 1132, height: 286},
    title: 'Warm retrieval latency (milliseconds)', titleTextStyle: {fontSize: 26, bold: true, fill: color.ink},
    categories: ['BM25', 'Dense', 'Hybrid'], series: [
      {name: 'Median', values: modes.map(mode => Math.round(retrieval.latency[mode].median_seconds * 10000) / 10), fill: color.accent},
      {name: 'P95', values: modes.map(mode => Math.round(retrieval.latency[mode].p95_seconds * 10000) / 10), fill: '#92ACBC'}],
    barOptions: {direction: 'column', grouping: 'clustered', gapWidth: 140}, hasLegend: true,
    legend: {position: 'bottom', textStyle: {fontSize: 24}},
    xAxis: {textStyle: {fontSize: 24}, majorGridlines: null},
    yAxis: {min: 0, max: 350, majorUnit: 100, numberFormatCode: '0', textStyle: {fontSize: 24},
      majorGridlines: {style: 'solid', fill: color.grid, width: 1}},
    dataLabels: {showValue: true, position: 'outEnd', numberFormatCode: '0.0', textStyle: {fontSize: 24}},
    chartFill: '#FFFFFF', plotAreaFill: '#FFFFFF'});
  utils.applyPresentationChartFont(chart, {fontFamily: font});
  nativeCharts.push(8);
  if (metrics) {
    table(slide, [['Mode', 'P@10', 'Pool R@10', 'MRR@10', 'nDCG@10'], ...modes.map(mode => [
      mode === 'bm25' ? 'BM25' : mode[0].toUpperCase() + mode.slice(1),
      ...['precision_at_k', 'pooled_recall_at_k', 'mrr_at_k', 'ndcg_at_k'].map(key => fmt(metrics.summary[mode][key]))])],
      445, 160, [232, 200, 260, 212, 232], 24);
  } else {
    text(slide, 'Relevance metrics await complete machine adjudication.', 72, 485, 1136, 88, 30);
  }
  text(slide, 'Pool-relative machine scores. Recall and nDCG cover 49 questions with positive evidence.',
    72, 629, 1136, 37, 24, false, color.muted);
  slide.speakerNotes.text += '\nLatency chart uses the original operational receipt and its linear-percentile P95. '
    + 'The derived retrieval report uses nearest-rank P95. Recall and nDCG exclude the one zero-positive evidence pool.';
  slide.speakerNotes.text += '\nNew literal chart values round to the displayed 0.1 millisecond precision for a portable workbook. '
    + 'The unrounded measurements remain in the hash-bound source receipt.';
}
// 9. Actual tested application output, without inventing a browser screenshot.
{
  const slide = page('Streamlit query smoke test', sourceNote('workbench_receipt', 'workbench_result'));
  text(slide, uiResult.question, 72, 178, 1136, 100, 31, true);
  table(slide, [['Observed result', 'One actual Codex query'], ['Retrieved evidence', String(ui.evidence)],
    ['Answer claims', String(ui.claims)], ['Exact quotations', String(ui.quotes)],
    ['End-to-end elapsed time', `${ui.total_seconds.toFixed(3)} seconds`]], 299, 270, [620, 516], 28);
  text(slide, 'No API-key input. AppTest confirms execution. Live browser HTTP behavior remains unverified.',
    72, 599, 1136, 62, 25, false, color.muted);
}
// 10. Actual diagnostic ablation only.
{
  const slide = page('A and B: Five-case diagnostic pilot', sourceNote('ablation_result'));
  if (ablation) {
    const keys = ['hybrid_base', 'hybrid_A', 'hybrid_B', 'hybrid_AB'];
    const names = ['Base', 'A: cutoff', 'B: verification', 'A + B'];
    table(slide, [['Variant', 'Machine\ncorrectness', 'Context\nprecision', 'Future\nhits', 'Ineligible\ncitations'],
      ...keys.map((key, index) => {
        const result = ablation.summary[key];
        return [names[index], pct(result.automatic_correctness), pct(result.automatic_context_precision),
          String(result.future_evidence_count), String(result.ineligible_citation_count)];
      })], 177, 340, [240, 250, 220, 180, 246], 25);
    text(slide, 'All automatic answer scores reach 1.00 in this pilot, creating a ceiling.', 72, 550, 1136, 45, 27);
    text(slide, 'Five predetermined cases and automatic judges cannot establish formal generalization gains.',
      72, 606, 1136, 57, 25, false, color.muted);
  } else {
    paragraphs(slide, ['A constrains retrieval by source availability.', 'B checks answer claims against their evidence.',
      'Actual pilot results are pending. This draft makes no measured gain claim.'], 190, 31);
  }
}
// 11. Evidence-grounded failures and limits.
{
  const futureCount = ablation?.summary?.hybrid_base?.future_evidence_count;
  const slide = page('Failure cases and unresolved risks', sourceNote('ablation_result', 'workbench_result', 'agreement_receipt'));
  table(slide, [['Case', 'Observed issue or tested risk', 'Current response'],
    ['Future evidence', futureCount === undefined ? 'Future-source leakage control' : `${futureCount} future hits in the base pilot`, 'A filters availability'],
    ['Policy effects', 'A notice alone cannot establish physical supply effects', 'Declare insufficient evidence'],
    ['Statistical units', 'Crude oil and total liquids cover different products', 'Keep product scope and units'],
    ['Latest forecast', 'The UI query retrieved 2018 and 2019 outlooks', 'Latest-report relevance remains unresolved']],
    176, 438, [240, 540, 356], 25);
  text(slide, 'Exact quotes and dates verify format. Semantic support still needs evaluation.',
    72, 624, 1136, 40, 24, false, color.muted);
}
// 12. Honest final coverage statement.
{
  const slide = page('Evaluation coverage and limitations', sourceNote('agreement_receipt', 'retrieval_metrics', 'ablation_result'), 'Development draft');
  paragraphs(slide, ['Completed: 50 development questions, 100 independent-context annotations and 150 retrieval runs.',
    'The target of 1,000 formal held-out test records remains incomplete.',
    'Model identity and human calibration remain unverified. Machine errors may be correlated.',
    'The user reports instructor approval for solo work and model annotation.',
    'Group, name and matriculation fields remain blank for the final cover.'], 184, 29);
  slide.speakerNotes.text += '\nApproval source: direct user statement in the task, not an independently inspected course document. '
    + 'Machine agreement is not accuracy, and the development pilot is not a formal held-out result.';
}
if (presentation.slides.items.length !== 12) throw new Error('Expected exactly 12 slides including cover');
const candidatePath = path.join(buildDir, 'candidate.pptx');
await (await PresentationFile.exportPptx(presentation)).save(candidatePath);
console.log(JSON.stringify({phase: 'draft_exported', nodeExitCode: process.exitCode ?? 0}));
await fs.writeFile(path.join(buildDir, 'source-bindings.json'), JSON.stringify({sources, hashes, font, slideCount: 12}, null, 2));
await fs.writeFile(path.join(buildDir, 'slide-text.json'), JSON.stringify(slideText, null, 2));
if (args['draft-only'] === 'true') {
  for (const [index, slide] of presentation.slides.items.entries()) {
    const blob = await presentation.export({slide, format: 'png', scale: 1});
    await fs.writeFile(path.join(buildDir, `draft-slide-${String(index + 1).padStart(2, '0')}.png`), new Uint8Array(await blob.arrayBuffer()));
  }
  console.log(JSON.stringify({candidatePath, slideCount: 12, finalized: false, nodeExitCode: process.exitCode ?? 0}));
} else {
  const validation = await utils.finalizePresentation({workspaceDir, candidatePath, finalPath,
    pythonExecutable: path.resolve(args['runtime-python']),
    integrityValidatorPath: path.join(skillDir, 'container_tools/inspect_presentation_package_integrity.py'),
    layoutValidatorPath: path.join(skillDir, 'container_tools/inspect_presentation_layout_geometry.py'),
    layoutArgs: ['--expected-slide-size-emu', '12192000,6858000', '--validate-bullet-geometry', '--validate-heading-fit',
      ...nativeTables.flatMap(slide => ['--require-native-table-slide', String(slide)])],
    explicitTotalSlideCount: 12, requiredNativeTableOwnerSlides: nativeTables, requiredNativeChartOwnerSlides: nativeCharts,
    materializeLiteralChartWorkbooks: true, fontPolicy: {basis: 'design', families: [font]},
    verifyArtifactToolImport: true, receiptPath: path.join(buildDir, 'validation.json')});
  for (const [file, expected] of Object.entries(hashes)) {
    if (createHash('sha256').update(await fs.readFile(file)).digest('hex') !== expected) throw new Error('Source changed during export');
  }
  console.log(JSON.stringify({finalPath, slideCount: 12, rasterRendering: 'separate_skill_renderer', nodeExitCode: process.exitCode ?? 0, validation}));
}
