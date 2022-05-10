import logging
import time

import fastapi
import uvicorn


from example_service_templete_service.api_v1.example_service import example_service_router as router_v1
from example_service_templete_service.constants import LOCALHOST, PROJECT_NAME, API_VERSION_PREFIX, PROJECT_DESCRIPTION, \
    DEFAULT_SERVICE_PORT, DEFAULT_LOG_LEVEL
from example_service_templete_service.metrics import metrics
from example_service_templete_service.utils import initialize_prometheus, initialize_configuration
from example_service_templete_service.version import __version__

logger = logging.getLogger(__name__)

__all__ = (
    'run_app',
)


def on_shutdown() -> None:
    logger.info('Killing app')
    logger.info('Goodbye!')


app = fastapi.FastAPI(
    title=PROJECT_NAME,
    version=__version__,
    description=PROJECT_DESCRIPTION
)
app.include_router(router_v1, prefix=API_VERSION_PREFIX)
app.add_event_handler('shutdown', on_shutdown)



@app.get('/health')
async def health() -> dict:
    return {'status': 'OK'}


@app.get('/version')
async def version() -> dict:
    return {'version': __version__}


ROUTE_PATHS = [route.path for route in app.routes]


@app.middleware('http')
async def log_request_duration(request: fastapi.Request, call_next) -> fastapi.Response:
    tic = time.time()
    response = await call_next(request)
    toc = time.time()
    duration = toc - tic
    if request.url.path in ROUTE_PATHS:  # we don't want prometheus metrics for non-existing routes
        metrics.request_duration(request.url.path, duration)
    response.headers['X-Process-Time'] = str(duration)
    logger.debug(f'Total request time: {duration:.3f}s')
    return response


def run_app(port: int = None, log_level: str = None) -> None:
    config = initialize_configuration()
    port = port or config.get('faceClusteringWeb.port', DEFAULT_SERVICE_PORT)
    host = config.get('faceClusteringWeb.hostName', LOCALHOST)
    log_file = config.get('faceClusteringWeb.logFile')
    fastapi_log_level = config.get('fastapi.logLevel')
    log_level = log_level or config.get('faceClusteringWeb.logLevel', DEFAULT_LOG_LEVEL)

#    set_logging(filepath=log_file, level=log_level, multithreaded=True)
    logging.getLogger('multipart.multipart').setLevel(logging.WARNING)

    initialize_prometheus(config)

    logger.info(f'Starting app on {host}:{port}')
    uvicorn.run(app, host=host, port=port, log_level=fastapi_log_level)


if __name__ == '__main__':
    run_app(log_level='debug')
