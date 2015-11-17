import pytest 


def test_empty_args(argparser):
    argparser.parse_args([])


def test_help_short(argparser):
    with pytest.raises(SystemExit) as excinfo:
        argparser.parse_args(['-h'])
    assert excinfo.value == 0


def test_help_long(argparser):
    with pytest.raises(SystemExit) as excinfo:
        argparser.parse_args(['--help'])
    assert excinfo.value == 0