"""pytest configuration — custom markers for aerospace-testbench."""

import pytest


def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers so pytest does not warn about unknown ones."""
    config.addinivalue_line(
        "markers",
        "integration: mark test as requiring a live PostgreSQL database",
    )
    config.addinivalue_line(
        "markers",
        "hardware: mark test as requiring physical instruments connected to the host",
    )
