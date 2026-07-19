cmake_minimum_required(VERSION 3.8)
project(plane_segmentation_interfaces)

## Compile as C++11, supported in ROS Kinetic and newer
add_compile_options(-std=c++20)

find_package(ament_cmake_auto REQUIRED)
ament_auto_find_build_dependencies()


# file(GLOB ${PROJECT_NAME}_msg_files RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} CONFIGURE_DEPENDS msg/*)
# # file(GLOB ${PROJECT_NAME}_srv_files RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} CONFIGURE_DEPENDS srv/*)
# rosidl_generate_interfaces(
#    ${PROJECT_NAME}
#    ${${PROJECT_NAME}_msg_files}
#   #  ${${PROJECT_NAME}_srv_files}
#    DEPENDENCIES ${${PROJECT_NAME}_FOUND_BUILD_DEPENDS}
# )

## Generate interfaces
rosidl_auto_generate_interfaces()

# ament_export_dependencies(rosidl_default_runtime)
ament_auto_package(
  USE_SCOPED_HEADER_INSTALL_DIR
)
