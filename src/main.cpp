#include <iostream>

#include "rubiks.hpp"
#include "solver.hpp"


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


void small_scramble(Cube& cube) {
    cube.push(Move(RED, true));
    cube.push(Move(YELLOW, true));
    cube.push(Move(BLUE, true));
    cube.push(Move(GREEN, true));
    cube.push(Move(WHITE, true));
    cube.push(Move(ORANGE, true));
}


int main() {
    Cube cube(3);
    small_scramble(cube);
    std::cout << cube << std::endl;

    HashTable hash;
    std::vector<Move> moves;
    dfs_3x3(hash, cube, 30, moves);
    std::cout << moves.size() << std::endl;
}
