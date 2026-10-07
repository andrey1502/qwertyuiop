import pytest
from unittest.mock import patch, MagicMock
from osint_tool.main import Site, Condition


@pytest.fixture
def sample_site():
    return Site(
        url="https://example.com/{}",
        found_conditions=[Condition('code', [200])],
        not_found_conditions=[Condition('code', [404])]
    )


@patch('requests.get')
def test_site_returns_found_when_found_condition_met(mock_get, sample_site):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    status = sample_site.check_username('valid_user')

    mock_get.assert_called_once_with('https://example.com/valid_user')
    assert status == 'found'


@patch('requests.get')
def test_site_returns_not_found_when_not_found_condition_met(mock_get, sample_site):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    status = sample_site.check_username('missing_user')

    mock_get.assert_called_once_with('https://example.com/missing_user')
    assert status == 'not_found'


@patch('requests.get')
def test_site_returns_unknown_when_no_conditions_met(mock_get, sample_site):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    status = sample_site.check_username('some_user')

    mock_get.assert_called_once_with('https://example.com/some_user')
    assert status == 'unknown'