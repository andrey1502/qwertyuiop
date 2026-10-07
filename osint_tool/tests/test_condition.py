import pytest
from unittest.mock import patch, MagicMock
from osint_tool.main import Site, Condition


@pytest.fixture
def sample_site():
    found = [Condition('code', [200])]
    not_found = [Condition('code', [404])]
    return Site(
        url="https://example.com/{}",
        found_conditions=found,
        not_found_conditions=not_found
    )


@patch('requests.get')
def test_check_username_found(mock_get, sample_site):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    result = sample_site.check_username('john_doe')

    mock_get.assert_called_once_with('https://example.com/john_doe')
    assert result == 'found'


@patch('requests.get')
def test_check_username_not_found(mock_get, sample_site):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    result = sample_site.check_username('non_existent_user')

    mock_get.assert_called_once_with('https://example.com/non_existent_user')
    assert result == 'not_found'


@patch('requests.get')
def test_check_username_unknown(mock_get, sample_site):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    result = sample_site.check_username('some_user')

    mock_get.assert_called_once_with('https://example.com/some_user')
    assert result == 'unknown'