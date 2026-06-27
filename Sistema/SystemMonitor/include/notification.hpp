#ifndef NOTIFICATION_HPP
#define NOTIFICATION_HPP

#include <string>

class Notification {
public:
    static void send(const std::string& title, const std::string& message);
};

#endif
