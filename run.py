import argparse
import logging

logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s', level=logging.DEBUG)
logger = logging.getLogger('runner')


from src.acquire import acquire
from src.initialize import initialize

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run components of the source code")
    subparsers = parser.add_subparsers()

    # ACQUIRE subparser
    sp_acq = subparsers.add_parser("acquire", description="Grab relevant links from Messages app")
    sp_acq.add_argument('--config', help='path to yaml file with configurations')
    sp_acq.add_argument('--input', default=None, help="Path to chat.db, found in ~/Library/Messages")
    sp_acq.add_argument('--output', default=None, help='Path to where the output should be saved to (optional')
    sp_acq.set_defaults(func=acquire)

    # FEATURE subparser
    sb_features = subparsers.add_parser("initialize", description="Create and populate database")
    sb_features.add_argument('--config', help='path to yaml file with configurations')
    sb_features.add_argument('--input', default=None, help="Path to txt file with links and timestamps")
    sb_features.add_argument('--output', default=None, help='Path to where the output db should be saved to (optional')
    sb_features.set_defaults(func=initialize)


    args = parser.parse_args()
    args.func(args)