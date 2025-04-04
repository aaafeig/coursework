import pytest

@pytest.fixture
def sample_transactions():
    return [
        {"category": "food", "amount": 100, "date": "2024-03-01"},
        {"category": "transport", "amount": 50, "date": "2024-03-02"}
    ]