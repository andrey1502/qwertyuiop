import pytest
from unittest.mock import MagicMock
from osint_tool.check import WebCheck
from osint_tool.condition import Condition, AND, NOT


@pytest.fixture
def mock_client():
    return MagicMock()


def test_web_check_returns_found(mock_client):
    response = MagicMock(status_code=200)
    mock_client.get.return_value = response

    web_check = WebCheck(
        url="https://example.com/{}",
        found_conditions=[Condition('code', [200])],
        not_found_conditions=[Condition('code', [404])],
        client=mock_client
    )

    result = web_check.check_username("user1")

    mock_client.get.assert_called_once_with("https://example.com/user1")
    assert result == 'found'


def test_web_check_returns_not_found(mock_client):
    response = MagicMock(status_code=404)
    mock_client.get.return_value = response

    web_check = WebCheck(
        url="https://example.com/{}",
        found_conditions=[Condition('code', [200])],
        not_found_conditions=[Condition('code', [404])],
        client=mock_client
    )

    result = web_check.check_username("missing_user")

    mock_client.get.assert_called_once_with("https://example.com/missing_user")
    assert result == 'not_found'


def test_web_check_returns_unknown(mock_client):
    response = MagicMock(status_code=500)
    mock_client.get.return_value = response

    web_check = WebCheck(
        url="https://example.com/{}",
        found_conditions=[Condition('code', [200])],
        not_found_conditions=[Condition('code', [404])],
        client=mock_client
    )

    result = web_check.check_username("server_error_user")
    assert result == 'unknown'