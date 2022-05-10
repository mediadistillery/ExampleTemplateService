"""Start the DL face clustering service from the command line."""
import argparse
import logging
import example_service_templete_service as service

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-p', '--port', type=int,
                        help='Specify the port to run the app on; evaluation order: '
                             'CLI argument -> YAML config -> code default ({})'.format(service.DEFAULT_SERVICE_PORT))
    parser.add_argument('-l', '--log-level', type=str, help='Log level to show',
                        choices=['debug', 'info', 'warning', 'error', 'critical'])
    parser.add_argument('-V', '--version', action='version', version=f'%(prog)s {service.__version__}')
    return parser.parse_args()


def run_cli() -> None:
    args = parse_args()
    service.run_app(port=args.port, log_level=args.log_level)


if __name__ == '__main__':
    service.run_app(port=service.DEFAULT_SERVICE_PORT)