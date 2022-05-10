import logging
import os

import prometheus_client as prometheus
from example_service_templete_service.constants import DEFAULT_CONFIG_PATH, DEFAULT_PROMETHEUS_PORT
from example_service_templete_foundation.configuration_manager import ConfigurationManager
#from md_foundation.config.configuration_manager import ConfigurationManager

logger = logging.getLogger(__name__)

__all__ = (
    'initialize_configuration',
    'initialize_prometheus',
)


def initialize_configuration() -> ConfigurationManager:
    config_path = os.getenv('REMOTE_CONFIG_URL', DEFAULT_CONFIG_PATH)
    return ConfigurationManager.from_path(config_path)


def initialize_prometheus(config: ConfigurationManager) -> None:
    if config.get('prometheus.enabled', False):
        prometheus_port = config.get('prometheus.port', DEFAULT_PROMETHEUS_PORT)
        logger.info(f'Starting prometheus client on port {prometheus_port}')
        prometheus.start_http_server(prometheus_port)
    else:
        logger.info('Prometheus client is not configured.')