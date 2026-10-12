from datetime import date
from html import escape
import json
import os
import time

import streamlit as st

from oil_evidence.annotations import agreement, validate_record
from oil_evidence.corpus_versions import annotation_passages, active_label_coverage, original_parent
from oil_evidence.query import query
from oil_evidence.retrieval import Retriever
from oil_evidence.store import DATA, config, digest, latest_reviews, read_jsonl, save_review, mark_suggestion_view, has_suggestion_view

st.set_page_config(page_title="Oil Evidence", page_icon="🛢", layout="wide")
st.title("Oil Evidence · 原油证据工作台")
with st.sidebar.expander("模型连接 · 本机进程"):
    st.caption("已配置 DeepSeek V4.1 Flash，累计估计费用上限 USD 5。密钥不会保存到文件。")
    with st.form("runtime_key"):
        runtime_key = st.text_input("DeepSeek API key", type="password")
        use_key = st.form_submit_button("仅用于当前服务进程")
    if use_key:
        if runtime_key.strip():
            os.environ[config()["llm"]["api_key_env"]] = runtime_key.strip()
            st.success("当前进程已配置；停止服务后失效。")
        else:
            st.error("密钥为空。")
    st.caption("连接状态：" + ("当前进程有密钥" if os.environ.get(config()["llm"]["api_key_env"]) else "当前进程未配置密钥，可使用原文预览"))
search_tab, review_tab, passage_tab, status_tab = st.tabs(["证据查询", "标注核对", "段落标签", "数据与进度"])

# Existing annotations always use their frozen text version, never child IDs.
try:
    annotation_rows = annotation_passages()
    annotation_map = {p["passage_id"]: p for p in annotation_rows}
except ValueError as exc:
    st.error("标注语料版本校验失败：" + str(exc))
    st.stop()


@st.cache_resource
def load_retriever(corpus_mtime, index_mtime):
    return Retriever()


def get_retriever():
    path = DATA / "passages.jsonl"
    index = DATA / "index/manifest.json"
    return load_retriever(path.stat().st_mtime_ns, index.stat().st_mtime_ns if index.exists() else 0)


with search_tab:
    st.caption("英文证据库。本地英文向量模型尚未验证中文检索质量，正式评估请使用英文问题。")
    with st.form("query"):
        question = st.text_area("研究问题", "What factors affect global crude oil supply and inventories?")
        a, b, c = st.columns(3)
        cutoff = a.date_input("资料截止日期", value=date.fromisoformat(config()["corpus"]["end_date"]))
        region = b.selectbox("地区（正文关键词筛选）", ["All", "Middle East", "Europe", "Asia", "Americas", "Africa"])
        mode = c.selectbox("检索方案", ["hybrid", "bm25", "dense"])
        temporal = st.checkbox("A：仅使用截止日前可获得的资料", value=True)
        verify = st.checkbox("B：检查引用支持（原文预览模式仅检查逐字引用）", value=False)
        generation = st.selectbox("回答方式", ["extractive", "llm"], format_func=lambda x: "原文摘录预览 · 无需模型 API" if x == "extractive" else "模型综合回答 · 需配置服务")
        submitted = st.form_submit_button("查询", type="primary")
    if submitted:
        try:
            with st.spinner("检索证据…"):
                st.session_state["query_result"] = query(question, mode=mode, as_of=cutoff.isoformat(),
                    region=None if region == "All" else region, temporal=temporal, verify=verify,
                    generation=generation, retriever=get_retriever())
        except Exception as exc:
            st.error(str(exc))
    result = st.session_state.get("query_result")
    if result:
        st.caption(f"{result['retrieval_mode']} · {result['total_seconds']:.2f} 秒 · {result['generation']}")
        for limitation in result["limitations"]:
            st.info(limitation)
        for claim in result["claims"]:
            st.write(claim["text"])
            st.caption("证据：" + ", ".join(claim["citations"]))
        for p in result["evidence"]:
            with st.expander(f"#{p['rank']} {p['title']} · 第 {p['page']} 页 · {p['available_by']}"):
                st.write(p["text"])
                st.markdown(f"[打开原始来源]({p['url']})")
                st.caption(f"{p['passage_id']} · 日期精度：{p['date_precision']} · 分数 {p['score']:.4f}")
                if p.get("parent_passage_id") or p.get("source_page_id"):
                    try:
                        parent = original_parent(p)
                        is_page = bool(p.get("source_page_id"))
                        label = "清洗后来源页" if is_page else "原父段"
                        context_id = parent["source_page_id"] if is_page else parent["passage_id"]
                        with st.expander(label + " · 仅上下文，不计额外检索段"):
                            st.caption("此上下文不自动加入答案引用，也不计入检索排名或语料段数。")
                            st.write(parent["text"])
                            st.caption(f"{label} {context_id} · 第 {parent['page']} 页 · {parent['available_by']}")
                    except ValueError as exc:
                        st.warning("来源上下文版本校验失败，暂不展示上下文：" + str(exc))
        st.download_button("导出本次查询 JSON", json.dumps(result, ensure_ascii=False, indent=2), file_name="query.json", mime="application/json")

with review_tab:
    st.caption("Codex 核对结果为机器标注，不自动算作人工审核。下面的人工表单只有点击保存才会写入人工判断。")
    if annotation_rows != read_jsonl(DATA / "passages.jsonl"):
        st.info("旧版本标注存档：问答候选池与引用仍对应原固定语料；不自动迁移到当前重新分块的检索段。")
    datasets = (["codex"] if (DATA / "annotations/codex.jsonl").exists() else []) + ["pilot", "candidates"]
    dataset = st.selectbox("审核数据", datasets, format_func=lambda x: {
        "codex": "Codex 已完成 · 100 条", "pilot": "原始待标注题 · 50 条", "candidates": "原始 Flash 候选 · 50 条"}[x])
    records = read_jsonl(DATA / f"annotations/{dataset}.jsonl")
    if dataset == "codex":
        outcomes = {name: sum(r["codex_review"]["result"] == name for r in records)
                    for name in ["passed", "corrected", "partial", "insufficient"]}
        st.success(f"已完成 {len(records)} 条：未发现明显错误 {outcomes['passed']} · 已修正 {outcomes['corrected']} · 部分可答 {outcomes['partial']} · 证据不足 {outcomes['insufficient']}")
        view = st.selectbox("核对结果筛选", ["全部", "已修正", "部分可答 / 证据不足", "不建议进入正式评估"])
        if view == "已修正":
            records = [r for r in records if r["codex_review"]["result"] == "corrected"]
        elif view == "部分可答 / 证据不足":
            records = [r for r in records if r["answerability"] != "sufficient"]
        elif view == "不建议进入正式评估":
            records = [r for r in records if not r["recommended_for_oil_evaluation"]]
    if not records:
        st.info("尚无审核队列。运行 oil pilot；模型配置后可运行 oil generate。")
    else:
        who = st.text_input("人工标注者 ID（真实区分不同标注者）", key="annotator")
        reviews = latest_reviews()
        completed = {r["record_id"] for r in reviews if r["annotator"] == who}
        st.caption(f"当前标注者已保存 {len(completed)} 条；所有记录保留追加式修改历史。")
        index = st.selectbox("记录", range(len(records)), format_func=lambda i: f"{'✓ ' if records[i]['record_id'] in completed else ''}{records[i]['record_id']}: {records[i]['question'][:85]}")
        record = records[index]
        key = record["record_id"]
        view_key = f"{dataset}:{key}:{who}"
        st.session_state.setdefault("start:" + view_key, time.monotonic())
        # Keep the full question above potentially long machine suggestions.
        # Escape source text so the responsive display cannot inject HTML.
        with st.container(border=True):
            st.markdown("### 完整问题")
            st.markdown(
                '<div aria-label="完整问题" style="white-space:pre-wrap;overflow-wrap:anywhere;'
                'font-size:1.15rem;line-height:1.65;">'
                + escape(record["question"]) + '</div>',
                unsafe_allow_html=True,
            )
            if record.get("question_zh"):
                st.write(record["question_zh"])
            st.caption("截止日期：" + str(record.get("as_of")))
        shown = st.checkbox("显示模型/候选答案建议（会记录为辅助审核）", value=dataset == "codex", key="show:" + view_key)
        if shown:
            st.session_state["exposed:" + view_key] = True
            mark_suggestion_view(key, who)
            review = record.get("codex_review")
            if review:
                result_label = {"passed": "未发现明显错误", "corrected": "已修正", "partial": "部分可答", "insufficient": "证据不足"}[review["result"]]
                st.subheader("Codex 核对结论 · " + result_label)
                st.write(review["note_zh"])
                if not record["recommended_for_oil_evaluation"]:
                    st.warning("这条已完成机器标注，但因范围、重复模板或来源日期问题，暂不建议进入正式原油评估集。")
            st.caption("证据是否足够：" + {"sufficient": "足够", "partial": "只能回答一部分", "insufficient": "不足", "unlabelled": "尚未标注"}.get(record.get("answerability"), "尚未标注")
                       + " · 事件状态：" + {"announced": "已宣布", "effective": "已生效", "observed": "来源报告已发生", "recovered": "已恢复", "uncertain": "预测 / 混合状态 / 不确定", "not_applicable": "不适用", "unlabelled": "尚未标注"}.get(record.get("event_status"), "尚未标注"))
            st.markdown("#### 参考答案要点（机器）")
            for n, point in enumerate(record.get("answer_points") or [], 1):
                st.write(f"{n}. {point}")
            if not record.get("answer_points"):
                st.info("这组原始记录没有机器答案；请选择 Codex 已完成数据查看新标注。")
            with st.expander("支持答案的逐字引用（机器）"):
                for q in record.get("quotes") or []:
                    st.write(q["text"])
                    st.caption(q["passage_id"])
                if not record.get("quotes"):
                    st.caption("没有足以支持实质答案的引用；不编造证据。")
            with st.expander("查看原始标注数据 JSON"):
                st.json({k: record.get(k) for k in ["answer_points", "quotes", "answerability", "event_status", "codex_review", "original_annotation", "model_verification"]})
        passage_map = annotation_map
        pool = record.get("candidate_pool_ids", record.get("evidence_ids", []))
        if record.get("validation_errors"):
            st.warning("机器预校验发现问题：" + "; ".join(record["validation_errors"]))
        prior = next((r for r in reviews if r["annotator"] == who and r["record_id"] == key), None)
        previous = prior["payload"] if prior else {}
        qrels = {}
        quotes = []
        for pid in pool:
            p = passage_map.get(pid)
            if not p:
                st.error(f"原文缺失：{pid}")
                continue
            with st.expander(f"{p['title']} / p.{p['page']} / {pid}", expanded=True):
                st.write(p["text"])
                st.markdown(f"[原文]({p['url']}) · 可获得日期 {p['available_by']}")
                if shown and pid in record.get("qrels", {}):
                    st.caption("机器相关性：" + {0: "无关", 1: "背景 / 部分相关", 2: "直接支持答案"}[record["qrels"][pid]] + "；下方人工判断不会自动填入机器标签。")
                grade = st.selectbox("相关性", [-1, 0, 1, 2],
                    index=[-1, 0, 1, 2].index(previous.get("qrels", {}).get(pid, -1)),
                    format_func=lambda x: {-1: "未判断", 0: "无关", 1: "背景/部分相关", 2: "直接支持答案"}[x], key=f"grade:{view_key}:{pid}")
                if grade >= 0:
                    qrels[pid] = grade
                old_quote = next((q["text"] for q in previous.get("quotes", []) if q["passage_id"] == pid), "")
                quote = st.text_area("支持答案的原文片段（直接复制，留空表示不用此段）", value=old_quote, key=f"quote:{view_key}:{pid}")
                if quote.strip():
                    quotes.append(dict(passage_id=pid, text=quote.strip()))
        with st.form("review:" + view_key):
            edited_question = st.text_area("最终问题", value=previous.get("question", record["question"]))
            options = ["unlabelled", "sufficient", "partial", "insufficient"]
            answerability = st.selectbox("证据是否足够", options, index=options.index(previous.get("answerability", "unlabelled")))
            statuses = ["unlabelled", "announced", "effective", "observed", "recovered", "uncertain", "not_applicable"]
            event_status = st.selectbox("事件状态", statuses, index=statuses.index(previous.get("event_status", "unlabelled")))
            points = st.text_area("参考答案要点：每行一条", value="\n".join(previous.get("answer_points", [])))
            group = st.text_input("事件分组 ID（相同事件及改写题必须同组）", value=previous.get("event_group", record["event_group"]))
            group_checked = st.checkbox("我已确认事件分组，包含跨文档的同一事件", value=not previous.get("event_group_review_required", True))
            accept = st.checkbox("接受为候选正式评估记录", value=previous.get("status") == "accepted")
            note = st.text_area("备注/错误原因", value=previous.get("note", ""))
            save = st.form_submit_button("保存人工判断")
        if save:
            payload = dict(question=edited_question.strip(), answerability=answerability, event_status=event_status,
                           answer_points=[p.strip() for p in points.splitlines() if p.strip()], event_group=group,
                           event_group_review_required=not group_checked, qrels=qrels, quotes=quotes,
                           evidence_ids=[q["passage_id"] for q in quotes], note=note,
                           status="accepted" if accept else "draft", as_of=record.get("as_of"),
                           elapsed_seconds=time.monotonic() - st.session_state["start:" + view_key])
            errors = validate_record(payload, passage_map) if accept else []
            if accept and (not group_checked or not qrels):
                errors.append("正式记录需确认事件分组并完成相关性判断")
            exposed = st.session_state.get("exposed:" + view_key, False) or has_suggestion_view(key, who) or (prior and prior["mode"] == "human_reviewed")
            if errors:
                st.error("；".join(errors))
            else:
                try:
                    save_review(key, who, "human_reviewed" if exposed else "human_independent", payload)
                    st.success("已保存。模型生成题目本身仍记录为合成题目，不等于人工原创。")
                except ValueError as exc:
                    st.error(str(exc))

with passage_tab:
    progress_path = DATA / "reports/passage_annotation_progress.json"
    if not progress_path.exists():
        st.info("尚未准备原文段落标注批次。")
    else:
        progress = json.loads(progress_path.read_text(encoding="utf-8"))
        current_passages = read_jsonl(DATA / "passages.jsonl")
        annotation_archive = len(current_passages) != progress['total'] or digest((DATA / 'passages.jsonl').read_bytes()) != progress['corpus_sha256']
        if annotation_archive:
            st.info(f"旧版本标注存档：当前检索语料 {len(current_passages):,} 段；下面的 {progress['validated']:,} 段机器标签只对应冻结原文。重新分块的新段不自动继承标签，问答候选池不代表当前全库真值。")
        st.subheader(f"{'旧版本' if annotation_archive else ''}原文段落标注 · {progress['validated']} / {progress['total']}")
        st.progress(progress["validated"] / progress["total"])
        st.caption(f"剩余 {progress['remaining']} 段；按段标主题和事件，不是问答题标注。机器标签不计作人工判断。")
        second_progress_path = DATA / "reports/passage_review_progress.json"
        if second_progress_path.exists():
            second = json.loads(second_progress_path.read_text(encoding="utf-8"))
            st.caption(f"机器二次复核：盲标 {second['blind_completed']} / {second['total']}；比较裁决 {second['reviewed']} / {second['total']}。准备输入不计作复核完成。")
        root = DATA / "annotations/passage_label_runs" / progress["corpus_sha256"][:16]
        labels = []
        for number, expected_hash in progress["output_sha256"].items():
            path = root / "outputs" / f"batch-{int(number):03d}.json"
            if path.exists() and digest(path.read_bytes()) == expected_hash:
                labels.extend(json.loads(path.read_text(encoding="utf-8"))["labels"])
            else:
                st.warning(f"第 {number} 批输出已变化，请重新校验后查看。")
        published_path = DATA / "annotations/passage_labels.jsonl"
        published_report_path = DATA / "reports/passage_annotation.json"
        if published_path.exists() and published_report_path.exists():
            published_report = json.loads(published_report_path.read_text(encoding="utf-8"))
            if (digest(published_path.read_bytes()) == published_report["labels_sha256"]
                and published_report["corpus_sha256"] == progress["corpus_sha256"]):
                labels = read_jsonl(published_path)
                st.caption(("存档标签版本：" if annotation_archive else "当前标签版本：") + published_report["version"])
            else:
                st.warning("合并标签的哈希或语料版本不匹配；仅展示此前通过校验的原始批次。")
        if labels:
            coverage = active_label_coverage(labels)
            st.caption(f"当前检索段标签覆盖：{coverage:,} / {len(current_passages):,}；旧版本机器标签存档：{len(labels):,}；当前未标注 {len(current_passages)-coverage:,} 段。")
            topic_labels = {"production_supply": "产量 / 供应", "opec_policy": "OPEC 政策", "sanctions_policy": "制裁 / 政策",
                            "shipping_logistics": "运输 / 航道", "inventories": "库存", "refining_demand": "炼油 / 需求",
                            "prices_market": "价格 / 市场", "statistical_methodology": "统计口径 / 方法", "other_energy": "其他能源", "other": "其他"}
            topic = st.selectbox("段落主题筛选", ["all"] + sorted({t for r in labels for t in r["topics"]}),
                                 format_func=lambda t: "全部" if t == "all" else topic_labels[t])
            attention = st.checkbox("只看段落中的歧义 / 待核对项")
            selected = [r for r in labels if (topic == "all" or topic in r["topics"]) and (not attention or r["needs_review"])]
            keyword = st.text_input("段落标签搜索（标题 / 实体 / 中文摘要）").strip().casefold()
            if keyword:
                titles = {pid: p["title"] for pid, p in annotation_map.items()}
                selected = [r for r in selected if keyword in (titles[r["passage_id"]] + " " + r["summary_zh"] + " " + " ".join(r["entities"])).casefold()]
            review_rows = read_jsonl(DATA / "annotations/passage_review.jsonl")
            if review_rows:
                outcome_names = {"all": "全部", "confirmed": "二次确认", "corrected": "二次修正", "unresolved": "仍未解决"}
                review_filter = st.selectbox("机器二次复核结果", list(outcome_names), format_func=outcome_names.get)
                if review_filter != "all":
                    selected = [r for r in selected if r.get("second_pass_outcome") == review_filter]
            st.caption(f"当前筛选 {len(selected)} 段；主题为多标签，主题统计不能直接相加当段落总数。")
            if selected:
                by_id = annotation_map
                position = st.selectbox("原文段落", range(len(selected)),
                                       format_func=lambda i: f"{by_id[selected[i]['passage_id']]['title']} · p.{by_id[selected[i]['passage_id']]['page']} · {selected[i]['passage_id']}")
                label = selected[position]
                passage = by_id[label["passage_id"]]
                st.write(label["summary_zh"])
                st.caption("主题：" + " / ".join(topic_labels[t] for t in label["topics"]) + " · 状态：" +
                           {"observed": "来源报告已发生", "estimated": "估计", "forecast": "预测", "announced": "已宣布", "effective": "已生效",
                            "recovered": "已恢复", "mixed": "混合状态", "uncertain": "不确定", "not_applicable": "不适用"}[label["event_status"]])
                st.caption("涉及实体（原文名称）：" + " / ".join(label["entities"]))
                st.caption("原油任务相关性：" + {"direct": "直接相关", "background": "背景相关", "out_of_scope": "范围外", "uncertain": "待判断"}[label["oil_relevance"]])
                for reason in label["review_reasons"]:
                    st.warning(reason)
                review = next((r for r in review_rows if r["passage_id"] == label["passage_id"]), None)
                if review:
                    st.info("机器二次复核 · " + outcome_names[review["outcome"]] + "：" + review["note"])
                    if review["exclude"]:
                        st.warning("本轮判定不宜用于严格历史/正式评估；这不是删除原文。")
                    with st.expander("二次复核依据（原文或上下文逐字片段）"):
                        for context_id, quote in review["support"]:
                            st.caption("依据位置：" + context_id + "；PDF文本不代表已验证表格视觉布局。")
                            st.write(quote)
                st.write(passage["text"])
                st.markdown(f"[查看原始来源]({passage['url']}) · 发布可得日期 {passage['available_by']}")
                with st.expander("数量、单位、事件日期及原始标签"):
                    for quantity in label["quantities"]:
                        st.write(f"数量：{quantity['value_text']} {quantity['unit_text']} · 对应时期/口径：{quantity['reference_period']}")
                        st.caption("原文支持：" + quantity["quote"])
                    for event in label["events"]:
                        st.write(f"事件：{event['description']} · 原文日期：{event['date_text'] or '未写明'}")
                        st.caption("原文支持：" + event["quote"])
                    if not label["quantities"] and not label["events"]:
                        st.caption("未单独提取关键数量或带日期事件；不代表未标注，也不保证正文没有数字。")
                    st.json(label)
            else:
                st.info("该筛选下没有已标注段落。")
        else:
            st.info("批次已准备，尚无通过校验的模型标签。")

with status_tab:
    codex_report = DATA / "reports/codex_annotation.json"
    if codex_report.exists():
        st.subheader("Codex 机器标注进度")
        st.json(json.loads(codex_report.read_text(encoding="utf-8")))
    report = DATA / "reports/corpus.json"
    if report.exists():
        st.json(json.loads(report.read_text(encoding="utf-8")))
    st.json(agreement())
    st.warning("模型预标注、单人完成和人工一致性要求仍需课程方确认。零人工标签不构成正式评估。")
