#pragma once


struct Move {
    int face;
    bool dir;
    // Slice start and end, not including end.
    int start;
    int end;

    /**
     * Unitialized; may contain garbage.
     */
    Move() {
    }

    /**
     * Only top layer
     * i.e. start = 0, end = 1
     */
    Move(int face, bool dir) {
        this->face = face;
        this->dir = dir;
        this->start = 0;
        this->end = 1;
    }

    Move(int face, bool dir, int start, int end) {
        this->face = face;
        this->dir = dir;
        this->start = start;
        this->end = end;
    }
};
