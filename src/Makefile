CXX = g++
CXXFLAGS = -std=c++17 -Wall -O3 -I./rubiks# -L./rubiks -lrubiks
CXXFILES = main.o search.o

.PHONY: build clean

build: $(CXXFILES)
	$(CXX) $(CXXFLAGS) $(CXXFILES) -o main.out

clean:
	rm -f *.o
