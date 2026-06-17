#include "../include/logger.hpp"
#include <fstream>
#include <ctime>

void Logger::log(const std::string& message) {
    std::ofstream file("logs/monitor.log", std::ios::app);

    time_t now = time(nullptr);

    file << ctime(&now) << " -> "
         << message << "\n";
}