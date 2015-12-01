import argparse


def create_parser():
    parser = argparse.ArgumentParser(
            prog="tmb",
            description="A monitoring bot for Telegram",
        )
    # parser.add_argument('-c', '--config', default=None, dest="config", help="path to the config file")
    return parser
