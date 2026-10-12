"""Export a whitelisted, hash-verified public progress summary, never raw data."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from oil_evidence.store import ROOT, digest, now


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def verify(path, expected):
    if digest(Path(path).read_bytes()) != expected:
        raise ValueError(f"Progress binding changed: {Path(path).name}")


def export(output=None):
    run = ROOT / "data/unified_runs/semantic-page-v2-buffer"
    checkpoint_path = run / "reports/completion_checkpoint.json"
    checkpoint = load(checkpoint_path)
    stage = run / "stage"
    corpus = load(stage / "reports/corpus.json")
    verify(stage / "passages.jsonl", checkpoint["corpus"]["sha256"])
    verify(stage / "source_pages.jsonl", checkpoint["corpus"]["source_pages_sha256"])
    for name, sha in corpus["implementation_hashes"].items():
        verify(ROOT / name, sha)
    receipts = {}
    for field in ("tests", "reconstruction_audit"):
        entry = checkpoint[field]
        path = run / entry["report"]
        verify(path, entry["sha256"])
        receipts[field] = load(path)
    for label in ("legacy", "new"):
        entry = checkpoint["source_qa"]
        path = run / entry[f"{label}_final_report"]
        verify(path, entry[f"{label}_sha256"])
        qa = load(path)
        if qa["remaining_critical_count"] != 0:
            raise ValueError("Unresolved fixed-sample source critical")
        for name, sha in qa["input_hashes"].items():
            verify(stage / name, sha)
        for name, sha in qa["implementation_hashes"].items():
            verify(ROOT / name, sha)
    for report in receipts.values():
        if report["corpus_sha256"] != checkpoint["corpus"]["sha256"]:
            raise ValueError("Receipt refers to another corpus")
    audit = receipts["reconstruction_audit"]
    if audit["errors"] or audit["index_verified"]:
        raise ValueError("Unexpected audit or release state")
    for name, sha in audit["stage_hashes"].items():
        verify(stage / name, sha)
    suite = receipts["tests"]
    verify(run / suite["junit_xml"], suite["junit_sha256"])
    suites = list(ET.parse(run / suite["junit_xml"]).getroot().iter("testsuite"))
    totals = {key: sum(int(item.get(key, "0")) for item in suites)
              for key in ("tests", "failures", "errors", "skipped")}
    passed = totals["tests"] - totals["failures"] - totals["errors"] - totals["skipped"]
    if (passed != suite["passed"] or totals["skipped"] != suite["skipped"]
            or totals["failures"] + totals["errors"] != suite["failed"]):
        raise ValueError("Test receipt and JUnit counts differ")
    for key in ("passages", "words", "unique_words", "contributing_documents", "cleaned_source_pages"):
        field = {"contributing_documents": "documents", "cleaned_source_pages": "source_pages"}.get(key, key)
        if checkpoint["corpus"][key] != corpus[field]:
            raise ValueError("Checkpoint and corpus statistics differ")
    summary = {
        "schema_version": 1,
        "exported_utc": now(),
        "status": "source_buffer_closeout_complete_new_corpus_staged_not_published",
        "publication_scope": "Code, documentation and whitelisted aggregate metrics only; original data and labels excluded.",
        "corpus": checkpoint["corpus"],
        "segmentation": checkpoint["segmentation"],
        "source_holds": checkpoint["source_holds"],
        "tests": {key: suite[key] for key in ("passed", "skipped", "failed", "elapsed_seconds", "skip_reason")},
        "tests_origin": "Recorded local run, not GitHub Actions",
        "source_reconstruction": {"errors": audit["errors"], "byte_rebuilt_artifact_classes": 4,
                                  "implementation_files": len(corpus["implementation_hashes"]),
                                  "index_verified": audit["index_verified"]},
        "machine_source_qa": {key: checkpoint["source_qa"][key] for key in (
            "fixed_cases", "additional_legacy_diagnostics", "total_original_cases_preserved",
            "new_original_critical_cases_excluded_not_passed", "warnings_retained",
            "remaining_known_sample_criticals", "human_gold", "whole_corpus_approved")},
        "default_corpus": {"passages": checkpoint["protection"]["default_corpus_passages"],
                           "archived_original_paragraph_machine_labels": 4500,
                           "existing_machine_qa_records": 100, "existing_machine_reviews": 728},
        "release": {key: checkpoint["release"][key] for key in (
            "new_index_created", "published", "evaluation_set_frozen", "formal_assignment_complete")},
        "new_tracked_paid_api_calls": checkpoint["protection"]["new_tracked_paid_model_api_calls"],
        "new_human_labels": checkpoint["protection"]["new_human_labels"],
        "codex_subscription_credit_usage": "Not measured",
        "local_receipt_sha256": {
            "completion_checkpoint": digest(checkpoint_path.read_bytes()),
            "tests": checkpoint["tests"]["sha256"],
            "reconstruction_audit": checkpoint["reconstruction_audit"]["sha256"],
            "legacy_fixed_review": checkpoint["source_qa"]["legacy_sha256"],
            "new_fixed_review": checkpoint["source_qa"]["new_sha256"]},
        "limitations": ["No raw documents, corpus, annotation records, databases or indexes are shipped.",
                        "Historical reconstruction requires the excluded matching local snapshots.",
                        "Machine source checks are neither human gold labels nor whole-corpus approval.",
                        "Course approval, held-out evaluation and new retrieval/publication remain pending."]}
    destination = Path(output) if output else ROOT / "reports/progress.json"
    destination = destination.resolve()
    if not destination.is_relative_to((ROOT / "reports").resolve()):
        raise ValueError("Public export must stay inside the project reports directory")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="\n") as stream:
        json.dump(summary, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    return destination, summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output")
    args = parser.parse_args()
    path, result = export(args.output)
    print(json.dumps({"output": path.relative_to(ROOT).as_posix(),
                      "passages": result["corpus"]["passages"],
                      "published": result["release"]["published"]}, ensure_ascii=False))
