import logging
from example_service_templete_core.utils import check_number_input
from example_service_templete_service.version import __version__
from example_service_templete_service.constants import *
from example_service_templete_foundation.configuration_manager import ConfigurationManager, ConfigurationMixin



logger = logging.getLogger(__name__)

__all__ = (
    'DlExampleService',
)


class DlExampleService(ConfigurationMixin):
    def __init__(self, config: ConfigurationManager = None) -> None:
        self.load_config(config=config, default_location=DEFAULT_CONFIG_PATH)

    def add(self,data) -> float:

        sum = 0
        print(data)

        print(f"We have {check_number_input(data)} numbers of add")
        for i in data:
            sum += i
            print(sum)

        print(f"Version of the service: {__version__}")
        return sum
