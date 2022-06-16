import logging
from typing import List

from fastapi import APIRouter

from example_template_service.metrics import metrics
from example_template_service.service import DlExampleService
from example_template_service.utils import initialize_configuration

logger = logging.getLogger(__name__)


__all__ = ('example_service_router',)

service: DlExampleService


def on_startup() -> None:
    """Lazy loading of the service to avoid loading models too soon."""
    global service
    config = initialize_configuration()
    service = DlExampleService(config=config)


example_service_router = APIRouter()
example_service_router.add_event_handler('startup', on_startup)


@example_service_router.post('/example/sum', tags=['sum'])
async def addition(inputs: List[float]):

    logger.info(f'Received addition request (service)')
    metrics.called('/example/sum')
    try:
        response = service.add(data=inputs)
    except Exception:
        metrics.call_failed('/example/sum')
        raise

    logger.debug(f"Returning response {response}")

    return response


@example_service_router.get('/example/version', tags=['version'])
async def addition():

    logger.info(f'Received addition request (service)')
    metrics.called('/example/version')
    try:
        response = service.version()
    except Exception:
        metrics.call_failed('/example/version')
        raise

    logger.debug(f"Returning response {response}")

    return response
