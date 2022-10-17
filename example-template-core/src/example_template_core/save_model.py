import tensorflow as tf
from absl import app, flags, logging
from absl.flags import FLAGS
from example_template_core.yolo.yolov4 import YOLO, decode, filter_boxes
import example_template_core.yolo.utils as utils
from example_template_core.yolo.config import cfg
from example_template_foundation.config.configuration_manager import ConfigurationManager

flags.DEFINE_string('weights', '/home/anustup/Desktop/Mediadistillery/YOLO4/yolov4-custom-functions/weights/yolov4.weights', 'path to weights file')
flags.DEFINE_string('output', '/home/anustup/Desktop/Mediadistillery/checkpoints/yolov4-416', 'path to output')
flags.DEFINE_boolean('tiny', False, 'is yolo-tiny or not')
flags.DEFINE_integer('input_size', 416, 'define input size of export model')
flags.DEFINE_float('score_thres', 0.2, 'define score threshold')
flags.DEFINE_string('framework', 'tf', 'define what framework do you want to convert (tf, trt, tflite)')
flags.DEFINE_string('model', 'yolov4', 'yolov3 or yolov4')


class Model_Converter:
  def __init__(self, config: ConfigurationManager):
    self.config = config
    self.weights = self.config.get('yolo.weightPath', '/home/anustup/Desktop/Mediadistillery/YOLO4/yolov4-custom-functions/weights/yolov4.weights')
    self.output = self.config.get('yolo.output', '/home/anustup/Desktop/Mediadistillery/checkpoints/yolov4-416')
    self.tiny = self.config.get('yolo.tiny', False)
    self.input_size = self.config.get('yolo.input_size', 416)
    self.score_thres = self.config.get('yolo.score_thres', 0.2)
    self.framework = self.config.get('yolo.framework', 'tf')
    self.model = self.config.get('yolo.model', 'yolov4')

  def save_tf(self):
    STRIDES, ANCHORS, NUM_CLASS, XYSCALE = utils.load_config(self)

    input_layer = tf.keras.layers.Input([self.input_size, self.input_size, 3])
    feature_maps = YOLO(input_layer, NUM_CLASS, self.model, self.tiny)
    bbox_tensors = []
    prob_tensors = []
    if self.tiny:
      for i, fm in enumerate(feature_maps):
        if i == 0:
          output_tensors = decode(fm, self.input_size // 16, NUM_CLASS, STRIDES, ANCHORS, i, XYSCALE, self.framework)
        else:
          output_tensors = decode(fm, self.input_size // 32, NUM_CLASS, STRIDES, ANCHORS, i, XYSCALE, self.framework)
        bbox_tensors.append(output_tensors[0])
        prob_tensors.append(output_tensors[1])
    else:
      for i, fm in enumerate(feature_maps):
        if i == 0:
          output_tensors = decode(fm, self.input_size // 8, NUM_CLASS, STRIDES, ANCHORS, i, XYSCALE, self.framework)
        elif i == 1:
          output_tensors = decode(fm, self.input_size // 16, NUM_CLASS, STRIDES, ANCHORS, i, XYSCALE, self.framework)
        else:
          output_tensors = decode(fm, self.input_size // 32, NUM_CLASS, STRIDES, ANCHORS, i, XYSCALE, self.framework)
        bbox_tensors.append(output_tensors[0])
        prob_tensors.append(output_tensors[1])
    pred_bbox = tf.concat(bbox_tensors, axis=1)
    pred_prob = tf.concat(prob_tensors, axis=1)
    if self.framework == 'tflite':
      pred = (pred_bbox, pred_prob)
    else:
      boxes, pred_conf = filter_boxes(pred_bbox, pred_prob, score_threshold=self.score_thres, input_shape=tf.constant([self.input_size, self.input_size]))
      pred = tf.concat([boxes, pred_conf], axis=-1)
    model = tf.keras.Model(input_layer, pred)
    utils.load_weights(model, self.weights, self.model, self.tiny)
    model.summary()
    model.save(self.output)















def main(_argv):
  save_tf()

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
