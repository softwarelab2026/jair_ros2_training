from launch import LaunchDescription
import launch_ros.actions

def generate_launch_description():
    return LaunchDescription([
        launch_ros.actions.Node(
            namespace='turtlesim1', package='turtlesim',
            executable='turtlesim_node', output='screen'),
        launch_ros.actions.Node(
            namespace='rqt_console', package='rqt_console',
            executable='rqt_console', output='screen'),
        launch_ros.actions.Node(
            namespace='rqt_gui', package='rqt_gui',
            executable='rqt_gui', output='screen'),
    ])

