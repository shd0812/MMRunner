from mlib.m_task import run
from mlib.load_case import TestLoad


result = TestLoad.load_file('../data/test_one/sxs_api.yaml')

run(result)