import pytest
from unittest.mock import MagicMock
from osint_tool.condition import Condition
from osint_tool.site import Site


@pytest.fixture
def sample_site():
    return Site(
        url="https://example.com/{}",
        found_conditions=[Condition('code', [200])],
        not_found_conditions=[Condition('code', [404])]
    )


@pytest.fixture
def mock_client():
    """Создаёт фейковый HTTPClient для всех тестов."""
    return MagicMock()


def test_check_username_returns_found(sample_site, mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_client.get.return_value = mock_response

    status = sample_site.check_username('valid_user', client=mock_client)

    # Проверяем, что клиент вызвал get с правильным сформированным URL
    mock_client.get.assert_called_once_with('https://example.com/valid_user')
    assert status == 'found'


def test_check_username_returns_not_found(sample_site, mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_client.get.return_value = mock_response

    status = sample_site.check_username('missing_user', client=mock_client)

    mock_client.get.assert_called_once_with('https://example.com/missing_user')
    assert status == 'not_found'


def test_check_username_returns_unknown(sample_site, mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_client.get.return_value = mock_response

    status = sample_site.check_username('unexpected_status_user', client=mock_client)

    mock_client.get.assert_called_once_with('https://example.com/unexpected_status_user')
    assert status == 'unknown'