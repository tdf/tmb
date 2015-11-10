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
