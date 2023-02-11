/**
 * This header contains all things related to solver.
 * Implementation is distributed across other files.
 */

#pragma once

#include <chrono>
#include <vector>

#include "hash.hpp"
#include "rubiks.hpp"


/**
 * Milliseconds
 */
inline uint64_t time() {
    const auto now = std::chrono::system_clock::now().time_since_epoch();
    const uint64_t elapse = std::chrono::duration_cast<std::chrono::milliseconds>(now).count();
    return elapse;
}


struct HashEntry {
    uint64_t hash;
    int8_t depth;
};

/**
 * Hash table for search.
 */
class HashTable {
public:
    int size;
    int used;

    ~HashTable() {
        delete[] _table;
    }

    HashTable(int size = 1000003) {
        this->size = size;
        used = 0;
        _table = new HashEntry[size];

        for (int i = 0; i < size; i++) {
            _table[i].depth = -1;
        }
    }

    inline int index(uint64_t hash) {
        return hash % size;
    }

    inline HashEntry& get(uint64_t hash) {
        return _table[index(hash)];
    }

    inline void set(uint64_t hash, int8_t depth) {
        HashEntry& entry = get(hash);
        if (entry.depth == -1) {
            used++;
        }
        entry.hash = hash;
        entry.depth = depth;
    }

private:
    HashEntry* _table;
};

inline uint64_t get_hash(const Cube& cube) {
    uint64_t hash = 0;
    for (int i = 0; i < 6*9; i++) {
        int col = cube.state[i];
        int idx = col * 54 + i;
        hash ^= HASH_VALUES[idx];
    }
    return hash;
}


struct SearchInfo {
    int depth;
    uint64_t nodes;
    int hashfull;
    uint64_t time_start;

    friend std::ostream& operator<<(std::ostream& os, const SearchInfo& info) {
        uint64_t elapse = time() - info.time_start;
        uint64_t nps = info.nodes * 1000 / (elapse+1);
        os << "info\t"
           << "depth " << info.depth << "\t"
           << "nodes " << info.nodes << "\t"
           << "nps " << nps << "\t"
           << "hashfull " << info.hashfull << "\t"
           << "time " << elapse << "\t";
        return os;
    }
};


/**
 * Run DFS with standard 3x3 moves.
 */
void dfs_3x3(HashTable& hash, Cube& cube, int depth, std::vector<Move>& r_moves);
