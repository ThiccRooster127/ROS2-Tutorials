import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json
import csv
from pathlib import Path
import datetime

class LoggerNode(Node):

    def __init__(self):
        super().__init__('logger_node')

        self.reading_frequency = 1
        self.delete_previous_readings = 0
        self.current_message = -1
        self.fieldnames = ['temperature', 'location', 'timestamp']


        self.subscription = self.create_subscription(
            String,
            'temperature_and_location',
            self.reading_callback,
            10
        )

        self.declare_parameter('reading_frequency', self.reading_frequency)
        self.reading_frequency = self.get_parameter(
            'reading_frequency',
            ).get_parameter_value().integer_value

        self.declare_parameter('delete_previous_readings', self.delete_previous_readings)
        self.delete_previous_readings = self.get_parameter(
            'delete_previous_readings',
        ).get_parameter_value().integer_value

        self.get_logger().info('Logger node initialized')
        self.get_logger().info(f'Reading frequency set to {self.reading_frequency}')
        if(self.delete_previous_readings):
            self.get_logger().info('Deleting previous readings')
            with open('Logs.csv', 'w', newline= '') as csvfile:
                headerWriter = csv.DictWriter(csvfile, fieldnames = self.fieldnames)
                headerWriter.writeheader()



    def reading_callback(self, msg):

        self.current_message += 1

        if(self.current_message % (self.reading_frequency*2) <= 1):

            json_payload = json.loads(msg.data)

            temperature = json_payload['temperature']
            location = json_payload['location']
            current_time = datetime.datetime.now()

            with open('Logs.csv', 'a', newline = '') as csvfile:
                temperatureWrite = csv.DictWriter(csvfile, fieldnames = self.fieldnames)
                temperatureWrite.writerow({'temperature': temperature, 'location': location, 'timestamp': current_time})

def main(args=None):
    rclpy.init(args=args)
    node = LoggerNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()