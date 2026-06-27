#include "../include/network_monitor.hpp"
#include <cstdlib>
#include <fstream>
#include <sstream>

static float lastPacketLoss = 0.0f;
static float lastLatency = 0.0f;

bool NetworkMonitor::ping(const std::string& host) {
    std::string command = "ping -c 1 -W 2 " + host +
                          " > /tmp/ping_result.txt 2>&1";

    int result = system(command.c_str());

    if (result == 0) {
        std::ifstream file("/tmp/ping_result.txt");

        if (file.is_open()) {
            std::string line;

            while (std::getline(file, line)) {
                size_t pos = line.find("time=");

                if (pos != std::string::npos) {
                    std::stringstream ss(line.substr(pos + 5));
                    ss >> lastLatency;
                }
            }

            file.close();
        }

        lastPacketLoss = 0.0f;
        return true;
    }

    lastLatency = -1.0f;
    lastPacketLoss = 100.0f;

    return false;
}

float NetworkMonitor::getPacketLoss() {
    return lastPacketLoss;
}

float NetworkMonitor::getLatency() {
    return lastLatency;
}