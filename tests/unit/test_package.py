"""Smoke tests — package is importable and metadata is present."""

import aerospace_testbench


def test_package_version_is_defined() -> None:
    """The package must expose a version string."""
    assert isinstance(aerospace_testbench.__version__, str)
    assert len(aerospace_testbench.__version__) > 0


def test_package_version_format() -> None:
    """Version must follow semver major.minor.patch."""
    parts = aerospace_testbench.__version__.split(".")
    assert len(parts) == 3
    assert all(part.isdigit() for part in parts)
