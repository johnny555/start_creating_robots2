cmake_minimum_required(VERSION 3.8)
project(magni_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_auto REQUIRED)

ament_auto_find_build_dependencies()


ament_auto_package(
  INSTALL_TO_SHARE     
    meshes
    materials
    urdf
)


install(DIRECTORY
  DESTINATION
  share/${PROJECT_NAME}/models/${PROJECT_NAME}
)
# Create symlink to meshes folder, otherwise RVIz won't find the model
install(CODE "execute_process( \
    COMMAND ${CMAKE_COMMAND} -E create_symlink \
    ${CMAKE_INSTALL_PREFIX}/share/${PROJECT_NAME}/meshes \
    ${CMAKE_INSTALL_PREFIX}/share/${PROJECT_NAME}/models/${PROJECT_NAME}/meshes  \
    )"
)
