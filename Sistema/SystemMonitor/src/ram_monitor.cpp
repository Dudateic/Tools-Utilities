#include "../include/ram_monitor.hpp"
#include <fstream>
#include <sstream>

static float totalMemory = 0.0f;

float RamMonitor::getTotalMemory() {
    if (totalMemory > 0) {
        return totalMemory;
    }
    
    std::ifstream file("/proc/meminfo");
    if (!file.is_open()) {
        return 0.0f;
    }
    
    std::string line;
    while (std::getline(file, line)) {
        if (line.find("MemTotal:") != std::string::npos) {
            std::stringstream ss(line);
            std::string label;
            float value;
            ss >> label >> value;
            totalMemory = value / 1024.0f; // Converter de KB para MB
            break;
        }
    }
    
    file.close();
    return totalMemory;
}

float RamMonitor::getAvailableMemory() {
    std::ifstream file("/proc/meminfo");
    if (!file.is_open()) {
        return 0.0f;
    }
    
    float available = 0.0f;
    std::string line;
    
    while (std::getline(file, line)) {
        if (line.find("MemAvailable:") != std::string::npos) {
            std::stringstream ss(line);
            std::string label;
            float value;
            ss >> label >> value;
            available = value / 1024.0f; // Converter de KB para MB
            break;
        }
    }
    
    file.close();
    return available;
}

float RamMonitor::getUsage() {
    float total = getTotalMemory();
    float available = getAvailableMemory();
    
    if (total <= 0) {
        return 0.0f;
    }
    
    float used = total - available;
    return (used / total) * 100.0f;
}
