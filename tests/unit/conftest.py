"""Fixtures."""


def robobrowser():
    """Return a robobrowser mock."""
    import unittest.mock
    from robobrowser import RoboBrowser
    return unittest.mock.MagicMock(spec=RoboBrowser)
