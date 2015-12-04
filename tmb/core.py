#!/usr/bin/env python3
import asyncio
import telegram
import tmb
import tmb.args
from tmb.config import config, writeconfig
from telegram.error import TelegramError

class MetaChat(type):
    _instances = {}

    def __call__(cls, chatid, *args, **kwargs):
        if chatid not in cls._instances:
            instance =  super().__call__(chatid, *args, **kwargs)
            cls._instances[chatid] = instance
            return instance    
        return cls._instances[chatid]


class ActiveChat(metaclass=MetaChat):
    password = None
    config = None

    def __init__(self, chatid, bot):
        self.chatid = chatid
        self.state = 'start'
        self.bot = bot
        if not self.password:
            self.password = config['global']['password']

    def msg(self, msg):
        self.bot.sendMessage(self.chatid, msg)

    def parseMessage(self, message):
        if message.startswith("/"):
            return self.parseCommand(message[1:])
        elif self.state == "register":
            if message == self.password:
                config['registered'][str(self.chatid)] = 'True'
                writeconfig()
                self.msg("You are now registered.")
                self.state = "start"
            else:
                self.msg("This is unfortunately wrong. Please try again.")
        elif self.state == "unregister":
            if message == "confirm":
                if str(self.chatid) in config['registered']:
                    config.remove_option("registered", str(self.chatid))
                    writeconfig()
                    self.msg("You are now unsubscribed.")
                    self.state = "start"
                else:
                    self.msg("You are not registered.")
                    self.state = "start"

    def parseCommand(self, command):
        if command == "start":
            self.state = 'start'
        elif command == "register":
            self.state = 'register'
            self.msg("Please send me the password to subscribe.")
        elif command == "unregister":
            self.state = 'unregister'
            self.msg("Please write 'confirm' to continue unsubscription.")
        elif command == "cancel":
            self.state = 'start'
            del self


def parseUpdate(update, bot):
    a = ActiveChat(update.message.chat.id, bot)
    a.parseMessage(update.message.text)


@asyncio.coroutine
def botloop(bot):
    while True:
        try:
            updates = bot.getUpdates(offset=int(config['global']['update_id'])+1, timeout=10)
        except TelegramError as e:
            if "Timed out" in str(e):
                continue
        if len(updates):
            config['global']['update_id'] = str(updates[-1].update_id)
            writeconfig()
        for update in updates:
            parseUpdate(update, bot)
        yield from asyncio.sleep(5)
        if tmb.called_from_test:
            break


@asyncio.coroutine
def monitoringloop(reader, writer):
    data = yield from reader.read()
    message = data.decode()
    bot = telegram.Bot(token=config['global']['token'])
    for key in config['registered']:
        bot.sendMessage(key, message)
    writer.close()


def main(): # pragma: no cover
    parser = tmb.args.create_parser()
    parser.parse_args()
    bot = telegram.Bot(token=config['global']['token'])
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(monitoringloop, config['global']['host'], config['global']['port'], loop=loop)
    server = loop.run_until_complete(coro)
    try:
        loop.run_until_complete(botloop(bot))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
