cmake_minimum_required(VERSION 3.8)
project(amr_camera_input)

find_package(ament_cmake REQUIRED)

install(DIRECTORY launch config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
