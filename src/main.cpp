#include <iostream>

#include <rubiks.hpp>


void scramble(Cube& cube) {
    Move moves[] = {
    Move(WHITE, true),
    Move(YELLOW, true),
    Move(YELLOW, true),
    Move(BLUE, false),
    Move(ORANGE, true),
    Move(ORANGE, true),
    Move(RED, true),
    Move(RED, true),
    Move(BLUE, true),
    Move(BLUE, true),
    Move(YELLOW, true),
    Move(YELLOW, true),
    Move(BLUE, false),
    Move(ORANGE, true),
    Move(ORANGE, true),
    Move(WHITE, true),
    Move(WHITE, true),
    Move(RED, true),
    Move(RED, true),
    Move(ORANGE, true),
    Move(GREEN, false),
    Move(RED, true),
    Move(RED, true),
    Move(WHITE, false),
    Move(ORANGE, false),
    Move(YELLOW, false),
    Move(ORANGE, false),
    Move(ORANGE, false),
    Move(YELLOW, true),
    Move(RED, false),
    };

    for (Move m: moves) {
        cube.push(m);
    }
}


int main() {
    Cube cube(3);
    scramble(cube);
    std::cout << cube << std::endl;
}
