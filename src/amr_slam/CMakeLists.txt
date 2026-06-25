cmake_minimum_required(VERSION 3.8)
project(amr_slam)

find_package(ament_cmake REQUIRED)

set(_required_launch_files
  launch/mapping.launch.py
  launch/online_async_slam.launch.py
  launch/slam_rviz.launch.py
  launch/save_map.launch.py
)
foreach(_launch_file IN LISTS _required_launch_files)
  if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/${_launch_file}")
    message(FATAL_ERROR "amr_slam: missing required launch file '${_launch_file}'")
  endif()
endforeach()

if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/config/slam_toolbox_default.rviz")
  message(FATAL_ERROR "amr_slam: missing config/slam_toolbox_default.rviz")
endif()

install(
  DIRECTORY config/
  DESTINATION share/${PROJECT_NAME}/config
)

install(
  DIRECTORY launch/
  DESTINATION share/${PROJECT_NAME}/launch
  FILES_MATCHING PATTERN "*.launch.py"
)

ament_package()
