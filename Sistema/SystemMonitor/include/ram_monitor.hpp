#ifndef RAM_MONITOR_HPP
#define RAM_MONITOR_HPP

class RamMonitor {
public:
    static float getUsage();
    static float getTotalMemory();
    static float getAvailableMemory();
};

#endif
