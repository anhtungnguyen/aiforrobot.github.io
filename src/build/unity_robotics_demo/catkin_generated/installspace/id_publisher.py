import rospy
# from unity_robotics_demo_msgs.msg import IntCus
from std_msgs.msg import Int32
from unity_robotics_demo_msgs.msg import PosRot
from geometry_msgs.msg import Pose

class MatLabToUnity:
    def __init__(self):
        # Initialize the ROS node
        rospy.init_node('matlab_listener', anonymous=True)

        # Variable to store the latest data
        self.matlab_data = None

        self.unity_data = PosRot()

        # Create a subscriber object
        self.subscriber = rospy.Subscriber("/marker_pose", Pose, self.matlab_callback)

        # Publisher to send data to Unity
        self.publisher = rospy.Publisher("/unity_pose", PosRot, queue_size=10)

    def matlab_callback(self, data):
        # Save the received data
        # self.matlab_data = data
        self.unity_data.pos_x = data.position.x
        self.unity_data.pos_y = data.position.y
        self.unity_data.pos_z = data.position.z
        self.unity_data.rot_x = data.orientation.x
        self.unity_data.rot_y = data.orientation.y
        self.unity_data.rot_z = data.orientation.z
        self.unity_data.rot_w = data.orientation.w
        # rospy.loginfo("Received data: %d", self.latest_data)

        self.publisher.publish(self.unity_data)

    def get_latest_data(self):
        # Return the latest data received
        return self.latest_data

def main():
    MatLabToUnity()

    # Keep the script alive, process callbacks, and wait for data
    rospy.spin()


if __name__ == '__main__':
    main()