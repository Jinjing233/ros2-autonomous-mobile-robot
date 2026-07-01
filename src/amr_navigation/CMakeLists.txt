cmake_minimum_required(VERSION 3.8)
project(amr_navigation)

find_package(ament_cmake REQUIRED)

if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/launch/map_server.launch.py")
  message(FATAL_ERROR "amr_navigation: missing required launch/map_server.launch.py")
endif()

if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/launch/localization.launch.py")
  message(FATAL_ERROR "amr_navigation: missing required launch/localization.launch.py")
endif()

if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/launch/localization_rviz.launch.py")
  message(FATAL_ERROR "amr_navigation: missing required launch/localization_rviz.launch.py")
endif()

if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/launch/navigation.launch.py")
  message(FATAL_ERROR "amr_navigation: missing required launch/navigation.launch.py")
endif()

if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/launch/amr_nav2_navigation.launch.py")
  message(FATAL_ERROR "amr_navigation: missing required launch/amr_nav2_navigation.launch.py")
endif()

if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/launch/navigation_rviz.launch.py")
  message(FATAL_ERROR "amr_navigation: missing required launch/navigation_rviz.launch.py")
endif()

if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/config/navigation_default.rviz")
  message(FATAL_ERROR "amr_navigation: missing required config/navigation_default.rviz")
endif()

if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/scripts/nav_goal_relay.py")
  message(FATAL_ERROR "amr_navigation: missing required scripts/nav_goal_relay.py")
endif()

if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/config/amr_nav2_params.yaml")
  message(FATAL_ERROR "amr_navigation: missing required config/amr_nav2_params.yaml")
endif()

if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/config/localization_default.rviz")
  message(FATAL_ERROR "amr_navigation: missing required config/localization_default.rviz")
endif()

install(
  PROGRAMS scripts/nav_goal_relay.py
  DESTINATION lib/${PROJECT_NAME}
)

install(
  DIRECTORY maps/
  DESTINATION share/${PROJECT_NAME}/maps
)

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
