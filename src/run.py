from launch import LaunchDescription
import launch_ros.actions

def generate_launch_description():
    return LaunchDescription([
        launch_ros.actions.Node(
            package='turtlesim',
            executable='turtlesim_node', output='screen'),
        launch_ros.actions.Node(
            package='rqt_console',
            executable='rqt_console', output='screen'),
        launch_ros.actions.Node(
            package='rqt_gui',
            executable='rqt_gui', output='screen'),
        launch_ros.actions.Node(
            package='jair_turtlesim',
            executable='jair_turtlesim', output='screen'),
        # launch_ros.actions.Node(
        #     namespace='image_feeder', package='image_feeder',
        #     executable='image_feeder', output='screen'),
    ])

