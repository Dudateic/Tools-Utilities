#ifndef CONFIG_HPP
#define CONFIG_HPP

#include <string>

class Config {
private:
    float cpu_limit;
    float ram_limit;
    std::string ping_host;
    int interval;

public:
    Config();
    bool loadConfig(const std::string& filename);
    
    float getCpuLimit() const;
    float getRamLimit() const;
    std::string getPingHost() const;
    int getInterval() const;
};

#endif
