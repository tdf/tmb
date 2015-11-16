def test_botloop(event_loop, monkeypatch):
    from tmb.tdfmonitoringbot import botloop
    from telegram import Bot
    def mockreturn(*args, **kwargs):
    	class Container:
    		pass
    	class Update:
    		def __init__(self, update_id, chat_id, text):
    			self.update_id = update_id
    			self.message = Container()
    			self.message.chat = Container()
    			self.message.chat.id = chat_id
    			self.message.text = text
    	return [Update(41, 141, '/start'),Update(42, 142, '/start')]
    monkeypatch.setattr(Bot, 'getUpdates', mockreturn)
    bot = Bot(token="test")
    event_loop.run_until_complete(botloop(bot))

