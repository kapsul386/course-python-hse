from controllers import operation


def test_operation_ints():
    assert operation(2, 3) == 5


def test_operation_floats():
    assert operation(2.5, 0.5) == 3.0
