CC=g++
CFLAGS=-c -g -Wall -std=c++11
LDFLAGS=
LIBFLAGS=
SOURCES=$(wildcard *.cpp) $(wildcard */*.cpp)
OBJECTS=$(SOURCES:.cpp=.o)
EXECUTABLE=a
BINDIR=/usr/bin

all: $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(LDFLAGS) $(OBJECTS) -o $@ $(LIBFLAGS)

.cpp.o:
	$(CC) $(CFLAGS) $< -o $@ $(LIBFLAGS)

clean:
	rm *.o */*.o $(EXECUTABLE)
