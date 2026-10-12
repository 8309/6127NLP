# Oil Evidence

原油供应、政策与运输事件的本地证据检索及人工标注工作台。工程进度见 [TASKS.md](TASKS.md)，课程验收见 [docs/ACCEPTANCE.md](docs/ACCEPTANCE.md)。

## GitHub 同步范围

本仓库同步实现代码、测试、配置、来源种子和进度文档。当前交接入口为 [GitHub 进度](docs/GITHUB_PROGRESS.md)，机器可读摘要为 [reports/progress.json](reports/progress.json)。原始 PDF/HTML、语料、提取缓存、标注、SQLite 账本、索引、模型文件及课程原始作业 PDF 不在此公开仓库中；下文 `data/` 路径指本地保存的产物。

克隆仓库后可安装依赖并运行基于固定测试样本的单元测试。精确重建历史语料、查询已有知识库和重放标注仍需要对应本地原件与冻结快照；GitHub 同步不等于发布完整数据包或完成课程验收。

**当前更新：本轮新增资料收尾完成，停止扩充；统一暂存库为 11,815 段、1,562,715 词，余量 18.15%。** 160/65/240/480 参数不变；按原 PDF 章节结构隔离评论/政府答复混列及参考文献，原件和失败记录保留。完整测试 1,171 通过、1 项主机权限跳过，最终逐字节来源重建审计通过；固定机器样本的已知严重问题已处置，警告保留，不代表全库或人工批准。默认旧库与标签未改，新库未构建索引或发布；历史 9,452 段混合检索 9/12→8/12 的发布拒绝仍保留。最后检查发现 8517 服务未监听，不声称网页当前可用；未擅自启动或切换服务。详见 [统一语料实施记录](docs/UNIFIED_CORPUS.md)。`oil build --run RUN` 只暂存，不直接覆盖默认库。

## Windows 启动

环境已安装后，可双击项目根目录的 `start-workbench.cmd`。使用期间保持该窗口打开；关闭窗口或按 Ctrl+C 会停止本地服务。浏览器显示“无法访问”时，先检查这个服务是否正在运行；浏览器标签本身不会启动后端。

在 `D:\coursework\AI6127\oil-evidence` 打开 PowerShell：

```powershell
uv sync --locked --group dev
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8517 --browser.gatherUsageStats false
```

浏览器访问 http://127.0.0.1:8517 。本项目固定使用自己的 `.venv`，由 `C:/Users/Jiang/.local/bin/python.exe` 创建；不依赖课程外的环境。`uv.lock` 固定依赖。

侧栏可不回显地输入 API 密钥，只供当前本机服务进程使用；也可以选择无 API 的原文预览。服务仅绑定 127.0.0.1，不要把这个无登录的本地工作台直接暴露到公网。

## 旧线上版本与历史可复现命令

2026-10-11 已发布合理重新切块版本：知识库为 **10,079 段、1,406,498 词、26,431 个唯一词**，来自 1,217 份贡献正文的文档；原始下载仍为 1,434 份。本轮没有新增源文档或导入 Hugging Face 数据，段数增长来自按完整句子划分，不是新增信息量。已达到 >=10,000 段及 >=100,000 词的数量要求；这不代表全库语义质量、人工标注、正式评估或作业整体已验收。当前主报告为 `data/reports/corpus_resegmentation.json`，不是历史 v2 的 `corpus_expansion.json`。

本轮将 2,030 个父段替换为 4,060 个无重叠、80–160 词的子段；父段仅在冻结版本和界面上下文中保留，不与子段重复计入索引。隔离 762 个原段：近重复候选涉及的 521 段、财务目录源待提取的 143 段、结构异常 81 段及明确问题 17 段，原文和排除原因未删除。保留内容的全部词序、精确字符偏移、来源、页码和日期不变；原 1,532,500 词减去隔离的 126,002 词，得到当前词数。

原 4,500 段标签、100 条问答和 728 条复核及其哈希未改写，仍读取原文版本。子段不继承父段标签。当前标签真实覆盖 **3,135 / 10,079**，另 6,944 段未逐段标注；页面明确区分旧版本标签存档和当前覆盖。新版本源文件、隔离记录、索引和检查报告冻结在 `data/resegmentation_runs/semantic-80-160-v1/published/<corpus_sha256>/`；8,811 段父版本位于该运行的 `baseline/`。原始标注版本仍在 v1 `baseline/`。

发布流程的历史执行记录如下，**不要对已发布 run 再次 stage/publish**。单写入器、来源/标注/哈希门禁、发布日志及异常回滚均已验证。后续版本必须明确保存标签原文和父子映射；不要直接用普通 `oil build` 或旧流程覆盖当前版本。

```powershell
# 本版的历史执行顺序：snapshot -> stage -> index -> audit --require-index -> publish
# 上述写入链已经完成；不要对 semantic-80-160-v1 再次运行 stage/audit/publish。
# 历史版本当时通过的重放命令；当前代码已改，需配套旧冻结实现，哈希不符会拒绝
.\.venv\Scripts\python.exe -X utf8 scripts/reproduce_resegmentation.py
# 当前版本的工作台与检索规则检查（无付费模型调用）
.\.venv\Scripts\python.exe -X utf8 scripts/check_workbench.py
.\.venv\Scripts\python.exe -X utf8 scripts/check_resegmentation_queries.py
```

实际重放通过，输出位于本运行的 `reproductions/<corpus_sha256>/`，语料和隔离记录与发布版字节相同。来源完整性、索引顺序与 384 维向量匹配；332 项测试通过、1 项因 Windows 符号链接权限跳过。30 次 BM25/向量/混合检索截止日和父子溯源检查通过，四个页签及父段展示通过。结果见 `data/reports/resegmentation_quality.json`、`resegmentation_queries.json`、`resegmentation_reproduction.json`、`workbench_checks.json`。固定机器抽查保留最初失败案例，撤销坏拆分；不是全库逐段人工语义审核。旧段的混合主题、部分截断、脚注和时间上界等局限仍需后续处理。本轮外部模型 API 调用和新人工标签均为 0；Codex 订阅消耗未计量。

### 历史第二批官方扩充（v2，8,811 段）

以下为 2026-10-10 的旧版执行记录，不能将其数量或报告当作当前状态。已有机器标签对应原始固定语料，不是扩充后全库的评估真值。

以下是本批执行链的记录，**已发布版本不要再次执行 `publish`**。只复现已下载语料及索引可从 `stage` 开始，结果写入本批 `stage/`，不改线上库。后续扩充须先使用新的 `--run` 名称创建当前库快照，不能复用 v1/v2 基线；默认 run 名称仅为旧流程兼容。

```powershell
.\.venv\Scripts\python.exe -X utf8 scripts/expand_corpus.py snapshot --run official-2018-2026-v2
.\.venv\Scripts\python.exe -X utf8 scripts/expand_corpus.py discover-extra --run official-2018-2026-v2
.\.venv\Scripts\python.exe -X utf8 scripts/expand_corpus.py discover-eia --run official-2018-2026-v2
.\.venv\Scripts\python.exe -X utf8 scripts/add_wb_observed.py
# 串行采集，各系列独立执行有上限的下载；不要启动并行写入器
.\.venv\Scripts\python.exe -X utf8 scripts/collect_expansion_batch.py --run official-2018-2026-v2 BSEE-HURRICANE DOE-SPR BOEM-POLICY AU-REQ UK-DUKES UK-ENERGY-TRENDS EIA-METHODS EIA-FINANCE EIA-IEO WB-CMO
.\.venv\Scripts\python.exe -X utf8 scripts/apply_source_page_exclusions.py
.\.venv\Scripts\python.exe -X utf8 scripts/validate_new_sources.py --run official-2018-2026-v2
.\.venv\Scripts\python.exe -X utf8 scripts/expand_corpus.py stage --run official-2018-2026-v2
.\.venv\Scripts\python.exe -X utf8 scripts/audit_expansion.py --run official-2018-2026-v2
.\.venv\Scripts\python.exe -X utf8 scripts/expand_corpus.py index --run official-2018-2026-v2
# 本批已执行一次并冻结；不要重发到线上
.\.venv\Scripts\python.exe -X utf8 scripts/expand_corpus.py publish --run official-2018-2026-v2
.\.venv\Scripts\python.exe -X utf8 scripts/check_workbench.py
.\.venv\Scripts\python.exe -X utf8 scripts/check_expansion_queries.py
```

`data/expansion_runs/official-2018-2026-v1/baseline/` 保存原 4,500 段标注语料；v2 的 `baseline/` 保存上一版 6,392 段和索引。每批 `published/<corpus_sha256>/` 保存该版本的语料、源清单、索引清单与质量报告，禁止不同内容覆盖。原 PDF/HTML 保留在 `data/raw/`。新发现网页会变化；冻结的本地原件和处理实现哈希才是版本复现依据。

本批新增美国战略石油储备、海上飓风停产、BOEM 政策/生产分析、英国能源统计、澳大利亚原油章节、EIA 原油模型方法/财务分析及世界银行 2025 年报告。方法报告只用于解释供给机制，不能作为已发生事件或实际产量证据。117 份新原件因历史版本时间不明被隔离，未通过改晚发布日期强行纳入；原件未删除。PDF 原页检查促成油章节限制、表格/字典/参考文献排除和年份保留修复。已有 OPEC 访问及批量使用限制未绕过；整库再分发、近重复裁决与人工抽查仍未验收。

```powershell
.\.venv\Scripts\oil.exe discover
.\.venv\Scripts\oil.exe collect --limit 6
# 当前 build 已改为统一暂存入口；选择新 run，不覆盖线上
.\.venv\Scripts\oil.exe build --run new-uniform-run
.\.venv\Scripts\oil.exe index
.\.venv\Scripts\oil.exe query "What factors affect crude oil supply and inventories?" --as-of 2026-08-01 --verify
.\.venv\Scripts\oil.exe pilot --limit 50
.\.venv\Scripts\oil.exe evaluate data/annotations/pilot.jsonl --smoke --limit 5
.\.venv\Scripts\oil.exe status
.\.venv\Scripts\python.exe -m pytest -q
```

上面的 discover/collect 是来源入口；当前 build 是统一暂存入口，已有标签的本库禁止自动继承旧标签或用旧增量流程混入旧块。例子里的 `new-uniform-run` 需替换为明确的新运行名称，并遵循统一流程的审核/比较/发布检查。`collect --limit N` 是新增 N 份，已下载且哈希一致的文件跳过。`pilot` 不覆盖已有审核队列。重新清洗会改变语料哈希，旧向量索引会拒绝加载，须重建。下载、模型、数据均在本目录，不写全局环境。

## 模型服务

当前已有 **100 条 Codex 机器标注**：50 条 Flash 候选核对、50 条原始试验题补齐。打开工作台的“标注核对”，默认选择“Codex 已完成”；可以只看已修正、证据不足或暂不建议进入正式评估的记录。中文核对说明、英文参考答案和原文引用分别显示，原始 JSON 折叠保留。

本批由当前 Codex 对话直接阅读固定证据后作出判断，没有调用外部 API；使用 Codex 订阅额度，具体额度消耗不由本程序计量。这不改变以下在线查询的 DeepSeek 配置。标签来源明确为 `codex_model_annotated`，不是人工真值，也不是第二位人工标注者。

结果为 `data/annotations/codex.jsonl`，不可覆盖的审计版本在 `data/annotations/codex_runs/`，统计见 `data/reports/codex_annotation.json`。`scripts/codex_labels.py` 可展示固定阅读材料和校验/发布已写好的决策；它本身不会调用 Codex、生成语义标签或把订阅转换成 API。原始 `pilot.jsonl`、`candidates.jsonl` 和人工审核历史保持独立。

用户已选择 DeepSeek V4.1 Flash（接口名 `deepseek-flash`）用于全部角色，费用上限 USD 5。没有本地进程密钥时，应用仍提供**原文摘录预览**，不冒充综合生成答案，不声称判断了可回答性。

`config.toml` 配置兼容 `/chat/completions` 的服务地址、生成模型、验证角色模型、费用上限和每百万输入/输出 token 费率。当前全部角色使用同一 Flash 模型的独立请求，结果不得描述为独立模型一致性。远端必须 HTTPS；密钥仅从 `OIL_LLM_API_KEY` 环境变量读取，勿写入代码或聊天。`scripts/run_model_pilot.py` 也支持不回显地输入密钥，仅存活于当前进程。

费用账本用 SQLite 事务预留上界，失败请求保留预留，避免不确定账单导致重复消费。账本跨运行累计；不能通过删除账本来假装费用未发生。按官方 Flash 高峰、缓存未命中价格保守估计（输入 $0.30/M、输出 $1.20/M，核对于 2026-10-06），供应商最终账单为准。来源：https://api-docs.deepseek.com/quick_start/pricing/ 。默认显式关闭 thinking，避免短结构化输出被隐式推理耗尽输出上限。

```powershell
# 配置和本地环境变量就绪后
.\.venv\Scripts\oil.exe query "What does the evidence establish about oil supply?" --generation llm --verify
.\.venv\Scripts\oil.exe generate --limit 50
.\.venv\Scripts\oil.exe export-reviews --dataset pilot
.\.venv\Scripts\oil.exe agreement
# 整理并裁决多标注者导出结果后，提交唯一记录列表；数量不足、未审核、分组未确认会拒绝冻结
.\.venv\Scripts\oil.exe freeze data/annotations/adjudicated.jsonl
.\.venv\Scripts\oil.exe evaluate data/frozen/VERSION/test.jsonl --generation llm
```

## 数据与接口

“段落标签”页签显示原文的主题、涉及实体、原油任务相关性、预测/实际/混合状态、关键数量单位和日期，独立于100条问答标注。页面仅计入通过校验的结果，实时进度见 `data/reports/passage_annotation_progress.json`。固定输入、逐批模型决策、输出、审计和修订记录位于 `data/annotations/passage_label_runs/e546fc6c7f1e48b7/`；全量完成前禁止发布为完整4,500段结果，原文库不改写。空数量/事件数组表示未单独选取，不等于未标注；机器输出不计作人工标签。

首轮4,500段发布为版本 `e4158423d4e7b3a5`，原不可覆盖快照保持不变。其728个待核对段落已全部完成机器二次复核：452个确认、20个修正、256个仍需核对来源。当前合并版本为 `034b1bc8d6575322`；完整标签在 `data/annotations/passage_labels.jsonl`，728条裁决在 `data/annotations/passage_review.jsonl`，统计与哈希在 `data/reports/passage_review.json`。可在“段落标签”选择“机器二次复核结果”，或勾选“只看段落中的歧义 / 待核对项”。

二次复核输入、盲标、比较、裁决及新快照位于 `data/annotations/passage_review_runs/e4158423d4e7b3a5/`，其中 `published/034b1bc8d6575322/` 为完整发布版本。两条政策主题粒度误判经主代理复读后追加修订，原裁决与审计未覆盖。256个未解决项不是已确认错误数，含源版本、统计口径、表格抽取以及保守保留的非原油行缺失警告；200个严格评估排除建议与这些状态重叠，不会删除原文或自动过滤在线检索。本次外部API调用为0，Codex订阅消耗未计量；人工审核仍为0。

- `data/sources.jsonl`：发现的来源、标题、日期依据和再分发标记。
- `data/raw/` 与 `data/documents.jsonl`：原始文件、链接、SHA-256、抓取时间和字节数。
- `data/passages.jsonl`：正文、文档/段落编号、页码、日期与地区。地区是关键词启发式，不是人工事实标签。
- `data/index/`：384 维英文语义向量、对应语料/模型/向量哈希；原生 NumPy 相似度计算。BM25 与向量候选以 reciprocal rank fusion 融合。
- `data/annotations/`、`data/annotations.sqlite3`：候选题、审核队列、追加式人工修改记录。
- `data/runs/`、`data/experiments/`：查询结果和实验配置、语料、代码、数据集哈希。

Python 查询入口 `oil_evidence.query.query(question, mode, as_of, region, temporal, verify, generation)` 返回 claims、evidence、removed_claims、verification_method、model_calls、retrieval_seconds、total_seconds。`temporal` 和 `verify` 分别对应 A/B。

所有数据采用 JSON/JSONL。模型建议、网页、PDF 都作为不可信资料，不作为执行指令。SQLite 仅用于标注和费用账本，不用于文本检索。

## 实验约束

英文 BGE 模型的中文检索效果未经验证；正式题目以英文为准。不得把检索命中当作答案正确。原文预览的 B 仅检查逐字引用，不能据此声称语义检查有效。

正式实验需要冻结数据、人工标签和模型服务。冒烟实验会明确写 `smoke_only=true`，无参考标签的质量指标为 null。检索召回率是候选池召回，未穷尽整个语料相关文档；必须一起报告 judged_fraction。先做开发集，禁止依据测试集反复改系统。

## 访问与版权

遵循 robots.txt，单主机节流、失败记录、文档大小及单批下载预算。403 不换身份绕过。EIA 来源保留归属与第三方图表版权标记；OPEC/政策资料的公开访问不等于可整库再分发。提交原始资料包前逐项检查许可，不能因报告写了云盘链接要求就默认有再分发权限。

## 未完成边界

1,000 条人工标注、两名独立人工标注者的一致性和课程方对单人/模型辅助方案的认可，不能由代码自动产生。最终正式实验、报告、展示和提交包须在这些输入齐备后完成，不能把当前工程检查写成作业实验结论。
