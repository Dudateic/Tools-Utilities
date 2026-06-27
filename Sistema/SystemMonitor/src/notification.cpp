#include "../include/notification.hpp"
#include "../include/logger.hpp"
#include <cstdlib>

void Notification::send(const std::string& title, const std::string& message) {
    std::string command =
        "notify-send \"" + title + "\" \"" + message + "\"";

    int result = system(command.c_str());

    if (result != 0) {
        Logger::log("Falha ao enviar notificação: " + title + " - " + message);
    }
}
