import pytest
from unittest.mock import MagicMock
from osint_tool.site import Site


def test_site_check_username_returns_found_if_any_check_found():
    mock_check_1 = MagicMock()
    mock_check_1.check_username.return_value = 'not_found'

    mock_check_2 = MagicMock()
    mock_check_2.check_username.return_value = 'found'

    site = Site(name="TestSite", checks=[mock_check_1, mock_check_2])

    result = site.check_username("alex")

    mock_check_1.check_username.assert_called_once_with("alex")
    mock_check_2.check_username.assert_called_once_with("alex")
    assert result == 'found'


def test_site_check_username_returns_not_found():
    mock_check = MagicMock()
    mock_check.check_username.return_value = 'not_found'

    site = Site(name="TestSite", checks=[mock_check])

    assert site.check_username("missing_user") == 'not_found'


def test_site_check_username_returns_unknown():
    mock_check = MagicMock()
    mock_check.check_username.return_value = 'unknown'

    site = Site(name="TestSite", checks=[mock_check])

    assert site.check_username("some_user") == 'unknown'