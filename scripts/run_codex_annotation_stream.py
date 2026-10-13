"""Run one independent annotation stream in its own process and output directory.

The existing individual-record protocol and input bytes are unchanged. This
wrapper selects only A or B, adds its source hash to protected inputs, and saves
a caller receipt before generation. It never edits the shared runner or helper.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import run_codex_annotation as native


def validated_cli(cli):
    executable = native.discover_native_cli(cli)
    if executable.name.lower() != "codex.exe" or not executable.is_file():
        raise ValueError("The stream wrapper requires the native codex.exe launcher")
    return executable


def run_stream(root, pool_dir, stream="b", max_records=50, cli=native.DEFAULT_CLI):
    if stream not in {"a", "b"}:
        raise ValueError("Select stream a or b")
    executable = validated_cli(cli)
    wrapper = Path(__file__).resolve()
    wrapper_sha = native.protocol.sha256(wrapper.read_bytes())
    runner_sha = native.protocol.sha256(Path(native.__file__).read_bytes())
    metadata = dict(schema_version=1, stream=stream, wrapper_sha256=wrapper_sha,
                    native_runner_sha256=runner_sha, native_cli_name=executable.name,
                    native_cli_sha256=native.protocol.sha256(executable.read_bytes()),
                    python_executable=str(Path(sys.executable).resolve()),
                    protocol_sha256=native.protocol.sha256((native.GUARD + "\n" + native.protocol.ANNOTATION_PROMPT).encode("utf-8")),
                    context_policy="Unmodified individual record protocol; one fresh context per selected stream record",
                    authentication="Existing ChatGPT login is checked by the unchanged native runner",
                    separate_output_directory=True, shared_progress_writers=False,
                    external_paid_api_calls=0, human_gold=False)
    previous_streams, previous_loader, previous_writer = native.STREAMS, native.load_pool, native.write_new

    def guarded_loader(selected_root, selected_pool):
        directory, rows, protected = previous_loader(selected_root, selected_pool)
        return directory, rows, {**protected, str(wrapper): wrapper_sha}

    def receipt_writer(path, value):
        previous_writer(path, value)
        if Path(path).name == "manifest.json" and isinstance(value, dict) and "specification" in value:
            previous_writer(Path(path).parent / "stream_wrapper_receipt.json", metadata)

    native.STREAMS = (stream,)
    native.load_pool = guarded_loader
    native.write_new = receipt_writer
    try:
        # No resume: the original concurrent run's progress must never be written.
        return native.run(root, pool_dir, max_records=max_records, cli=str(executable))
    finally:
        native.STREAMS, native.load_pool, native.write_new = previous_streams, previous_loader, previous_writer


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--canonical-root", required=True, type=Path)
    parser.add_argument("--pool-dir", required=True, type=Path)
    parser.add_argument("--stream", choices=["a", "b"], default="b")
    parser.add_argument("--max-records", type=int, default=50)
    parser.add_argument("--codex-cli", default=native.DEFAULT_CLI)
    args = parser.parse_args()
    _, summary = run_stream(args.canonical_root, args.pool_dir, args.stream,
                            args.max_records, args.codex_cli)
    print(json.dumps(summary, indent=2))
    raise SystemExit(1 if summary["failures"] else 0)
