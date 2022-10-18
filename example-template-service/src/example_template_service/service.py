import logging
import json
from typing import Optional
from example_template_core.utils import check_number_input
from example_template_foundation.config.configuration_manager import (
    ConfigurationManager,
    ConfigurationMixin,
)
from example_template_core.service.object_detection_service import ObjectDetectionService

from example_template_service.constants import *
from example_template_service.version import __version__

import cv2
import numpy as np

logger = logging.getLogger(__name__)

__all__ = ('DlExampleService',)


class DlExampleService(ConfigurationMixin):
    def __init__(self, config: ConfigurationManager = None) -> None:
        self.load_config(config=config, default_location=DEFAULT_CONFIG_PATH)
        self.input_size = config.get('yolo.input_size', 416)
        self.object_detection_service = ObjectDetectionService(config=config)


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

    def detect(self, image: np.ndarray, allowed_classes: str = None, metadata: Optional[dict] = None) :

        img_np = cv2.imdecode(image, cv2.IMREAD_COLOR)  # cv2.IMREAD_COLOR in OpenCV 3.1
        original_image = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

        image_data = cv2.resize(original_image, (self.input_size, self.input_size))
        image_data = image_data / 255.
        images_data = []

        for i in range(1):
            images_data.append(image_data)

        images_data = np.asarray(images_data).astype(np.float32)
        detections = self.object_detection_service.detect(images_data, original_image,allowed_classes)
        return detections




