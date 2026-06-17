CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra -O2 -I.
TARGET = system_monitor
BUILD_DIR = build
OBJ_DIR = $(BUILD_DIR)/obj
BIN_DIR = $(BUILD_DIR)/bin

SOURCES_DIR = .
SOURCES_STRUCTURED = src/main.cpp src/logger.cpp src/config.cpp src/cpu_monitor.cpp src/ram_monitor.cpp src/network_monitor.cpp
SOURCES_FLAT = src_main.cpp src_logger.cpp src_config.cpp src_cpu_monitor.cpp src_ram_monitor.cpp src_network_monitor.cpp

ifeq ($(wildcard src/main.cpp),)
	SOURCES = $(SOURCES_FLAT)
else
	SOURCES = $(SOURCES_STRUCTURED)
	CXXFLAGS += -Iinclude
endif

OBJECTS = $(addprefix $(OBJ_DIR)/,$(notdir $(SOURCES:.cpp=.o)))

all: prepare $(TARGET)

prepare:
	mkdir -p logs
	mkdir -p $(OBJ_DIR)
	mkdir -p $(BIN_DIR)

$(TARGET): $(OBJECTS) | $(BIN_DIR)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJECTS)
	cp $(TARGET) $(BIN_DIR)/$(TARGET)

$(OBJ_DIR)/%.o: %.cpp | $(OBJ_DIR)
	$(CXX) $(CXXFLAGS) -c $< -o $@
	echo "  Compilado: $<"

$(OBJ_DIR)/%.o: src/%.cpp | $(OBJ_DIR)
	$(CXX) $(CXXFLAGS) -c $< -o $@

$(OBJ_DIR):
	mkdir -p $(OBJ_DIR)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

clean:
	rm -rf $(BUILD_DIR) $(TARGET)

clean-all: clean
	rm -rf logs/

organize:
	bash organize.sh

run: $(TARGET) prepare
	./$(TARGET)

.PHONY: all prepare clean clean-all organize run debug help