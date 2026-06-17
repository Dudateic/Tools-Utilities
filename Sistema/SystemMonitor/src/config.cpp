#include "../include/config.hpp"
#include <fstream>
#include <sstream>

Config::Config() 
    : cpu_limit(80), ram_limit(80), ping_host("8.8.8.8"), interval(5) {
}

bool Config::loadConfig(const std::string& filename) {
    std::ifstream file(filename);
    
    if (!file.is_open()) {
        return false;
    }
    
    std::string line;
    while (std::getline(file, line)) {
        // Ignorar linhas vazias e comentários
        if (line.empty() || line[0] == ';') {
            continue;
        }
        
        // Ignorar seções
        if (line[0] == '[') {
            continue;
        }
        
        size_t pos = line.find('=');
        if (pos == std::string::npos) {
            continue;
        }
        
        std::string key = line.substr(0, pos);
        std::string value = line.substr(pos + 1);
        
        // Remover espaços em branco
        key.erase(key.find_last_not_of(" \t") + 1);
        value.erase(0, value.find_first_not_of(" \t"));
        
        if (key == "CPU_LIMIT") {
            cpu_limit = std::stof(value);
        } else if (key == "RAM_LIMIT") {
            ram_limit = std::stof(value);
        } else if (key == "PING_HOST") {
            ping_host = value;
        } else if (key == "INTERVAL") {
            interval = std::stoi(value);
        }
    }
    
    file.close();
    return true;
}

float Config::getCpuLimit() const {
    return cpu_limit;
}

float Config::getRamLimit() const {
    return ram_limit;
}

std::string Config::getPingHost() const {
    return ping_host;
}

int Config::getInterval() const {
    return interval;
}
