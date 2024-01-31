import pytest
import source.shapes as shapes

@pytest.mark.parametrize("side_length, expected_area", [(4, 16,), (5, 25), (6, 36)])
def test_multiple_square_areas(side_length, expected_area):
    assert shapes.Square(side_length).area() == expected_area

@pytest.mark.parametrize("side_length, expected_perimeter", [(2, 8), (4, 16), (9, 36)])
def test_multiple_square_permimeters(side_length, expected_perimeter):
    assert shapes.Square(side_length).perimeter() == expected_perimeter