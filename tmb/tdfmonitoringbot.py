#!/usr/bin/env python3
import asyncio
import configparser
import telegram


def writeconfig(conf):
    with open('tdfmonitoringbot.ini', 'w') as configfile:
        conf.write(configfile)


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

    def msg(self, msg):
        self.bot.sendMessage(self.chatid, msg)

    def parseMessage(self, message):
        if message.startswith("/"):
            return self.parseCommand(message[1:])
        elif self.state == "register":
            if message == self.password:
                self.msg("You are now registered.")
                self.state = "start"
            else:
                self.msg("This is unfortunately wrong. Please try again.")

    def parseCommand(self, command):
        if command == "start":
            self.state = 'start'
        elif command == "register":
            self.state = 'register'
            self.msg("Please send me the password to subscribe.")
        elif command == "unregister":
            self.state = 'unregister'
        elif command == "cancel":
            self.state = 'start'
            del self



def parseUpdate(update):
    if update.message.text == "/register 33clLaeskedrik.":
        config['registered'][str(update.message.chat.id)] = 'True'
        writeconfig(config)
        bot.sendMessage(update.message.chat.id, "You are now getting the finest of monitoring notifications.")
    elif update.message.text.startswith("/register"):
        bot.sendMessage(update.message.chat.id, "My password lies in my source.".format(update.message.chat.first_name))
    elif update.message.text.startswith("/unregister"):
        if str(update.message.chat.id) in config['registered']:
            config.remove_option("registered", str(update.message.chat.id))
            writeconfig(config)
            bot.sendMessage(update.message.chat.id, "I'm so sorry you leave us, {}".format(update.message.chat.first_name))
        else:
            bot.sendMessage(update.message.chat.id, "Seems as if you are not registered, so your command doesn't make any sense :(")
    else:
        bot.sendMessage(update.message.chat.id, "Sorry {}, I don't understand you.".format(update.message.chat.first_name))

@asyncio.coroutine
def botloop():
    while True:
        updates = bot.getUpdates(offset=int(config['global']['update_id'])+1, timeout=10)
        if len(updates):
            config['global']['update_id'] = str(updates[-1].update_id)
            writeconfig(config)
        for update in updates:
            parseUpdate(update)
        yield from asyncio.sleep(5)


@asyncio.coroutine
def monitoringloop(reader, writer):
    data = yield from reader.read()
    message = data.decode()
    for key in config['registered']:
        bot.sendMessage(key, message)
    writer.close()

def main():
    global config
    config = configparser.ConfigParser()
    config['global'] = {'update_id': 0}
    config['registered'] = {}
    config.read(['tdfmonitoringbot.ini',])
    global bot 
    bot = telegram.Bot(token=config['global']['token'])
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(monitoringloop, '127.0.0.1', 64321, loop=loop)
    server = loop.run_until_complete(coro)
    try:
        bot = loop.run_until_complete(botloop())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
 
if __name__ == '__main__':
    main()