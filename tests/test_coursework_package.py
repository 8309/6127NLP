"""Deterministic packaging and privacy rules, never redistribution clearance."""
import importlib.util
from pathlib import Path

import pytest


@pytest.fixture
def packager():
    spec = importlib.util.spec_from_file_location("coursework_packager", Path(__file__).parents[1] / "scripts/package_coursework.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("name", ["data/raw/report.pdf", "models/model.onnx", ".env", "docs/.env.local", "src/auth.pem", "../secret.json", "tmp/report.md", "src/auth.json", "docs/model.safetensors"])
def test_private_or_rights_sensitive_files_excluded(packager, name):
    assert not packager.allowed_source(name)


def test_code_and_public_summaries_included(packager):
    assert packager.allowed_source("app.py")
    assert packager.allowed_source("src/oil_evidence/codex_runtime.py")
    assert packager.allowed_source("reports/progress.json")
    assert not packager.allowed_source("reports/private.json")


def test_summary_redacts_text_secrets_and_local_paths(packager):
    value = dict(status="complete", usage=dict(input_tokens=12), claims=[dict(text="source")],
        quotes=[dict(text="source")], evidence=[dict(text="source")], artifact_directory="D:/private/path",
        OPENAI_API_KEY="synthetic", nested=dict(path="D:/private/file", corpus_sha256="fixture"))
    result = packager.sanitize_summary(value)
    assert result == dict(status="complete", usage=dict(input_tokens=12), nested=dict(path="[local path excluded]", corpus_sha256="fixture"))


def test_zip_bytes_reproduce_without_timestamp_drift(packager, tmp_path):
    first, second = tmp_path / "one.zip", tmp_path / "two.zip"
    packager.deterministic_zip(first, {"b.txt":b"two", "a.txt":b"one"})
    packager.deterministic_zip(second, {"a.txt":b"one", "b.txt":b"two"})
    assert first.read_bytes() == second.read_bytes()


def test_credential_literal_refuses_package_without_echoing_value(packager):
    token = b"sk-" + b"x" * 32
    with pytest.raises(ValueError, match="package refused") as failure:
        packager.guard_source_bytes("fixture.py", b'API_KEY="' + token + b'"')
    assert token.decode() not in str(failure.value)
    packager.guard_source_bytes("fixture.py", b'API_KEY="synthetic-placeholder"')


def test_credential_in_arbitrary_summary_value_is_not_copied(packager):
    token = "sk-" + "x" * 32
    result = packager.sanitize_summary(dict(message="Synthetic failure " + token,
        nested=[token, dict(status="complete", value=token)], normal="machine-only"))
    assert result == dict(message="[potential credential excluded]",
        nested=["[potential credential excluded]", dict(status="complete", value="[potential credential excluded]")],
        normal="machine-only")
    assert token not in str(result)
