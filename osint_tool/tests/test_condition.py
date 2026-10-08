import pytest
from unittest.mock import MagicMock
from osint_tool.condition import Condition, AND, OR, NOT


# --- Базовые тесты Condition ---

def test_condition_code():
    response = MagicMock(status_code=200)
    cond = Condition('code', [200, 301])
    assert cond.check(response) is True

    response.status_code = 404
    assert cond.check(response) is False


def test_condition_text():
    response = MagicMock(text="User profile found")
    cond = Condition('text', ['profile'])
    assert cond.check(response) is True

    response.text = "Not found"
    assert cond.check(response) is False


def test_condition_url():
    response = MagicMock(url="https://github.com/404")
    cond = Condition('url', ["https://github.com/404"])
    assert cond.check(response) is True


def test_condition_unknown_type_raises_exception():
    response = MagicMock()
    cond = Condition('invalid_type', [])
    with pytest.raises(Exception) as exc_info:
        cond.check(response)
    assert "Unknown condition type: invalid_type" in str(exc_info.value)


# --- Логические операторы (*args) ---

def test_and_condition_with_multiple_args():
    response = MagicMock(status_code=200, text="Profile")
    c1 = Condition('code', [200])
    c2 = Condition('text', ['Profile'])
    c3 = Condition('text', ['404'])

    # True AND True AND True -> True
    assert AND(c1, c2).check(response) is True
    # True AND True AND False -> False
    assert AND(c1, c2, c3).check(response) is False


def test_or_condition_with_multiple_args():
    response = MagicMock(status_code=404, text="Missing")
    c1 = Condition('code', [200])
    c2 = Condition('code', [404])
    c3 = Condition('text', ['Missing'])

    # False OR True OR True -> True
    assert OR(c1, c2, c3).check(response) is True
    # False OR False -> False
    assert OR(c1, Condition('text', ['Profile'])).check(response) is False


def test_not_condition():
    response = MagicMock(status_code=200)
    c1 = Condition('code', [200])

    assert NOT(c1).check(response) is False