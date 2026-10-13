"""Five mocked single-stream wrapper tests; no model or authentication calls."""
import importlib.util
from pathlib import Path

import pytest


@pytest.fixture
def wrapper(monkeypatch):
    scripts = Path(__file__).parents[1] / "scripts"
    monkeypatch.syspath_prepend(str(scripts))
    spec = importlib.util.spec_from_file_location("isolated_codex_stream", scripts / "run_codex_annotation_stream.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def cli(wrapper, tmp_path, monkeypatch):
    binary = tmp_path / "codex.exe"
    wrapper.native.write_new(binary, b"fixture-only-not-executed")
    monkeypatch.setattr(wrapper.native, "discover_native_cli", lambda requested: binary)
    return binary


def test_only_selected_stream_runs_and_globals_restore(wrapper, cli, tmp_path, monkeypatch):
    before = wrapper.native.STREAMS, wrapper.native.load_pool, wrapper.native.write_new
    seen = []
    def mocked_run(root, pool, **kwargs):
        seen.append((wrapper.native.STREAMS, kwargs))
        return tmp_path, dict(failures=[])
    monkeypatch.setattr(wrapper.native, "run", mocked_run)
    wrapper.run_stream(tmp_path, tmp_path, "b", 50)
    assert seen == [(("b",), dict(max_records=50, cli=str(cli)))]
    assert (wrapper.native.STREAMS, wrapper.native.load_pool, wrapper.native.write_new) == before


def test_parent_guards_preserved_and_wrapper_added(wrapper, cli, tmp_path, monkeypatch):
    expected = {"synthetic-original": "original-hash"}
    monkeypatch.setattr(wrapper.native, "load_pool", lambda root, pool: (tmp_path, [], expected))
    def mocked_run(root, pool, **kwargs):
        _, _, protected = wrapper.native.load_pool(root, pool)
        assert protected["synthetic-original"] == "original-hash"
        assert protected[str(Path(wrapper.__file__).resolve())] == wrapper.native.protocol.sha256(Path(wrapper.__file__).read_bytes())
        assert expected == {"synthetic-original": "original-hash"}
        return tmp_path, dict(failures=[])
    monkeypatch.setattr(wrapper.native, "run", mocked_run)
    wrapper.run_stream(tmp_path, tmp_path)


def test_receipt_saved_before_generation_and_prompt_bytes_unchanged(wrapper, cli, tmp_path, monkeypatch):
    row = dict(question_id="q-1", question="What did the synthetic oil report observe?", question_zh="Translated fixture", as_of="2024-06-30",
               evidence=[dict(passage_id="p-1", text="Crude exports were stable.", available_by="2024-01-01")])
    original_packet, original_stdin = wrapper.native.packet_and_prompt(row)
    def mocked_run(root, pool, **kwargs):
        output = tmp_path / "separate-run"
        wrapper.native.write_new(output / "manifest.json", dict(specification=dict(streams=list(wrapper.native.STREAMS))))
        receipt = wrapper.native.read_json(output / "stream_wrapper_receipt.json")
        assert receipt["stream"] == "b"
        assert receipt["wrapper_sha256"] == wrapper.native.protocol.sha256(Path(wrapper.__file__).read_bytes())
        assert receipt["native_cli_name"] == "codex.exe"
        assert receipt["shared_progress_writers"] is False
        assert receipt["external_paid_api_calls"] == 0
        assert wrapper.native.packet_and_prompt(row) == (original_packet, original_stdin)
        assert receipt["protocol_sha256"] == original_packet["prompt_sha256"]
        return output, dict(failures=[])
    monkeypatch.setattr(wrapper.native, "run", mocked_run)
    wrapper.run_stream(tmp_path, tmp_path)


def test_failure_restores_patches_without_fallback_or_second_stream(wrapper, cli, tmp_path, monkeypatch):
    before = wrapper.native.STREAMS, wrapper.native.load_pool, wrapper.native.write_new
    calls = []
    def mocked_run(root, pool, **kwargs):
        calls.append(wrapper.native.STREAMS)
        raise RuntimeError("Synthetic quota/error stop")
    monkeypatch.setattr(wrapper.native, "run", mocked_run)
    with pytest.raises(RuntimeError, match="quota/error"):
        wrapper.run_stream(tmp_path, tmp_path)
    assert calls == [("b",)]
    assert (wrapper.native.STREAMS, wrapper.native.load_pool, wrapper.native.write_new) == before


def test_wrong_executable_or_stream_rejected_before_model_call(wrapper, tmp_path, monkeypatch):
    wrong = tmp_path / "other.exe"
    wrapper.native.write_new(wrong, b"fixture-only")
    monkeypatch.setattr(wrapper.native, "discover_native_cli", lambda requested: wrong)
    monkeypatch.setattr(wrapper.native, "run", lambda *args, **kwargs: pytest.fail("No model run allowed"))
    with pytest.raises(ValueError, match="native codex.exe"):
        wrapper.run_stream(tmp_path, tmp_path)
    with pytest.raises(ValueError, match="stream"):
        wrapper.run_stream(tmp_path, tmp_path, "both")
