#include <iostream>
#include "MindRove.h"  // Include MindRove header for connection and setup

int main() {
    // Initialize the MindRove SDK
    if (MindRove::initialize()) {
        std::cout << "MindRove initialized successfully." << std::endl;
        
        // Connect to device
        MindRove::Device device;
        if (device.connect("DeviceID")) {
            std::cout << "Connected to device successfully!" << std::endl;

            // Start reading data (assuming MindRove provides a function for this)
            device.startReading();

            // Process data here...

            device.stopReading();
            std::cout << "Data collection stopped." << std::endl;

            device.disconnect();
            std::cout << "Disconnected from device." << std::endl;
        } else {
            std::cerr << "Failed to connect to device." << std::endl;
        }

        MindRove::shutdown();
    } else {
        std::cerr << "MindRove initialization failed." << std::endl;
    }

    return 0;
}
