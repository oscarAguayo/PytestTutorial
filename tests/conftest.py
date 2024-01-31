import pytest
import source.shapes as shapes


@pytest.fixture
def rectangle():
    return shapes.Rectangle(2, 4)

def pytest_configure(config):
    config.addinivalue_line('markers', 'slow: marks tests as slow (deselect with `-m \"not slow\"`)')