import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped
from threading import Thread

# Lets create a class that takes x,y coords and sends the robot there.
class KrytnCommander(Node):
    def __init__(self):
        super().__init__('krytn_commander', parameter_overrides=[Parameter(name='use_sim_time',value=True)])
        self.action = ActionClient(self, NavigateToPose, '/navigate_to_pose')
        self.clock = self.get_clock()

    def feedback_callback(self, msg):
        print(f"distance remaining: {msg.feedback.distance_remaining}")

    def send_krytn(self, x, y, rz=0):
        self.action.wait_for_server()
        now = self.clock.now().to_msg()

        point = PoseStamped()
        point.pose.position.x = x
        point.pose.position.y = y
        point.header.frame_id ='map'
        point.header.stamp = now

        goal = NavigateToPose.Goal()
        goal.pose = point
        print('sending goal')
        result = self.action.send_goal(goal, feedback_callback=self.feedback_callback)

        print("goal completed")
        print(result)
        

def main():

    rclpy.init()
    executor = rclpy.executors.MultiThreadedExecutor(2)

    commander = KrytnCommander()
    executor.add_node(commander)

    executor_thread = Thread(target=executor.spin, daemon=True, args=())
    executor_thread.start()
    commander.create_rate(1.0).sleep()

    commander.send_krytn(-3.015, -3.637)
    commander.send_krytn(-1.0, -1.0)
    
    print("finished, shutting down")
    executor_thread.join()

if __name__ == '__main__':
    main()
