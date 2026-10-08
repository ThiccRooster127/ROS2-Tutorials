import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json

class EnhancedMonitorNode(Node):

    def __init__(self):
        super().__init__('enhanced_temperature_monitor')

        self.temps_room1 = []
        self.temps_room2 = []
        self.average_temperature = 0
        self.high_temperature_alerts = 0
        self.critical_temperature_alerts = 0

        self.subscription = self.create_subscription(
            String, 
            'temperature_and_location',
            self.temperature_callback,
            10
        )

        self.temperature_threshold = 28.0
        self.critical_temperature_threshold = 32.0

        self.declare_parameter('temperature_threshold', self.temperature_threshold)
        self.declare_parameter('critical_temperature_threshold', self.critical_temperature_threshold)

        self.temperature_threshold = self.get_parameter(
            'temperature_threshold'
        ).get_parameter_value().double_value

        self.critical_temperature_threshold = self.get_parameter(
            'critical_temperature_threshold'
        ).get_parameter_value().double_value

        self.get_logger().info('Enhanced temperature monitor node initialised')
        self.get_logger().info(f'Temperature threshold set to {self.temperature_threshold}')
        self.get_logger().info(f'Critical temperature threshold set to {self.critical_temperature_threshold}')

    def temperature_callback(self, msg):
        json_payload = json.loads(msg.data)

        location = json_payload["location"]
        temperature = json_payload["temperature"]

        self.get_logger().info(f'Temperature in {location} is {temperature:.1f}')

        if(location == "room 1"):

            if(len(self.temps_room1) == 5):
                self.temps_room1.pop()

            self.temps_room1.insert(0, temperature)
            self.average_temperature = sum(self.temps_room1) / 5
            self.get_logger().info(f'Average Temp in room 1 is {self.average_temperature}')
        else:

            if(len(self.temps_room2) == 5):
                self.temps_room2.pop()

            self.temps_room2.insert(0, temperature)
            self.average_temperature = sum(self.temps_room2) / 5
            self.get_logger().info(f'Average Temp in room 2 is {self.average_temperature}')

        if(self.average_temperature > self.critical_temperature_threshold):
            self.critical_temperature_alerts += 1
            self.get_logger().error(f'CRITICAL TEMPERATURE ALERT: {self.average_temperature:0.1f}ºC at {location} exceeds {self.critical_temperature_threshold}, {self.critical_temperature_alerts} counts of critical temperature occured')

        elif(self.average_temperature > self.temperature_threshold):
            self.high_temperature_alerts += 1
            self.get_logger().warn(f'HIGH TEMPERATURE ALERT: {self.average_temperature:0.1f}ºC at {location} exceeds {self.temperature_threshold}, {self.high_temperature_alerts} counts of high temperature occured')
        

def main(args=None):
    rclpy.init(args=args)
    node = EnhancedMonitorNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

