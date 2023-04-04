# Mkf-eu v1.2
CXX			:= g++
CXX_FLAGS	:= -Wall -Werror
EXTRA_NAME	:= cpp

SRC			:= src
BUILD		:= build
EXECUTABLE	:= test.exe

INCLUDE		:= -I include 
LIB			:=
LIBRARIES	:=

SRCS		:= $(wildcard $(SRC)/*.$(EXTRA_NAME) $(SRC)/**/*.$(EXTRA_NAME))
OBJS		:= $(patsubst $(SRC)/%.$(EXTRA_NAME),$(BUILD)/%.o,$(SRCS))

RM			:=
DIV			:=
ifeq ($(OS),Windows_NT)
# PLATFORM="Windows"
 RM			:= del /s /q /f
else
#  PLATFORM="Unix-Like"
 RM			:= rm -rf
endif



.PHONY: all
all:$(EXECUTABLE)
	@echo Success.

$(EXECUTABLE):$(OBJS)
	@echo Linking $@
	@$(CXX) $(CXX_FLAGS) $(INCLUDE) $^ $(LIB) $(LIBRARIES) -o $@

$(BUILD)/%.o: $(SRC)/%.$(EXTRA_NAME)
	@echo Compiling $@
	@if not exist $(dir $@) mkdir "$(dir $@)"
	@$(CXX) $(CXX_FLAGS) $(INCLUDE) -c $< -o $@

.PHONY: clean
clean:
	@echo remove $(BUILD)
	@$(RM) $(BUILD)
	@echo remove $(EXECUTABLE)
	@$(RM) $(EXECUTABLE)
