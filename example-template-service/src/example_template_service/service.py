import logging

from example_template_core.utils import check_number_input
from example_template_foundation.configuration_manager import (
    ConfigurationManager,
    ConfigurationMixin,
)

from example_template_service.constants import *
from example_template_service.version import __version__

logger = logging.getLogger(__name__)

__all__ = ('DlExampleService',)


class DlExampleService(ConfigurationMixin):
    def __init__(self, config: ConfigurationManager = None) -> None:
        self.load_config(config=config, default_location=DEFAULT_CONFIG_PATH)

    def add(self, data) -> float:
        sum = 0
        print(data)
        print(f"We have {check_number_input(data)} numbers to add")
        for i in data:
            sum += i
            print(sum)

        print(f"Version of the service: {__version__}")
        return sum

    def version(self) -> float:
        print(f"Version of the service: {__version__}")
        v = __version__
        return v
