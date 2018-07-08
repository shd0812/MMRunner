# encoding: utf-8

"""
Built-in dependent functions used in YAML/JSON testcases.
"""

import datetime
import json
import os
import random
import re
import string
import time
import string

from mlib.m_expection  import ParamsError



""" built-in functions
"""
def gen_random_string(str_len):
    """ generate random string with specified length
    """
    return ''.join(
        random.choice(string.ascii_letters + string.digits) for _ in range(str_len))

def get_timestamp(str_len=13):
    """ get timestamp string, length can only between 0 and 16
    """
    if isinstance(str_len, int) and 0 < str_len < 17:
        return str(time.time()).replace(".", "")[:str_len]

    raise ParamsError("timestamp length can only between 0 and 16.")

def get_current_date(fmt="%Y-%m-%d"):
    """ get current date, default format is %Y-%m-%d   %H:%M:%S current_time
    """
    return datetime.datetime.now().strftime(fmt)


""" built-in comparators
"""
def equals(check_value, expect_value):
    assert check_value == expect_value

def less_than(check_value, expect_value):
    assert check_value < expect_value

def less_than_or_equals(check_value, expect_value):
    assert check_value <= expect_value

def greater_than(check_value, expect_value):
    assert check_value > expect_value

def greater_than_or_equals(check_value, expect_value):
    assert check_value >= expect_value

def not_equals(check_value, expect_value):
    assert check_value != expect_value

def string_equals(check_value, expect_value):
    assert str(check_value) == str(expect_value)

def length_equals(check_value, expect_value):
    assert isinstance(expect_value, int)
    assert len(check_value) == expect_value

def length_greater_than(check_value, expect_value):
    assert isinstance(expect_value, int)
    assert len(check_value) > expect_value

def length_greater_than_or_equals(check_value, expect_value):
    assert isinstance(expect_value, int)
    assert len(check_value) >= expect_value

def length_less_than(check_value, expect_value):
    assert isinstance(expect_value, int)
    assert len(check_value) < expect_value

def length_less_than_or_equals(check_value, expect_value):
    assert isinstance(expect_value, int)
    assert len(check_value) <= expect_value

def contains(check_value, expect_value):
    assert isinstance(check_value, (list, tuple, dict, str))
    assert expect_value in check_value

def contained_by(check_value, expect_value):
    assert isinstance(expect_value, (list, tuple, dict, str))
    assert check_value in expect_value

def type_match(check_value, expect_value):
    def get_type(name):
        if isinstance(name, type):
            return name
        elif isinstance(name, str):
            try:
                return __builtins__[name]
            except KeyError:
                raise ValueError(name)
        else:
            raise ValueError(name)

    assert isinstance(check_value, get_type(expect_value))

def regex_match(check_value, expect_value):
    assert isinstance(expect_value, str)
    assert isinstance(check_value, str)
    assert re.match(expect_value, check_value)

def startswith(check_value, expect_value):
    assert str(check_value).startswith(str(expect_value))

def endswith(check_value, expect_value):
    assert str(check_value).endswith(str(expect_value))

""" built-in hooks
"""
def setup_hook_prepare_kwargs(request):
    if request["method"] == "POST":
        content_type = request.get("headers", {}).get("content-type")
        if content_type and "data" in request:
            # if request content-type is application/json, request data should be dumped
            if content_type.startswith("application/json") and isinstance(request["data"], (dict, list)):
                request["data"] = json.dumps(request["data"])

            if isinstance(request["data"], str):
                request["data"] = request["data"].encode('utf-8')

def sleep_N_secs(n_secs):
    """ sleep n seconds
    """
    time.sleep(n_secs)

def get_uniform_comparator(comparator):
    """ convert comparator alias to uniform name
    """
    if comparator in ["eq", "equals", "==", "is"]:
        return "equals"
    elif comparator in ["lt", "less_than"]:
        return "less_than"
    elif comparator in ["le", "less_than_or_equals"]:
        return "less_than_or_equals"
    elif comparator in ["gt", "greater_than"]:
        return "greater_than"
    elif comparator in ["ge", "greater_than_or_equals"]:
        return "greater_than_or_equals"
    elif comparator in ["ne", "not_equals"]:
        return "not_equals"
    elif comparator in ["str_eq", "string_equals"]:
        return "string_equals"
    elif comparator in ["len_eq", "length_equals", "count_eq"]:
        return "length_equals"
    elif comparator in ["len_gt", "count_gt", "length_greater_than", "count_greater_than"]:
        return "length_greater_than"
    elif comparator in ["len_ge", "count_ge", "length_greater_than_or_equals", \
        "count_greater_than_or_equals"]:
        return "length_greater_than_or_equals"
    elif comparator in ["len_lt", "count_lt", "length_less_than", "count_less_than"]:
        return "length_less_than"
    elif comparator in ["len_le", "count_le", "length_less_than_or_equals", \
        "count_less_than_or_equals"]:
        return "length_less_than_or_equals"
    else:
        return comparator

def do_validation(comparator_str,check_value,expect_value):
    if get_uniform_comparator(comparator_str) == 'equals':
        return equals(check_value,expect_value)
    elif get_uniform_comparator(comparator_str) =='less_than':
        return less_than(check_value,expect_value)
    elif get_uniform_comparator(comparator_str) == 'less_than_or_equals':
        return less_than_or_equals(check_value,expect_value)
    elif get_uniform_comparator(comparator_str) == 'greater_than':
        return greater_than(check_value,expect_value)
    elif get_uniform_comparator(comparator_str) == 'greater_than_or_equals':
        return greater_than_or_equals(check_value,expect_value)
    elif get_uniform_comparator(comparator_str) == 'not_equals':
        return not_equals(check_value,expect_value)
    elif get_uniform_comparator(comparator_str) == 'string_equals':
        return string_equals(check_value,expect_value)
    elif get_uniform_comparator(comparator_str) == 'length_equals':
        return length_equals(check_value,expect_value)
    elif get_uniform_comparator(comparator_str) == 'length_greater_than':
        return length_greater_than(check_value,expect_value)
    elif get_uniform_comparator(comparator_str) == 'length_greater_than_or_equals':
        return length_greater_than_or_equals(check_value,expect_value)
    elif get_uniform_comparator(comparator_str) == 'length_less_than':
        return length_less_than(check_value,expect_value)
    elif get_uniform_comparator(comparator_str) == 'length_less_than_or_equals':
        return length_less_than_or_equals(check_value,expect_value)
    else:
        raise ParamsError('not found comparator')


if __name__ == '__main__':
    print (do_validation('lts',3,2))




