import pytest
from src.views import write_json_sob, write_json_gl

@pytest.fixture
def valid_date():
    return "2018-04-01 00:00:00"

def test_write_json_sob(valid_date):
    result = write_json_sob(valid_date)
    assert isinstance(result, dict), f"Ожидался JSON (dict), но получен {type(result)}"

def test_write_json_gl(valid_date):
    result = write_json_gl(valid_date)
    assert isinstance(result, dict), f"Ожидался JSON (dict), но получен {type(result)}"