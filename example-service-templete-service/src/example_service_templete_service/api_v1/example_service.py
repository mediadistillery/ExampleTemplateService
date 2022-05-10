import gc
import logging
import os
from typing import List

import psutil
from fastapi import APIRouter

from example_service_templete_service.metrics import metrics
from example_service_templete_service.service import DlExampleService
from example_service_templete_service.utils import initialize_configuration

logger = logging.getLogger(__name__)


__all__ = (
    'example_service_router',
)

service: DlExampleService


def on_startup() -> None:
    """Lazy loading of the service to avoid loading models too soon."""
    global service
    config = initialize_configuration()
    service = DlExampleService(config=config)



example_service_router = APIRouter()
example_service_router.add_event_handler('startup', on_startup)


def memory_usage():
    return psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2



@example_service_router.post('/example/sum', tags=['sum'])
async def addition(inputs: List[float]):

    logger.info(f'Received addition request (service)')
    metrics.called('/example/sum')
    try:
        response = service.add(data=inputs)
        gc.collect()
    except Exception:
        metrics.call_failed('/example/sum')
        raise

    logger.debug(f"Memory:\t {int(memory_usage())} MB")
    logger.debug(f"Returning response {response}")

    return response
