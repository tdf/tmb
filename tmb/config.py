import configparser
import os

configfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tdfmonitoringbot.ini')
config = configparser.ConfigParser()
config['global'] = {'update_id': 0}
config['registered'] = {}


def readconfig():
    config.read([configfile, ])


def writeconfig(conf=config):
    with open(configfile, 'w') as f:
        conf.write(f)


readconfig()
