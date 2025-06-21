# Unit tests for stdlib.py functions

import compiler.stdlib as stdlib
import math

def test_flow_and_measure(capsys):
    stdlib.flow("hello world")
    out, _ = capsys.readouterr()
    assert "hello world" in out
    assert stdlib.measure([1,2,3]) == 3
    assert stdlib.measure("abc") == 3
    assert stdlib.measure({"a":1, "b":2}) == 2

def test_map_and_filter():
    res = stdlib.map_basin([1,2,3], lambda x: x+1)
    assert res == [2,3,4]
    res = stdlib.filter_basin([1,2,3,4], lambda x: x%2==0)
    assert res == [2,4]

def test_reduce_and_math():
    res = stdlib.reduce_basin([1,2,3], lambda a,b: a+b, 0)
    assert res == 6
    assert stdlib.max_basin([1,8,3]) == 8
    assert stdlib.min_basin([1,8,3]) == 1
    assert stdlib.sum_basin([1,2,3]) == 6
    assert abs(stdlib.avg_basin([1,2,3]) - 2) < 1e-6

def test_string_utils():
    assert stdlib.upper_rivulet("abc") == "ABC"
    assert stdlib.lower_rivulet("ABC") == "abc"
    assert stdlib.strip_rivulet("  hi ") == "hi"
    assert stdlib.split_rivulet("a,b,c", ",") == ["a", "b", "c"]
    assert stdlib.join_basin(["x","y","z"], "-") == "x-y-z"

def test_numeric_utils():
    assert stdlib.abs_depth(-5) == 5
    assert stdlib.sqrt_depth(9) == 3
    assert abs(stdlib.log_depth(math.e) - 1) < 1e-6
    assert stdlib.pow_depth(2,3) == 8

def test_type_conversions():
    assert stdlib.to_rivulet(123) == "123"
    assert stdlib.to_depth("3.14") == 3.14
    assert stdlib.to_drop("true") is True
    assert stdlib.to_drop(0) is False

def test_random_and_now():
    val = stdlib.random_depth()
    assert 0 <= val <= 1
    assert stdlib.now() > 0