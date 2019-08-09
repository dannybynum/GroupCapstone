from styx_msgs.msg import TrafficLight
import numpy as np
import tensorflow as tf
import datetime

class TLClassifier(object):
    def __init__(self):
        #TODO load classifier
        MODELFILE = r'light_classification/model/frozen_inference_graph.pb'
        self.graph = tf.Graph()
        self.threshold = .5
        with self.graph.as_default():
            graph_def = tf.GraphDef()
            with tf.gfile.GFile(MODELFILE, 'rb') as fid:
                graph_def.ParseFromString(fid.read())
                tf.import_graph_def(graph_def, name='')

            self.image_tensor = self.graph.get_tensor_by_name('image_tensor:0')
            self.boxes = self.graph.get_tensor_by_name('detection_boxes:0')
            self.scores = self.graph.get_tensor_by_name('detection_scores:0')
            self.classes = self.graph.get_tensor_by_name('detection_classes:0')
            self.num_detections = self.graph.get_tensor_by_name(
                'num_detections:0')

        self.sess = tf.Session(graph=self.graph)
        #print('end classifier init')

    def get_classification(self, image):
        """Determines the color of the traffic light in the image

        Args:
            image (cv::Mat): image containing the traffic light

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        #TODO implement light color prediction
        #print('enter get_classification')
        with self.graph.as_default():
            img_expand = np.expand_dims(image, axis=0)
            (boxes, scores, classes, num_detections) = self.sess.run(
                [self.boxes, self.scores, self.classes, self.num_detections],
                feed_dict={self.image_tensor: img_expand})

        boxes = np.squeeze(boxes)
        scores = np.squeeze(scores)
        classes = np.squeeze(classes).astype(np.int32)
        #print('found classes: ', classes[0])

        if scores[0] > self.threshold:
            if classes[0] == 1:
                print('1:green')
                return TrafficLight.GREEN
            elif classes[0] == 2:
                print('2:red')
                return TrafficLight.RED
            elif classes[0] == 3:
                print('3:yellow')
                return TrafficLight.YELLOW
                
        return TrafficLight.UNKNOWN
