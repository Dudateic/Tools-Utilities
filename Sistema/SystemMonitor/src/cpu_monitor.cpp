#include "../include/cpu_monitor.hpp"
#include <fstream>
#include <sstream>
#include <unistd.h>

static unsigned long lastTotalTicks = 0;
static unsigned long lastIdleTicks = 0;

float CpuMonitor::getUsage() {
    std::ifstream file("/proc/stat");
    if (!file.is_open()) {
        return 0.0f;
    }
    
    std::string line;
    std::getline(file, line);
    file.close();
    
    unsigned long user, nice, system, idle, iowait, irq, softirq;
    std::stringstream ss(line);
    std::string cpu;
    
    ss >> cpu >> user >> nice >> system >> idle >> iowait >> irq >> softirq;
    
    unsigned long totalTicks = user + nice + system + idle + iowait + irq + softirq;
    unsigned long idleTicks = idle + iowait;
    
    if (lastTotalTicks == 0) {
        lastTotalTicks = totalTicks;
        lastIdleTicks = idleTicks;
        return 0.0f;
    }
    
    unsigned long deltaTotalTicks = totalTicks - lastTotalTicks;
    unsigned long deltaIdleTicks = idleTicks - lastIdleTicks;
    
    float cpuUsage = 0.0f;
    if (deltaTotalTicks != 0) {
        cpuUsage = ((deltaTotalTicks - deltaIdleTicks) * 100.0f) / deltaTotalTicks;
    }
    
    lastTotalTicks = totalTicks;
    lastIdleTicks = idleTicks;
    
    return cpuUsage;
}
