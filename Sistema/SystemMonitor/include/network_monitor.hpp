#ifndef NETWORK_MONITOR_HPP
#define NETWORK_MONITOR_HPP

#include <string>

class NetworkMonitor {
public:
    static bool ping(const std::string& host);
    static float getPacketLoss();
    static float getLatency();
};

#endif
