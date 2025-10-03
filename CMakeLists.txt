cmake_minimum_required(VERSION 3.20)
project(rpmtt_gui_packaging LANGUAGES NONE)

# Find Python3 interpreter
find_package(Python3 COMPONENTS Interpreter REQUIRED)

# Source file (located in the same directory as this CMakeLists.txt)
set(APP_ENTRY main.py)

# Build directory and output directory (PyInstaller convention)
set(PYI_BUILD_DIR ${CMAKE_BINARY_DIR}/pyinstaller)
set(PYI_DIST_DIR  ${PYI_BUILD_DIR}/dist)

# Output name for different platforms
if(APPLE)
  set(APP_NAME rpmtt_gui.app)
  set(APP_OUTPUT ${PYI_DIST_DIR}/${APP_NAME})
else()
  set(APP_NAME rpmtt_gui)
  if(WIN32)
    set(APP_OUTPUT ${PYI_DIST_DIR}/${APP_NAME}.exe)
  else()
    set(APP_OUTPUT ${PYI_DIST_DIR}/${APP_NAME})
  endif()
endif()

# Main packaging command: Install/upgrade PyInstaller, copy source code, execute packaging
add_custom_command(
  OUTPUT ${APP_OUTPUT}
  COMMAND ${Python3_EXECUTABLE} -m pip install --upgrade pip
  COMMAND ${Python3_EXECUTABLE} -m pip install --upgrade pyinstaller
  COMMAND ${CMAKE_COMMAND} -E make_directory ${PYI_BUILD_DIR}
  COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_SOURCE_DIR}/${APP_ENTRY} ${PYI_BUILD_DIR}/
  # --windowed: Hide console window (friendly for Tk GUI applications); --onefile: Single file distribution (generates .app on macOS)
  COMMAND ${Python3_EXECUTABLE} -m PyInstaller
          --noconfirm --clean
          --name rpmtt_gui
          --onefile
          --windowed
          ${PYI_BUILD_DIR}/main.py
  WORKING_DIRECTORY ${PYI_BUILD_DIR}
  COMMENT "Building standalone GUI executable with PyInstaller"
  VERBATIM
)

# Default build target: Generate the executable output
add_custom_target(build_rpmtt ALL DEPENDS ${APP_OUTPUT})

# Install target: Install the output to bin (.app bundle for macOS)
if(APPLE)
  install(DIRECTORY ${APP_OUTPUT} DESTINATION bin)
else()
  install(PROGRAMS ${APP_OUTPUT} DESTINATION bin)
endif()