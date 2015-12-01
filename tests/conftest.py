import pytest


class TestBot:
    lastmessage = None
    lastchatid = None

    def sendMessage(self, chatid, message):
        self.lastmessage = message
        self.lastchatid = chatid
        print(chatid, message)


@pytest.fixture
def activechat():
    import tmb.core
    tmb.core.ActiveChat.password = "password"
    return tmb.core.ActiveChat


@pytest.fixture
def testbot():
    return TestBot()


@pytest.fixture
def argparser():
    import tmb.args
    return tmb.args.create_parser()


def pytest_configure(config):
    import tmb, tmb.config, os
    tmb.config.configfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tmb.ini')
    tmb.config.readconfig()
    tmb.called_from_test = True


def pytest_unconfigure(config):
    import tmb
    tmb.called_from_test = False
