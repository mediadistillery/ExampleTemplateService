import logging

import fastapi
import uvicorn
from example_template_foundation.logger import set_logging

from example_template_service.api_v1.example_service import (
    example_service_router as router_v1,
)
from example_template_service.constants import (
    API_VERSION_PREFIX,
    DEFAULT_LOG_LEVEL,
    DEFAULT_SERVICE_PORT,
    LOCALHOST,
    PROJECT_DESCRIPTION,
    PROJECT_NAME,
)
from example_template_service.utils import (
    initialize_configuration,
    initialize_prometheus,
)
from example_template_service.version import __version__

logger = logging.getLogger(__name__)

__all__ = ('run_app',)


def on_shutdown() -> None:
    logger.info('Killing app')
    logger.info('Goodbye!')


app = fastapi.FastAPI(title=PROJECT_NAME, version=__version__, description=PROJECT_DESCRIPTION)
app.include_router(router_v1, prefix=API_VERSION_PREFIX)
app.add_event_handler('shutdown', on_shutdown)


@app.get('/health')
async def health() -> dict:
    return {'status': 'OK'}


@app.get('/version')
async def version() -> dict:
    return {'version': __version__}


def run_app(port: int = None, log_level: str = None) -> None:
    config = initialize_configuration()
    port = port or config.get('exampleservicetemplateservice.port', DEFAULT_SERVICE_PORT)
    host = config.get('exampleservicetemplateservice.hostName', LOCALHOST)
    log_file = config.get('exampleservicetemplateservice.logFile')
    fastapi_log_level = config.get('fastapi.logLevel')
    log_level = log_level or config.get('exampleservicetemplateservice.logLevel', DEFAULT_LOG_LEVEL)

    set_logging(filepath=log_file, level=log_level, multithreaded=True)
    logging.getLogger('multipart.multipart').setLevel(logging.WARNING)

    initialize_prometheus(config)

    logger.info(f'Starting app on {host}:{port}')
    uvicorn.run(app, host=host, port=port, log_level=fastapi_log_level)


if __name__ == '__main__':
    run_app(log_level='debug')
