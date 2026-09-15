import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from std_msgs.msg import String
import random
import json

class EnhancedSensorNode(Node):

    def __init__(self):
        super().__init__('enhanced_temperature_sensor')

        self.publisher = self.create_publisher(
            String,
            'temperature_and_location',
            10
        )

        self.timer_period = 1.0
        self.timer = self.create_timer(
            self.timer_period,
            self.timer_callback
        )


        self.get_logger().info('Temperature and location sensor node initialised')

    def timer_callback(self):

        temp_data_1 = random.uniform(15.0, 35.0)
        temp_data_2 = random.uniform(15.0, 35.0)
        location_1 = "room 1"
        location_2 = "room 2"

        data = {
            "temperature": temp_data_1,
            "location": location_1
        }

        data_String = String()

        data_String.data = json.dumps(data)
        self.publisher.publish(data_String)

        self.get_logger().info(f'Publishing temperature: {temp_data_1:.1f} from {location_1}')

        data = {
            "temperature": temp_data_2,
            "location": location_2
        }

        data_String.data = json.dumps(data)
        self.publisher.publish(data_String)

        self.get_logger().info(f'Publishing temperature: {temp_data_2:.1f} from {location_2}')

def main (args=None):
    rclpy.init(args=args)
    node = EnhancedSensorNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()