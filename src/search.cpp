#include <algorithm>
#include <cstring>

#include "solver.hpp"


bool criterion(Cube& cube) {
    int face_size = cube.size * cube.size;
    for (int col = 0; col < 6; col++) {
        uint8_t* start = cube.state + col*face_size;
        if (memcmp(start, start+1, face_size-1) != 0) {
            return false;
        }
        if (start[0] != col) {
            return false;
        }
    }
    return true;
}


/**
 * @param depth  Depth left.
 */
bool dfs(Cube& cube, int depth, SearchInfo& info, std::vector<Move>& r_moves, int prev_move = -1) {
    info.nodes++;
    if (depth == 0) {
        return criterion(cube);
    }

    int skip = (prev_move == -1) ? -1 : prev_move ^ 1;
    for (int i = 0; i < 12; i++) {
        if (i == skip) {
            continue;
        }

        Move move(i/2, i%2);
        cube.push(move);
        if (dfs(cube, depth-1, info, r_moves, i)) {
            r_moves.push_back(move);
            return true;
        }
        cube.push(move.reverse());
    }

    return false;
}


void dfs_3x3(Cube& cube, int depth, std::vector<Move>& r_moves) {
    SearchInfo info;
    info.nodes = 0;
    info.time_start = time();
    r_moves.clear();

    for (int d = 1; d <= depth; d++) {
        bool found = dfs(cube, d, info, r_moves);
        info.depth = d;
        std::cout << info << std::endl;
        if (found) {
            break;
        }
    }

    std::reverse(r_moves.begin(), r_moves.end());
}
