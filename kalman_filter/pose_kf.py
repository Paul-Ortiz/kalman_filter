import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from std_msgs.msg import Header
from yolo_msgs.msg import PoseArray, Pose
from kalman_filter.kalmanfilter import KalmanFilter
import numpy as np


class PoseSubscriber(Node):

    def __init__(self):
        super().__init__('PoseSubscriber')
        self.subscription = self.create_subscription(PoseArray, 'pose', self.listener_callback, 10)
        self.subscription  # prevent unused variable warning
        self.publisher_ = self.create_publisher(PoseArray, 'pose_pred', 10)
        self.kf = KalmanFilter()
        self.object_id = 5

    def listener_callback(self, pos_array):
        #print(pos_array)
        for pos in pos_array.poses:
            if pos.object_id == self.object_id:
                print(pos.class_name)
                print(pos.object_id)
                print(pos.position.x)
                print(pos.position.y)
                predicted = self.kf.predict(pos.position.x, pos.position.y)
                future_state = self.kf.getParam()[0]
                transitionMatrix = self.kf.getParam()[1]
                for i in range(2):   # n+1 predictions
                    future_state = np.dot(transitionMatrix , future_state);
                predicted_n = int(future_state[0]), int(future_state[1])
                print(predicted)
                print(predicted_n)

                # armar el nuevo PoseArray

def main(args=None):
    rclpy.init(args=args)

    pose_subscriber = PoseSubscriber()

    rclpy.spin(pose_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    pose_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
