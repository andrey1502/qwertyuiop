import pytest
from unittest.mock import MagicMock
from osint_tool.condition import Condition, AND, OR, NOT


# --- Тесты базового Condition ---

def test_condition_code():
    response = MagicMock()
    response.status_code = 200

    cond_match = Condition('code', [200, 301])
    cond_mismatch = Condition('code', [404])

    assert cond_match.check(response) is True
    assert cond_mismatch.check(response) is False


def test_condition_text():
    response = MagicMock()
    response.text = "User not found"

    cond_match = Condition('text', ['not found'])
    cond_mismatch = Condition('text', ['Welcome'])

    assert cond_match.check(response) is True
    assert cond_mismatch.check(response) is False


def test_condition_url():
    response = MagicMock()
    response.url = "https://github.com/404"

    cond_match = Condition('url', ["https://github.com/404"])
    cond_mismatch = Condition('url', ["https://github.com/user"])

    assert cond_match.check(response) is True
    assert cond_mismatch.check(response) is False


def test_condition_unknown_type_raises_exception():
    response = MagicMock()
    cond = Condition('invalid', [])

    with pytest.raises(Exception) as exc_info:
        cond.check(response)

    assert "Unknown condition type: invalid" in str(exc_info.value)


# --- Тесты для AND ---

def test_and_condition():
    response = MagicMock(status_code=200, text="Profile page")

    code_200 = Condition('code', [200])
    has_text = Condition('text', ['Profile'])
    no_text = Condition('text', ['404'])

    # True AND True -> True
    assert AND(code_200, has_text).check(response) is True

    # True AND False -> False
    assert AND(code_200, no_text).check(response) is False


# --- Тесты для OR ---

def test_or_condition():
    response = MagicMock(status_code=404, text="Page missing")

    code_200 = Condition('code', [200])
    code_404 = Condition('code', [404])
    has_text = Condition('text', ['missing'])

    # False OR True -> True
    assert OR(code_200, code_404).check(response) is True

    # True OR True -> True
    assert OR(code_404, has_text).check(response) is True

    # False OR False -> False
    assert OR(code_200, Condition('text', ['Welcome'])).check(response) is False


# --- Тесты для NOT ---

def test_not_condition():
    response = MagicMock(status_code=200)

    code_200 = Condition('code', [200])
    code_404 = Condition('code', [404])

    # NOT True -> False
    assert NOT(code_200).check(response) is False

    # NOT False -> True
    assert NOT(code_404).check(response) is True


# --- Комплексные вложенные условия ---

def test_nested_composite_conditions():
    # Пример: статус 200 И (текст содержит "Dashboard" ИЛИ НЕ содержит "Login")
    response = MagicMock(status_code=200, text="Welcome to Dashboard")

    is_200 = Condition('code', [200])
    has_dashboard = Condition('text', ['Dashboard'])
    has_login = Condition('text', ['Login'])

    complex_condition = AND(
        is_200,
        OR(has_dashboard, NOT(has_login))
    )

    assert complex_condition.check(response) is True