import pytest

class TestBot():
	lastmessage = None
	lastchatid = None
	def sendMessage(self, chatid, message):
		self.lastmessage = message
		self.lastchatid = chatid
		print(chatid, message)

@pytest.fixture
def activechat():
    import tmb.tdfmonitoringbot
    tmb.tdfmonitoringbot.ActiveChat.password = "password"
    return tmb.tdfmonitoringbot.ActiveChat

@pytest.fixture
def testbot():
	return TestBot()

def pytest_configure(config):
    import tmb
    tmb._called_from_test = True

def pytest_unconfigure(config):
    import tmb
    del tmb._called_from_test