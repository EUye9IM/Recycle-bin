#编译器和编译选项
export CC=g++
export CFLAGS= -O2 -std=c++11 -static -pthread -Wall 
# -march=native

#输出文件名
OUTPUT=Block_cipher.exe
BUILDDIR=./build

export MKDIR=mkdir
export RD=rd /s /q


INCLUDEPATH=-I ./include 

LIBPATH=-L ./lib
LIB=-lntl
SRC=$(wildcard ./src/*.cpp)
OBJ=$(patsubst ./src/%.cpp,$(BUILDDIR)/obj/%.o,$(SRC))

all :  $(BUILDDIR) $(OBJ) 
	@echo build $(OUTPUT)
	@$(CC) $(CFLAGS)   $(INCLUDEPATH) $(OBJ) $(LIBPATH) $(LIB) -o $(BUILDDIR)/bin/$(OUTPUT)
	@echo Done.

$(BUILDDIR):
	-$(MKDIR) "$(BUILDDIR)/obj"
	-$(MKDIR) "$(BUILDDIR)/bin"

$(BUILDDIR)/obj/%.o:./src/%.cpp
	@echo compile: $(notdir $<)
	@$(CC) $(CFLAGS)  $(INCLUDEPATH) -c $< -o $@

clean:
	-$(RD) "$(BUILDDIR)"

run:$(BUILDDIR)/bin/$(OUTPUT)
	$(BUILDDIR)/bin/$(OUTPUT)

.PHONY:clean all run
