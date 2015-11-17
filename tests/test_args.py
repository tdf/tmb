import pytest 


def test_empty_args(argparser):
    argparser.parse_args([])


def test_help_short(argparser):
    with pytest.raises(SystemExit):
        argparser.parse_args(['-h'])

def test_help_long(argparser):
    with pytest.raises(SystemExit):
        argparser.parse_args(['--help'])