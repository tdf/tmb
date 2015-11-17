def test_botloop(event_loop, monkeypatch):
    from tmb.core import botloop
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


def test_monitoringloop(event_loop, monkeypatch):
    from tmb.core import monitoringloop
    import tmb.core
    from telegram import Bot
    import asyncio

    def mockreturn(*args, **kwargs):
        return

    class MockReader:
        message = b''

        @asyncio.coroutine
        def read(self):
            return self.message

    class MockWriter:
        closed = False

        def close(self):
            self.closed = True

    monkeypatch.setattr(Bot, 'sendMessage', mockreturn)
    tmb.core.bot = Bot(token="test")
    event_loop.run_until_complete(monitoringloop(MockReader(), MockWriter()))

