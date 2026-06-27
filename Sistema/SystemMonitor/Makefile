CXX = g++
TARGET = system_monitor_gui
BUILD_DIR = build
OBJ_DIR = $(BUILD_DIR)/obj
BIN_DIR = $(BUILD_DIR)/bin

CXXFLAGS = -std=c++17 -Wall -Wextra -O2 -Iinclude `pkg-config --cflags gtkmm-3.0`
LDFLAGS = `pkg-config --libs gtkmm-3.0`

SOURCES = src/main.cpp src/config.cpp src/cpu_monitor.cpp src/ram_monitor.cpp src/network_monitor.cpp src/logger.cpp
OBJECTS = $(patsubst src/%.cpp,$(OBJ_DIR)/%.o,$(SOURCES))

all: prepare $(TARGET)

prepare:
	mkdir -p logs
	mkdir -p $(OBJ_DIR)
	mkdir -p $(BIN_DIR)

$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJECTS) $(LDFLAGS)
	cp $(TARGET) $(BIN_DIR)/$(TARGET)

$(OBJ_DIR)/%.o: src/%.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

run: all
	env -u GTK_PATH -u LD_LIBRARY_PATH ./$(TARGET)

clean:
	rm -rf $(BUILD_DIR) $(TARGET)

clean-all: clean
	rm -rf logs

.PHONY: all prepare run clean clean-all
