"""Tests for boolean template options."""

from __future__ import annotations

import pytest


class TestWithoutExample:
    """With add_example=False, example-specific files should be absent."""

    ABSENT_FILES = [
        "src/test_schema/schema/test_schema.yaml",
        "tests/test_data.py",
        "tests/data/valid/Person-001.yaml",
        "tests/data/valid/PersonCollection-001.yaml",
        "tests/data/invalid/Person-002.yaml",
    ]

    PRESENT_FILES = [
        "pyproject.toml",
        "justfile",
        "config.public.mk",
        "src/test_schema/__init__.py",
        "src/test_schema/schema/README.md",
        "tests/__init__.py",
        "tests/data/README.md",
    ]

    @pytest.mark.parametrize("relpath", ABSENT_FILES)
    def test_file_absent(self, no_example_project, relpath):
        assert not (no_example_project / relpath).exists(), f"Should be absent: {relpath}"

    @pytest.mark.parametrize("relpath", PRESENT_FILES)
    def test_file_present(self, no_example_project, relpath):
        assert (no_example_project / relpath).exists(), f"Missing: {relpath}"


class TestWithoutPypiAction:
    """With gh_action_pypi=False, pypi-publish.yaml should be absent."""

    def test_pypi_publish_absent(self, no_pypi_project):
        assert not (no_pypi_project / ".github/workflows/pypi-publish.yaml").exists()

    def test_main_workflow_present(self, no_pypi_project):
        assert (no_pypi_project / ".github/workflows/main.yaml").exists()


class TestWithoutDocsPreview:
    """With gh_action_docs_preview=False, test_pages_build.yaml should be absent."""

    def test_pages_build_absent(self, no_docs_preview_project):
        assert not (
            no_docs_preview_project / ".github/workflows/test_pages_build.yaml"
        ).exists()

    def test_deploy_docs_present(self, no_docs_preview_project):
        assert (no_docs_preview_project / ".github/workflows/deploy-docs.yaml").exists()


class TestWithLokf:
    """With add_lokf=True, the knowledge bundle and lokf recipes should be present."""

    PRESENT_FILES = [
        "knowledge/index.md",
        "knowledge/glossary/active-user.md",
        "knowledge/metrics/weekly-active-users.md",
        "lokf.justfile",
    ]

    @pytest.mark.parametrize("relpath", PRESENT_FILES)
    def test_file_present(self, lokf_project, relpath):
        assert (lokf_project / relpath).exists(), f"Missing: {relpath}"

    def test_lokf_dependency_present(self, lokf_project):
        pyproject = (lokf_project / "pyproject.toml").read_text(encoding="utf-8")
        assert "lokf[build,tables]" in pyproject

    def test_justfile_imports_lokf(self, lokf_project):
        justfile = (lokf_project / "justfile").read_text(encoding="utf-8")
        assert 'import? "lokf.justfile"' in justfile


class TestWithoutLokf:
    """With add_lokf=False (the default), no LOKF files should be produced."""

    ABSENT_FILES = [
        "knowledge/index.md",
        "knowledge/glossary/active-user.md",
        "knowledge/metrics/weekly-active-users.md",
        "lokf.justfile",
    ]

    @pytest.mark.parametrize("relpath", ABSENT_FILES)
    def test_file_absent(self, default_project, relpath):
        assert not (default_project / relpath).exists(), f"Should be absent: {relpath}"

    def test_lokf_dependency_absent(self, default_project):
        pyproject = (default_project / "pyproject.toml").read_text(encoding="utf-8")
        assert "lokf[build,tables]" not in pyproject

