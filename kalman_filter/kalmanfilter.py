import cv2
import numpy as np

class KalmanFilter:
    kf = cv2.KalmanFilter(4, 2)
    kf.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
    kf.transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)
    kf.processNoiseCov = np.eye(4, dtype=np.float32) * 5 
    kf.measurementNoiseCov = np.eye(2, dtype=np.float32) * 1
    kf.statePre = np.array([50, 100, 0, 0], np.float32)
    kf.statePost = np.array([50, 100, 0, 0], np.float32)


    def predict(self, coordX, coordY):
        ''' This function estimates the position of the object'''
        measured = np.array([[np.float32(coordX)], [np.float32(coordY)]])
        # Occlusion handling
        if measured is not None:
            # Update
            self.kf.correct(np.array(measured, np.float32))
            # Reset covariance to a smaller value as a new detection is available
            self.kf.processNoiseCov = np.eye(4, dtype=np.float32) * 5 
        else:
            # Increase covariance during occlusion
            self.kf.processNoiseCov = np.eye(4, dtype=np.float32) * 100
        
        
        predicted = self.kf.predict()
        x, y = int(predicted[0]), int(predicted[1])
        return x, y

    def getParam(self):
        return  self.kf.statePost, self.kf.transitionMatrix
