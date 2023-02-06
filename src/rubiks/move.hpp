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

    Move(int face, bool dir, int start, int end) {
        this->face = face;
        this->dir = dir;
        this->start = start;
        this->end = end;
    }
};
