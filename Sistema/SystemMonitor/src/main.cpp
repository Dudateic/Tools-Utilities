#include "../include/config.hpp"
#include "../include/cpu_monitor.hpp"
#include "../include/ram_monitor.hpp"
#include "../include/network_monitor.hpp"
#include "../include/logger.hpp"

#include <gtkmm.h>
#include <iomanip>
#include <sstream>
#include <string>

class MonitorWindow : public Gtk::Window {
private:
    Config config;

    Gtk::Box mainBox;
    Gtk::Label titleLabel;

    Gtk::Frame cpuFrame;
    Gtk::Box cpuBox;
    Gtk::Label cpuLabel;
    Gtk::ProgressBar cpuBar;

    Gtk::Frame ramFrame;
    Gtk::Box ramBox;
    Gtk::Label ramLabel;
    Gtk::ProgressBar ramBar;

    Gtk::Frame networkFrame;
    Gtk::Box networkBox;
    Gtk::Label networkLabel;
    Gtk::Label latencyLabel;

    Gtk::Frame configFrame;
    Gtk::Box configBox;
    Gtk::Label configLabel;

    Gtk::Frame alertFrame;
    Gtk::Box alertBox;
    Gtk::Label alertLabel;

    sigc::connection timerConnection;

public:
    MonitorWindow()
        : mainBox(Gtk::ORIENTATION_VERTICAL, 12),
          cpuBox(Gtk::ORIENTATION_VERTICAL, 6),
          ramBox(Gtk::ORIENTATION_VERTICAL, 6),
          networkBox(Gtk::ORIENTATION_VERTICAL, 6),
          configBox(Gtk::ORIENTATION_VERTICAL, 6),
          alertBox(Gtk::ORIENTATION_VERTICAL, 6) {

        set_title("System Monitor");
        set_default_size(520, 420);
        set_border_width(16);

        if (!config.loadConfig("config.ini")) {
            config = Config();
            Logger::log("config.ini nao encontrado. Usando configuracao padrao.");
        }

        Logger::log("System Monitor GUI iniciado");

        titleLabel.set_markup("<span size='xx-large' weight='bold'>System Monitor</span>");
        titleLabel.set_halign(Gtk::ALIGN_CENTER);

        setupCpuArea();
        setupRamArea();
        setupNetworkArea();
        setupConfigArea();
        setupAlertArea();

        mainBox.pack_start(titleLabel, Gtk::PACK_SHRINK);
        mainBox.pack_start(cpuFrame, Gtk::PACK_SHRINK);
        mainBox.pack_start(ramFrame, Gtk::PACK_SHRINK);
        mainBox.pack_start(networkFrame, Gtk::PACK_SHRINK);
        mainBox.pack_start(configFrame, Gtk::PACK_SHRINK);
        mainBox.pack_start(alertFrame, Gtk::PACK_SHRINK);

        add(mainBox);
        show_all_children();

        updateStatus();
        timerConnection = Glib::signal_timeout().connect(
            sigc::mem_fun(*this, &MonitorWindow::updateStatus),
            config.getInterval() * 1000
        );
    }

    ~MonitorWindow() override {
        if (timerConnection.connected()) {
            timerConnection.disconnect();
        }
        Logger::log("System Monitor GUI finalizado");
    }

private:
    void setupCpuArea() {
        cpuFrame.set_label("CPU");
        cpuFrame.set_shadow_type(Gtk::SHADOW_ETCHED_IN);
        cpuBar.set_show_text(true);
        cpuBox.set_border_width(10);
        cpuBox.pack_start(cpuLabel, Gtk::PACK_SHRINK);
        cpuBox.pack_start(cpuBar, Gtk::PACK_SHRINK);
        cpuFrame.add(cpuBox);
    }

    void setupRamArea() {
        ramFrame.set_label("Memoria RAM");
        ramFrame.set_shadow_type(Gtk::SHADOW_ETCHED_IN);
        ramBar.set_show_text(true);
        ramBox.set_border_width(10);
        ramBox.pack_start(ramLabel, Gtk::PACK_SHRINK);
        ramBox.pack_start(ramBar, Gtk::PACK_SHRINK);
        ramFrame.add(ramBox);
    }

    void setupNetworkArea() {
        networkFrame.set_label("Rede");
        networkFrame.set_shadow_type(Gtk::SHADOW_ETCHED_IN);
        networkBox.set_border_width(10);
        networkBox.pack_start(networkLabel, Gtk::PACK_SHRINK);
        networkBox.pack_start(latencyLabel, Gtk::PACK_SHRINK);
        networkFrame.add(networkBox);
    }

    void setupConfigArea() {
        configFrame.set_label("Configuracao");
        configFrame.set_shadow_type(Gtk::SHADOW_ETCHED_IN);
        configBox.set_border_width(10);
        configBox.pack_start(configLabel, Gtk::PACK_SHRINK);
        configFrame.add(configBox);

        std::stringstream ss;
        ss << "Limite CPU: " << config.getCpuLimit() << "% | "
           << "Limite RAM: " << config.getRamLimit() << "% | "
           << "Host: " << config.getPingHost() << " | "
           << "Intervalo: " << config.getInterval() << "s";
        configLabel.set_text(ss.str());
    }

    void setupAlertArea() {
        alertFrame.set_label("Alertas");
        alertFrame.set_shadow_type(Gtk::SHADOW_ETCHED_IN);
        alertBox.set_border_width(10);
        alertLabel.set_line_wrap(true);
        alertLabel.set_text("Nenhum alerta no momento.");
        alertBox.pack_start(alertLabel, Gtk::PACK_SHRINK);
        alertFrame.add(alertBox);
    }

    std::string formatPercent(float value) const {
        std::stringstream ss;
        ss << std::fixed << std::setprecision(2) << value << "%";
        return ss.str();
    }

    bool updateStatus() {
        float cpuUsage = CpuMonitor::getUsage();
        float ramUsage = RamMonitor::getUsage();
        bool networkOk = NetworkMonitor::ping(config.getPingHost());
        float latency = NetworkMonitor::getLatency();

        cpuLabel.set_text("Uso atual: " + formatPercent(cpuUsage));
        cpuBar.set_fraction(cpuUsage / 100.0f);
        cpuBar.set_text(formatPercent(cpuUsage));

        ramLabel.set_text("Uso atual: " + formatPercent(ramUsage));
        ramBar.set_fraction(ramUsage / 100.0f);
        ramBar.set_text(formatPercent(ramUsage));

        if (networkOk) {
            networkLabel.set_markup("<span foreground='green' weight='bold'>Rede: conectada</span>");
        } else {
            networkLabel.set_markup("<span foreground='red' weight='bold'>Rede: sem conexao</span>");
        }

        std::stringstream latencyStream;
        latencyStream << std::fixed << std::setprecision(2)
                      << "Latencia: " << latency << " ms";
        latencyLabel.set_text(latencyStream.str());

        std::stringstream logStream;
        logStream << std::fixed << std::setprecision(2)
                  << "CPU: " << cpuUsage << "% | RAM: " << ramUsage
                  << "% | Rede: " << (networkOk ? "OK" : "FAIL")
                  << " | Latencia: " << latency << " ms";
        Logger::log(logStream.str());

        std::stringstream alerts;
        bool hasAlert = false;

        if (cpuUsage > config.getCpuLimit()) {
            alerts << "CPU acima do limite: " << formatPercent(cpuUsage)
                   << " / limite " << formatPercent(config.getCpuLimit()) << "\n";
            hasAlert = true;
        }

        if (ramUsage > config.getRamLimit()) {
            alerts << "RAM acima do limite: " << formatPercent(ramUsage)
                   << " / limite " << formatPercent(config.getRamLimit()) << "\n";
            hasAlert = true;
        }

        if (!networkOk) {
            alerts << "Rede indisponivel. Falha ao pingar " << config.getPingHost() << "\n";
            hasAlert = true;
        }

        if (hasAlert) {
            alertLabel.set_markup("<span foreground='red' weight='bold'>" + alerts.str() + "</span>");
            Logger::log("ALERTA: " + alerts.str());
        } else {
            alertLabel.set_markup("<span foreground='green'>Nenhum alerta no momento.</span>");
        }

        return true;
    }
};

int main(int argc, char* argv[]) {
    auto app = Gtk::Application::create(argc, argv, "com.axio.systemmonitor");
    MonitorWindow window;
    return app->run(window);
}
