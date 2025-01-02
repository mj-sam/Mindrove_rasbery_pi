cmake_minimum_required(VERSION 3.10)
project(EMGSyncBox)
set(CMAKE_CXX_STANDARD 11)
find_package(MindRove REQUIRED)  # Specify your SDK package
add_executable(YourExecutable main.cpp)
target_link_libraries(YourExecutable PRIVATE MindRove::MindRoveLib)
