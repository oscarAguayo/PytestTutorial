import pytest
import time

@pytest.mark.skip(reason="This feature is currently broken")
def test_add():
    assert 1 + 2 == 2 + 1

@pytest.mark.slow # reference: https://docs.pytest.org/en/latest/how-to/mark.html and https://pytest-with-eric.com/hooks/pytest-configure/
def test_very_slow():
    time.sleep(7)
    assert 1 + 2 == 2 + 1

@pytest.mark.xfail(reason="We know we cannot divide by zero")
def test_divide_by_zero():
    assert 7/0