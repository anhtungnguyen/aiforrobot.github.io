#!/usr/bin/env python3
import sys
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError  
import cv2
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap, QScreen
from PyQt5.QtGui import QImage
import numpy as np
# from PIL import ImageGrab

app = QApplication(sys.argv)
def capture_screen():
    # app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    img = screen.grabWindow(0).toImage()
    if img.isNull():
        print("Failed to capture the screen")
    else:
        return img
    ###############################################
    # Set up video capture from the stream URL
    # cap = cv2.VideoCapture('https://www.youtube.com/watch?v=kYM_LCUaT6E')
    # ret, frame = cap.read()
    # if not ret:
    #     print("Failed to capture from stream")
    #     return None
    # return frame

def qimage_to_cv2(qt_image):
    """ Convert a QImage object to an OpenCV image format """
    # qt_image = qt_image.convertToFormat(QImage.Format_RGB32)
    # width = qt_image.width()
    # height = qt_image.height()
    # ptr = qt_image.bits()
    # ptr.setsize(qt_image.byteCount())
    # arr = np.array(ptr).reshape(height, width, 4)  # 4 for RGBA
    # # Convert RGBA to BGR for OpenCV
    # return arr[:, :, :3][:, :, ::-1]

    qt_image = qt_image.convertToFormat(QImage.Format_RGB888)
    width = qt_image.width()
    height = qt_image.height()
    ptr = qt_image.bits()
    ptr.setsize(height * width * 3)
    arr = np.array(ptr).reshape(height, width, 3)  # 3 for RGB
    return arr
    # return arr[:, :, ::-1]
    ###############################################

def main():
    rospy.init_node('screen_capture_publisher', anonymous=True)
    image_pub = rospy.Publisher("/screen/image_raw", Image, queue_size=10)
    bridge = CvBridge()

    while not rospy.is_shutdown():
        qt_image = capture_screen()
        cv_image = qimage_to_cv2(qt_image)
        try:
            ros_image = bridge.cv2_to_imgmsg(cv_image, "bgr8")
            image_pub.publish(ros_image)
            # Display the image using OpenCV
            cv2.imshow('Screen Capture', cv_image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except cv_bridge.CvBridgeError as e:
            rospy.logerr("CvBridge Error: {0}".format(e))
        rospy.sleep(0.1)
        ###############################################
# def main():
#     rospy.init_node('screen_capture_publisher', anonymous=True)
#     image_pub = rospy.Publisher("/screen/image_raw", Image, queue_size=10)
#     bridge = CvBridge()
#     # Initialize video capture once
#     stream_url = 'https://www.youtube.com/watch?v=kYM_LCUaT6E'
#     cap = cv2.VideoCapture(stream_url)

#     while not rospy.is_shutdown():
#         ret, frame = cap.read()
#         if ret:
#             try:
#                 ros_image = bridge.cv2_to_imgmsg(frame, "bgr8")
#                 image_pub.publish(ros_image)
#                 # Display the image using OpenCV
#                 cv2.imshow('Screen Capture', frame)
#                 if cv2.waitKey(1) & 0xFF == ord('q'):
#                     break
#             except CvBridgeError as e:
#                 rospy.logerr("CvBridge Error: {0}".format(e))
#         else:
#             print("Failed to capture frame from stream")
#         rospy.sleep(0.1)

#     cap.release()
#     cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
