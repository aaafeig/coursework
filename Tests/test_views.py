
from src.views import write_json_gl, write_json_sob


def test_write_json_gl():
    mock_time = "2024-03-28 00:00:00"
    write_json_gl(mock_time)


def test_write_json_sob():
    mock_date = "2024-03-03 00:00:00"
    mock_setting = "M"
    write_json_sob(mock_date, mock_setting)
