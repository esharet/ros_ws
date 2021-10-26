from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import Command, LaunchConfiguration
import os.path

pkg_name="m2wr_description"
pkg_share = get_package_share_directory(pkg_name)
default_urdf_model_path = os.path.join(pkg_share, "urdf", "m2wr.xacro")
rviz_config_path = os.path.join(pkg_share, "config", "config.rviz")
urdf_model = LaunchConfiguration('urdf_model')

# Declare the launch arguments  
declare_urdf_model_path_cmd = DeclareLaunchArgument(
    name='urdf_model', 
    default_value=default_urdf_model_path, 
    description='Absolute path to robot urdf file')

start_joint_state_publisher_cmd = Node(
    package='joint_state_publisher',
    executable='joint_state_publisher',
    name='joint_state_publisher')

start_rviz_cmd = Node(
            package='rviz2',
            namespace='',
            executable='rviz2',
            name='rviz2',
            arguments=["-d", rviz_config_path]
        )
start_robot_state_publisher_cmd = Node(
    package='robot_state_publisher',
    executable='robot_state_publisher',
    parameters=[{'use_sim_time': True, 
    'robot_description': Command(['xacro ', urdf_model])}],

    arguments=[default_urdf_model_path])
def generate_launch_description():
    ld = LaunchDescription()
    ld.add_action(declare_urdf_model_path_cmd)
    ld.add_action(start_robot_state_publisher_cmd)
    ld.add_action(start_joint_state_publisher_cmd)
    ld.add_action(start_rviz_cmd)
    return ld
# arguments=['-d' + os.path.join(get_package_share_directory('m2wr_description'), 'config', 'config_file.rviz')]