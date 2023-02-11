#pragma once

#include <chrono>
#include <vector>

#include "rubiks.hpp"


/**
 * Milliseconds
 */
inline uint64_t time() {
    const auto now = std::chrono::system_clock::now().time_since_epoch();
    const uint64_t elapse = std::chrono::duration_cast<std::chrono::milliseconds>(now).count();
    return elapse;
}


struct SearchInfo {
    int depth;
    int nodes;
    uint64_t time_start;

    friend std::ostream& operator<<(std::ostream& os, const SearchInfo& info) {
        uint64_t elapse = time() - info.time_start;
        uint64_t nps = (uint64_t)info.nodes * 1000 / (elapse+1);
        os << "info\t"
           << "depth " << info.depth << "\t"
           << "nodes " << info.nodes << "\t"
           << "nps " << nps << "\t"
           << "time " << elapse << "\t";
        return os;
    }
};


/**
 * Run DFS with standard 3x3 moves.
 */
void dfs_3x3(Cube& cube, int depth, std::vector<Move>& r_moves);
