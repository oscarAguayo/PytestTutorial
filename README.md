# Pytest

Reference: https://www.youtube.com/watch?v=cHYq1MRoyI0

Documentation: https://pytest.org/

Pytest is a testing framework for Python, auto-discovery of test files.

## Install

```shell
(venv) $ pip install pytest
```

## Import pytest

You need to import `pytest` in each test file.

```python
# tests/test_circle.py
import pytest
```

## Execute all tests

```shell
(venv) $ pytest
```

## Basic tests

### Define a test file

All test files starts with **test_** and then the name of file you want. Example: `test_functions.py`

### Define a function test

All functions test starts with **test_** and then the name of function to test, example: `test_function_name`

```python
# source/functions.py
def add(number_one: int, number_two: int) -> int:
	return number_one + number_two

def divide(number_one: int, number_two: int) -> float:
	return number_one/number_two
```

```python
# tests/test_functions.py
from source.functions import add, divide
import pytest


def test_add(): # the name of test function starts with test
	result = add(1, 4)
	assert result == 5


def test_divide_by_zero():
	with pytest.raises(ZeroDivisionError):
		divide(5, 0)
```

### Assert

`assert` is the way that python can test a valid argument. If is `True` the argument _pass_ the test. Else if is `False` the argument _fail_ the test and the execution is interrupted with an AsertionError message.

### Execute a specific test

You can execute a simple test with

```shell
(venv) $ pytest tests/test_functions.py
```

### Expect an Exception in test

When you expect an exception in the function, you can "handle" with `with pytest.raises(Exception)` that allow that the test can continue.

```python
def test_divide_by_zero():
	with pytest.raises(ZeroDivisionError):
		divide(5, 0)
```

## Class-based Test

We can define a Class Tests whit the prefix `Test` text in class name.


```python
class TestCircle:

	def test_one(self):
		assert True
```

### Methods in classes

You can use some methods to execute before or after each test, we can use `setup_method(self, method)` to execute the method before each test or `teardown_method(self, method)` to execute the method after each test.

## Fixtures

We can define values with the decorator `@pytest.fixture` in a function:

```python
# tests/test_rectangle.py
import pytest
import source.shapes as shapes

@pytest.fixture
def rectangle():
    return shapes.Rectangle(2, 4)

def test_area(rectangle):
    assert rectangle.area() == 2 * 4

def test_perimeter(rectangle):
    assert rectangle.perimeter() == 2*2 + 2*4
```

### Conftest file

We can create a `conftest.py` file inside `tests/` folder to "fixture" global values for our all tests files.

```python
# tests/conftest.py
import pytest
import source.shapes as shapes

@pytest.fixture
def rectangle():
    return shapes.Rectangle(2, 4)
```

So we can edit the `tests/test_rectangle.py` to:

```python
# tests/test_rectangle.py
def test_area(rectangle):
    assert rectangle.area() == 2 * 4

def test_perimeter(rectangle):
    assert rectangle.perimeter() == 2*2 + 2*4
```

## Mark and Parametrize

Documentations: https://docs.pytest.org/en/latests/how-to/mark.html, https://pytest-with-eric.com/hooks/pytest-configure/

We can mark our test with an additional info with **marks**.

You can see all **markers** available with the command `pytest --markers`

```shell
(venv) $ pytest --markers
# @pytest.mark.slow: marks tests as slow (deselect with `-m "not slow"`)
# ...
```

### Mark skip

> @pytest.mark.skip(reason=None): skip the given test function with an optional reason. Example: skip(reason="no way of currently testing this") skips the test.

```python
# tests/functions.py
import pytest
import time

@pytest.mark.skip(reason="This feature is currently broken")
def test_add():
    assert 1 + 2 == 2 + 1
```

The test will be skiped that test, because it has a mark `skip`, you can see a `s` in the output test file, and indicate with a `skipped` text how many test was skipped.

```python
(env) $ pytest
# ...
# tests/test_functions.py s.
# ...
# ====== 4 passed, 1 skipped in 7.02s ======
```

### Custom mark

We can create a custom marks, editing the file `conftest.py` adding a function `pytest_configure(config)` and using `config.addinivalue_line()` to add a new marker name.

```python
# tests/conftest.py
import pytest
import source.shapes as shapes


@pytest.fixture
def rectangle():
    return shapes.Rectangle(2, 4)

def pytest_configure(config):
    config.addinivalue_line('markers', 'slow: marks tests as slow (deselect with `-m \"not slow\"`)')
```

Now you can add `@pytest.mark.slow` decorator to mark a _slow_ test function.

```python
# tests/test_functions.py
import pytest
import time

@pytest.mark.skip(reason="This feature is currently broken")
def test_add():
    assert 1 + 2 == 2 + 1

@pytest.mark.slow # reference: https://docs.pytest.org/en/latests/how-to/mark.html
def test_very_slow():
    time.sleep(7)
    assert 1 + 2 == 2 + 1
```

With markers, **you can choose only specific tests with a mark name to run**, for example:

```python
(venv) $ pytest -m slow
# ...
# ===== 1 passed, 4 deselected in 7.02s =====
```

Pytest indicate with `deselected` all tests that **not has the mark slow** and not executed.

And you can run all tests except specific marked tests with prefix `not mark_name`

```shell
(venv) $ pytest -m "not slow"
# ...
# ===== 3 passed, 1 skipped, 1 deselected in 0.01s =====
```

Pytest indicate with `deselected` all tests that **has the mark slow** and execute all of others tests.

### Mark xfail

We can use a `@pytest.mark.xfail` decorator when we expect that test will be fail, it is used to test exceptions.

> @pytest.mark.xfail(condition, ..., *, reason=..., run=True, raises=None, strict=xfail_strict): mark the test function as an expected failure if any of the conditions evaluate to True. Optionally specify a reason for better reporting and run=False if you don't even want to execute the test function. If only specific exception(s) are expected, you can list them in raises, and if the test fails in other ways, it will be reported as a true failure. See https://docs.pytest.org/en/stable/reference/reference.html#pytest-mark-xfail


```python
# tests/test_functions.py
import pytest
...
@pytest.mark.xfail(reason="We know we cannot divide by zero")
def test_divide_by_zero():
    assert 7/0
```

And when we run the test, we can see an `x` in the output and a text `xfailed` indicate the tests

```shell
(venv) $ pytest -m "not slow"
# ...
# tests/test_functions.py sx
# ...
# ===== 3 passed, 1 skipped, 1 deselected, 1 xfailed in 0.02s =====
```


### Mark parametrize

> @pytest.mark.parametrize(argnames, argvalues): call a test function multiple times passing in different arguments in turn. argvalues generally needs to be a list of values if argnames specifies only one name or a list of tuples of values if argnames specifies multiple names. Example: @parametrize('arg1', [1,2]) would lead to two calls of the decorated test function, one with arg1=1 and another with arg1=2.see https://docs.pytest.org/en/stable/how-to/parametrize.html for more info and examples.

Parametrize allow us to check a test with multiple arguments as a values

```python
# tests/test_square.py
import pytest
import source.shapes as shapes

@pytest.mark.parametrize("side_length, expected_area", [(4, 16,), (5, 25), (6, 36)])
def test_multiple_square_areas(side_length, expected_area):
    assert shapes.Square(side_length).area() == expected_area

@pytest.mark.parametrize("side_length, expected_perimeter", [(2, 8), (4, 16), (9, 36)])
def test_multiple_square_permimeters(side_length, expected_perimeter):
    assert shapes.Square(side_length).perimeter() == expected_perimeter
```

And to test it

```shell
(venv) $ pytest tests/test_square.py
# tests/test_square.py ......                                                           [100%]
#
# ===================================== 6 passed in 0.01s =====================================

```


