CXX			= g++
CXX_FLAGS	= -Wall -Werror -O2 -std=c++11

LIBRARIES	=  -lglad -lglfw3 -lgdi32
EXECUTABLE	= app.exe

SRC			= src
INCLUDE		= include
LIB			= lib
BUILD		= build
RESOURCES	= resources
PUBLISH		= publish

OBJS		= $(patsubst $(SRC)/%.cpp,$(BUILD)/%.o,$(wildcard $(SRC)/*.cpp $(SRC)/*/*/*.cpp $(SRC)/*/*/*/*.cpp  $(SRC)/*/*.cpp))

all:$(PUBLISH)/$(EXECUTABLE)
	@xcopy /e /y /q $(RESOURCES) $(PUBLISH)
	@cls
	@echo Success.

run: all
	@cls
	@cd $(PUBLISH)&&$(EXECUTABLE)

$(PUBLISH)/$(EXECUTABLE):$(OBJS)
	@cls
	@echo Linking $@

	@if not exist $(dir $@) mkdir "$(dir $@)"
	@$(CXX) $(CXX_FLAGS) -I$(INCLUDE) -L$(LIB) $^ -o $@ $(LIBRARIES)


build/%.o: src/%.cpp 
	@cls
	@echo Compiling...
	@echo $@
	@echo [$(foreach i,$(OBJS), $(if $(findstring $@, $(i)),*))]

	@if not exist $(dir $@) mkdir "$(dir $@)"
	@$(CXX) $(CXX_FLAGS) -I$(INCLUDE) -L$(LIB) -c $< -o $@

.PHONY:clean
clean:
	@rmdir /S /Q "$(BUILD)" 2>nul || @echo >nul
	@rmdir /S /Q "$(PUBLISH)" 2>nul || @echo >nul

.PHONY:test
test:


