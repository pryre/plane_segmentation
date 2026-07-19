#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

from typing import Any


def get_settable_arg(name:str, description:str, default_value:Any = None):
    cfg = LaunchConfiguration(name, default=default_value)
    arg = DeclareLaunchArgument(
        name,
        default_value=str(default_value),
        description=description
    )
    return (cfg, arg)


def generate_launch_description():
    camera_name = "camera/camera"

    return LaunchDescription([
        Node(
            name='plane_segmentation',
            namespace=camera_name,
            package='plane_segmentation_node',
            executable='server',
            parameters=[
                # {"frame_id": '/base_link'},
            ],
        ),
    ])



