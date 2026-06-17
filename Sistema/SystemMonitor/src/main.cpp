#include "include/config.hpp"
#include "include/cpu_monitor.hpp"
#include "include/ram_monitor.hpp"
#include "include/network_monitor.hpp"
#include "include/logger.hpp"
#include <iostream>
#include <unistd.h>
#include <iomanip>
#include <sstream>

void displayStatus(float cpu, float ram, bool network, const Config& config) {
    std::cout << "\n=== SYSTEM MONITOR ===" << std::endl;
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "CPU Usage:    " << cpu << "% (Limit: " << config.getCpuLimit() << "%)" << std::endl;
    std::cout << "RAM Usage:    " << ram << "% (Limit: " << config.getRamLimit() << "%)" << std::endl;
    std::cout << "Network:      " << (network ? "OK" : "FAIL") << std::endl;
    std::cout << "Interval:     " << config.getInterval() << "s" << std::endl;
    std::cout << "=====================\n" << std::endl;
}

void logAlert(const std::string& component, float value, float limit) {
    std::stringstream ss;
    ss << std::fixed << std::setprecision(2);
    ss << "ALERT: " << component << " exceeded limit! Current: " << value 
       << "% (Limit: " << limit << "%)";
    Logger::log(ss.str());
}

int main() {
    Config config;
    
    // Carregar configuração
    if (!config.loadConfig("config.ini")) {
        std::cerr << "Erro ao carregar config.ini" << std::endl;
        return 1;
    }
    
    std::cout << "System Monitor iniciado" << std::endl;
    Logger::log("System Monitor iniciado");
    
    int interval = config.getInterval();
    
    // Loop principal de monitoramento
    while (true) {
        float cpuUsage = CpuMonitor::getUsage();
        float ramUsage = RamMonitor::getUsage();
        bool networkOk = NetworkMonitor::ping(config.getPingHost());
        
        // Exibir status
        displayStatus(cpuUsage, ramUsage, networkOk, config);
        
        // Verificar limites e logar alertas
        if (cpuUsage > config.getCpuLimit()) {
            logAlert("CPU", cpuUsage, config.getCpuLimit());
        }
        
        if (ramUsage > config.getRamLimit()) {
            logAlert("RAM", ramUsage, config.getRamLimit());
        }
        
        if (!networkOk) {
            Logger::log("ALERT: Network unreachable - Cannot ping " + config.getPingHost());
        }
        
        // Log normal
        std::stringstream ss;
        ss << std::fixed << std::setprecision(2);
        ss << "CPU: " << cpuUsage << "% | RAM: " << ramUsage << "% | Network: "
           << (networkOk ? "OK" : "FAIL");
        Logger::log(ss.str());
        
        // Aguardar intervalo
        sleep(interval);
    }
    
    Logger::log("System Monitor finalizado");
    return 0;
}
