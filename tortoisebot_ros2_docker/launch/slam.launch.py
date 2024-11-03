import os

from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch_ros.actions import Node


def generate_launch_description():
    navigation_dir = os.path.join(
        get_package_share_directory('tortoisebot_navigation'), 'launch')
    cartographer_launch_dir = os.path.join(
        get_package_share_directory('tortoisebot_slam'), 'launch')
    prefix_address = get_package_share_directory('tortoisebot_slam')
    params_file = os.path.join(prefix_address, 'config', 'nav2_params.yaml')
    map_directory = os.path.join(get_package_share_directory(
        'tortoisebot_bringup'), 'maps', 'room2.yaml')

    use_sim_time = LaunchConfiguration('use_sim_time')
    exploration = LaunchConfiguration('exploration')
    map_file = LaunchConfiguration('map')

    use_sim_time_arg = DeclareLaunchArgument(name='use_sim_time', default_value='False',
                                             description='Flag to enable use_sim_time')
    exploration_arg = DeclareLaunchArgument(name='exploration', default_value='True',
                                            description='Flag to enable use_sim_time')
    map_arg = DeclareLaunchArgument(name='map', default_value=map_directory,
                                    description='Map to be used')

    navigation_launch_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(navigation_dir, 'navigation.launch.py')),
        launch_arguments={'params_file': params_file, }.items(),
        condition=IfCondition(PythonExpression(['not ', exploration])))
    cartographer_launch_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(cartographer_launch_dir, 'cartographer.launch.py')),
        launch_arguments={'params_file': params_file,
                          'slam': exploration,
                          'use_sim_time': use_sim_time}.items())
    nav2_map_server_launch_cmd = Node(
        package='nav2_map_server',
        condition=IfCondition(PythonExpression(['not ', exploration])),
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time},
                    {'yaml_filename': map_file}
                    ])
    nav2_lifecycle_manager_launch_cmd = Node(
        package='nav2_lifecycle_manager',
        condition=IfCondition(PythonExpression(['not ', exploration])),
        executable='lifecycle_manager',
        name='lifecycle_manager_mapper',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time},
                    {'autostart': True},
                    {'node_names': ['map_server']}])

    return LaunchDescription([
        #SetEnvironmentVariable('RCUTILS_LOGGING_BUFFERED_STREAM', '1'),
        use_sim_time_arg,
        exploration_arg,
        map_arg,
        nav2_map_server_launch_cmd,
        nav2_lifecycle_manager_launch_cmd,
        navigation_launch_cmd,
        cartographer_launch_cmd,
    ]
    )
