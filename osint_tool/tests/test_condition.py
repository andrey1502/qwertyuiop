import pytest
from unittest.mock import MagicMock
from osint_tool.main import Condition


# --- Тесты для типа 'code' ---

def test_condition_code_returns_true_when_matched():
    mock_response = MagicMock()
    mock_response.status_code = 200

    condition = Condition('code', [200, 301])
    assert condition.check(mock_response) is True


def test_condition_code_returns_false_when_not_matched():
    mock_response = MagicMock()
    mock_response.status_code = 404

    condition = Condition('code', [200, 301])
    assert condition.check(mock_response) is False


# --- Тесты для типа 'text' ---

def test_condition_text_returns_true_when_substring_present():
    mock_response = MagicMock()
    mock_response.text = "Error: User not found in database."

    condition = Condition('text', ['User not found'])
    assert condition.check(mock_response) is True


def test_condition_text_returns_false_when_substring_absent():
    mock_response = MagicMock()
    mock_response.text = "Welcome to user profile!"

    condition = Condition('text', ['User not found'])
    assert condition.check(mock_response) is False


# --- Тесты для типа 'url' ---

def test_condition_url_returns_true_when_matched():
    mock_response = MagicMock()
    mock_response.url = "https://github.com/404"

    condition = Condition('url', ["https://github.com/404"])
    assert condition.check(mock_response) is True


def test_condition_url_returns_false_when_not_matched():
    mock_response = MagicMock()
    mock_response.url = "https://github.com/andrey1502"

    condition = Condition('url', ["https://github.com/404"])
    assert condition.check(mock_response) is False


# --- Граничный случай ---

def test_condition_raises_exception_on_unknown_type():
    mock_response = MagicMock()
    condition = Condition('unsupported_type', [123])

    with pytest.raises(Exception) as exc_info:
        condition.check(mock_response)

    assert "Unknown condition type: unsupported_type" in str(exc_info.value)