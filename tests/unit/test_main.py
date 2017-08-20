"""Base tests. Nothing related to plugins goes here."""


def test_basesearch():
    """Test basesearch has required methods."""
    import pytest
    import unittest.mock
    from katcr import BaseSearch

    assert hasattr(BaseSearch, "search")
    assert hasattr(BaseSearch, "search_magnets")

    with pytest.raises(NotImplementedError):
        BaseSearch().search_magnets("foo", 1)

    with unittest.mock.patch('katcr.BaseSearch.search_magnets',
                             side_effect=(['foo'],)) as mock:
        BaseSearch().search('foo', 2)
        assert mock.call_count == 2


def test_cli_help():
    """Test help call."""
    import subprocess
    from katcr import main
    result = subprocess.check_output(['katcr', '--help'])
    assert main.__doc__.encode() in result
