from setuptools import find_packages, setup

package_name = 'temperature_monitor'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='manuel',
    maintainer_email='manuel@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'publisher_node = temperature_monitor.publisher_node:main',
            'monitor_node = temperature_monitor.monitor_node:main',
            'enhanced_publisher_node = temperature_monitor.enhanced_sensor_node:main',
            'enhanced_monitor_node = temperature_monitor.enhanced_monitor_node:main',
            'logger_node = temperature_monitor.logger_node:main',
        ],
    },
)
