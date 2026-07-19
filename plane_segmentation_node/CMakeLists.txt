cmake_minimum_required(VERSION 3.8)
project(plane_segmentation_node)

add_compile_options(-std=c++20)

find_package(ament_cmake_auto REQUIRED)
ament_auto_find_build_dependencies()

## Generate interfaces
ament_auto_generate_code()

## Prepare programs

ament_python_install_package(${PROJECT_NAME})

# ament_auto_add_library(${PROJECT_NAME}_server
#   SHARED
#   src/server.cpp
# )

# rclcpp_components_register_node(
#     ${PROJECT_NAME}_server
#     PLUGIN "${PROJECT_NAME}::Server"
#     EXECUTABLE server
# )

install(PROGRAMS
  scripts/server
  DESTINATION lib/${PROJECT_NAME}
)

## Install resources

# Install launch files
install(DIRECTORY
  launch
  resources
  DESTINATION share/${PROJECT_NAME}/
)

ament_auto_package(
  USE_SCOPED_HEADER_INSTALL_DIR
)
