import re
import os

from example_template_foundation.config.configuration_manager import ConfigurationManager
from example_template_foundation.storage.google_cloud import GoogleStorage
import tensorflow as tf
from example_template_core.save_model import Model_Converter
from absl.flags import FLAGS
from example_template_core.yolo.yolov4 import YOLO, decode, filter_boxes
import example_template_core.yolo.utils as utils


import logging


logger = logging.getLogger(__name__)


def get_model_version(filename):
    """
    model names should have the following structure:
    '0000_1594732917', where
    0000: denotes the version number
    1594732917: denotes the model creation timestamp
    """

    filestem = filename.split(".")[0]
    model_version = re.search(r'\d{4}_\d{10}$', filestem)
    if model_version is None:
        raise ValueError(f'Model filename {filename} does not have the correct structure! Correct structure should be: \n'
                         '{model_name}_{version_number}_{timestamp} \n'
                         'e.g.: aesthetic_0000_1594732917')
    return model_version.group()


class ModelsProvider:
    def __init__(self, config: ConfigurationManager):
        self.config = config
        self.storage_client_name = self.config.get('storage.client', 'gcloud')
        self._init_client(self.storage_client_name)
        self.enabled_models = self.config.get('models.enabledTypes')



        if not self.enabled_models:
            raise ValueError("No models enabled in configuration. Specify a list of enabled model types with key `models.enabledTypes`.")
        self.service_name = self.config.get('storage.serviceName')
        if not self.service_name:
            raise ValueError("No service name specified in configuration. Specify the service name with key storage.serviceName")

        self.destination_folder = self.config.get('models.location', f"/etc/{self.service_name}/models")

    def _init_client(self, storage_client='gcloud'):
        if storage_client == 'gcloud':
            self.storage_client = GoogleStorage(self.config.get('storage.key', '/etc/gcloud/key.json'))
        else:
            self.storage_client = "local"
            raise NotImplementedError('Currently only supported for gcloud')
        logger.info(f"Initialized ModelsProvider with storage client {storage_client}")

    def _get_blob_name(self, model_type, model_version, filename):
        return os.path.join(self.service_name, model_type, model_version, filename)

    def _get_file_destination(self, model_type, filename):
        destination_folder = os.path.join(self.destination_folder, model_type)
        destination_path = os.path.join(destination_folder, filename)
        return destination_path

    def get_model_path(self, model_type):
        filename = self.config.data[f'{model_type}.modelName']
        return self._get_file_destination(model_type, filename)

    def save_tf(self):
        STRIDES, ANCHORS, NUM_CLASS, XYSCALE = utils.load_config(self.config)

        input_layer = tf.keras.layers.Input([FLAGS.input_size, FLAGS.input_size, 3])
        feature_maps = YOLO(input_layer, NUM_CLASS, FLAGS.model, FLAGS.tiny)
        bbox_tensors = []
        prob_tensors = []
        if FLAGS.tiny:
            for i, fm in enumerate(feature_maps):
                if i == 0:
                    output_tensors = decode(fm, FLAGS.input_size // 16, NUM_CLASS, STRIDES, ANCHORS, i, XYSCALE, FLAGS.framework)
                else:
                    output_tensors = decode(fm, FLAGS.input_size // 32, NUM_CLASS, STRIDES, ANCHORS, i, XYSCALE, FLAGS.framework)
                bbox_tensors.append(output_tensors[0])
                prob_tensors.append(output_tensors[1])
        else:
            for i, fm in enumerate(feature_maps):
                if i == 0:
                    output_tensors = decode(fm, FLAGS.input_size // 8, NUM_CLASS, STRIDES, ANCHORS, i, XYSCALE, FLAGS.framework)
                elif i == 1:
                    output_tensors = decode(fm, FLAGS.input_size // 16, NUM_CLASS, STRIDES, ANCHORS, i, XYSCALE, FLAGS.framework)
                else:
                    output_tensors = decode(fm, FLAGS.input_size // 32, NUM_CLASS, STRIDES, ANCHORS, i, XYSCALE, FLAGS.framework)
                bbox_tensors.append(output_tensors[0])
                prob_tensors.append(output_tensors[1])
        pred_bbox = tf.concat(bbox_tensors, axis=1)
        pred_prob = tf.concat(prob_tensors, axis=1)
        if FLAGS.framework == 'tflite':
            pred = (pred_bbox, pred_prob)
        else:
            boxes, pred_conf = filter_boxes(pred_bbox, pred_prob, score_threshold=FLAGS.score_thres, input_shape=tf.constant([FLAGS.input_size, FLAGS.input_size]))
            pred = tf.concat([boxes, pred_conf], axis=-1)
        model = tf.keras.Model(input_layer, pred)
        utils.load_weights(model, FLAGS.weights, FLAGS.model, FLAGS.tiny)
        model.summary()
        model.save(FLAGS.output)

    def download_models(self):
        models_converter = Model_Converter(self.config)
        for model_type in self.enabled_models:
            logger.info(f"Attempting download of {model_type}")
            try:
                filename = self.config.data[f'{model_type}.modelName']
            except KeyError:
                raise ValueError(f"No configuration value found for `{model_type}.modelName`.")

            blob_name = filename
            file_destination = self._get_file_destination(model_type, filename)
            folder_destination = os.path.dirname(os.path.abspath(file_destination))
            os.makedirs(folder_destination, exist_ok=True)
            if not os.path.isfile(file_destination):
                self.storage_client.download(self.config.get('storage.bucket', 'md-blog-model-zoo'), blob_name, file_destination)
                models_converter.save_tf()

