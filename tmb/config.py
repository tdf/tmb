import configparser
import os

configfile = os.path.expanduser('~/.config/tmb/tmb.ini')
config = configparser.ConfigParser()
config['global'] = {'update_id': '0',
                    'token': 'invalid',
                    'host': '127.0.0.1',
                    'port': '64321',
                    'password': 'changeme'}
config['registered'] = {}


def readconfig():
    config.read([configfile, ])


def writeconfig(conf=config):
    configdir = os.path.dirname(configfile)
    if not os.path.isdir(configdir):
        os.makedirs(configdir, exist_ok=True)
    with open(configfile, 'w') as f:
        conf.write(f)


readconfig()
