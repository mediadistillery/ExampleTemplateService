import os
# comment out below line to enable tensorflow outputs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

import example_template_core.yolo.utils as utils
from example_template_core.yolo.yolov4 import filter_boxes
from example_template_core.yolo.functions import *
from tensorflow.python.saved_model import tag_constants



class ObjectDetectionService:
    def __init__(self, config):

        self.input_size = config.get('yolo.input_size', 416)
        self.framework = config.get('yolo.framework', 'tf')
        self.iou = config.get('yolo.iou', 0.45)
        self.score_threshold = config.get('yolo.score_threshold', 0.50)
        self.tiny = config.get('yolo.tiny', False)
        self.final_weight_path = config.get('yolo.finalweights', '/etc/example_templete/models/yolo_checkpoint')
        self.model_name = config.get('yolo.model', 'yolov4')
        self.model = self._load_model()

    def _load_model(self):

        if self.framework == 'tflite':
            return tf.lite.Interpreter(model_path=self.final_weight_path)
        else:
            return tf.saved_model.load(self.final_weight_path, tags=[tag_constants.SERVING])

    def _format_detctions(self, detections, original_image,allowed_classes):

        boxes = detections[0]
        scores = detections[1]
        classes = detections[2]
        valid_detections = detections[3]
        # format bounding boxes from normalized ymin, xmin, ymax, xmax ---> xmin, ymin, xmax, ymax
        original_h, original_w, _ = original_image.shape
        bboxes = utils.format_boxes(boxes.numpy()[0], original_h, original_w)
        # hold all detection data in one variable
        pred_bbox = [bboxes, scores.numpy()[0], classes.numpy()[0], valid_detections.numpy()[0]]
        # read in all class names from config
        class_names = utils.read_class_names(cfg.YOLO.CLASSES)

        if allowed_classes == 'all' or allowed_classes is None:
            # by default allow all classes in .names file
            allowed_classes = list(class_names.values())
        else:
            allowed_classes = allowed_classes.split(',')

        if True:
            crops = get_objects(pred_bbox, allowed_classes)

        return crops

    def detect(self, images_data, original_image,allowed_classes = 'all'):

        if self.framework == 'tflite':
            interpreter = self.model
            interpreter.allocate_tensors()
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()
            interpreter.set_tensor(input_details[0]['index'], images_data)
            interpreter.invoke()
            pred = [interpreter.get_tensor(output_details[i]['index']) for i in range(len(output_details))]
            if self.model_name == 'yolov3' and self.tiny == True:
                boxes, pred_conf = filter_boxes(pred[1], pred[0], score_threshold=0.25, input_shape=tf.constant([self.input_size, self.input_size]))
            else:
                boxes, pred_conf = filter_boxes(pred[0], pred[1], score_threshold=0.25, input_shape=tf.constant([self.input_size, self.input_size]))
        else:
            saved_model_loaded = self.model
            infer = saved_model_loaded.signatures['serving_default']
            batch_data = tf.constant(images_data)
            pred_bbox = infer(batch_data)
            for key, value in pred_bbox.items():
                boxes = value[:, :, 0:4]
                pred_conf = value[:, :, 4:]

        # run non max suppression on detections
        boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
                        boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
                        scores=tf.reshape(pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
                        max_output_size_per_class=50,
                        max_total_size=50,
                        iou_threshold=self.iou,
                        score_threshold=self.score_threshold)

        raw_detections = [boxes, scores, classes, valid_detections]

        final_detections = self._format_detctions(raw_detections, original_image,allowed_classes)

        return final_detections

