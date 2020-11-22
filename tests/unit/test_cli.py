from unittest.mock import patch


def test_result_noninteractive():
    from katcr import Result
    res = Result(['a' * 20, 'b' * 20], False)
    assert str(res) == 'aaaaaaaaaaaaaaaaaaaa | bbbbbbbbbbbbbbbbbbbb'


@patch('katcr.MAX_SIZE', 5)
def test_result_ninteractive():
    from katcr import Result
    res = Result(['a' * 20, 'b' * 20], True)
    assert str(res) == 'aaaaa'


@patch('subprocess.check_call')
def test_result_open(spmock):
    from katcr import Result
    res = Result(['a' * 20, 'b' * 20], True)
    res.open()
    spmock.assert_called_with(['xdg-open', 'b' * 20])


class FakeEngines:
    class fake:
        async def search(*args, **kwargs):
            return []


def test_search_cmd():
    from cleo import CommandTester
    from katcr import CLICommand
    from cleo import Application
    from katcr.engines.base import BaseSearch

    import katcr
    katcr.engines = FakeEngines

    assert CLICommand().logger is None
    application = Application()
    application.add(CLICommand())

    command_tester = CommandTester(application.find('search'))
    command_tester.execute('search --engine fake asdf')
    assert BaseSearch.logger
    assert BaseSearch.config
    assert BaseSearch.session
