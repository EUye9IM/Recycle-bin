CXX			= g++
CXX_FLAGS	= -mwindows -std=c++17 -Wall -Werror -Wno-error=unused-variable -O2

LIBRARIES	= -lglfw3 -lgdi32 -lopengl32
EXECUTABLE	= app.exe

SRC			= src
INCLUDE		= include
LIB			= lib
BUILD		= build


OBJS		= $(patsubst $(SRC)/%.cpp,$(BUILD)/%.o,$(wildcard $(SRC)/*.cpp  $(SRC)/*/*.cpp $(SRC)/*/*/*.cpp $(SRC)/*/*/*/*.cpp))

all:$(EXECUTABLE)
	@cls
	@echo Success.

run: all
	@cls
	@./$(EXECUTABLE)

$(EXECUTABLE):$(OBJS)
	@cls
	@echo Linking $@

	@if not exist $(dir $@) mkdir "$(dir $@)"
	@$(CXX) $(CXX_FLAGS) -I$(INCLUDE) -L$(LIB) $^ -o $@ $(LIBRARIES)


$(BUILD)/%.o: $(SRC)/%.cpp 
	@cls
	@echo Compiling...
	@echo $@
	@echo [$(foreach i,$(OBJS), $(if $(findstring $@, $(i)),*))]

	@if not exist $(dir $@) mkdir "$(dir $@)"
	@$(CXX) $(CXX_FLAGS) -I$(INCLUDE) -L$(LIB) -c $< -o $@

.PHONY:clean
clean:
	@rmdir /S /Q "$(BUILD)" 2>nul || @echo >nul
	@del $(EXECUTABLE) 2>nul || @echo >nul

.PHONY:test
test:



