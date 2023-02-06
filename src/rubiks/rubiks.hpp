#pragma once

#include <iostream>

#include "constants.hpp"


/**
 * Iterate over an array with a stride.
 */
struct StrideIter {
    uint8_t* ptr;
    int stride;

    StrideIter() : ptr(nullptr), stride(0) {
        set(nullptr, 0);
    }

    StrideIter(uint8_t* ptr, int stride) {
        set(ptr, stride);
    }

    void set(uint8_t* ptr, int stride) {
        this->ptr = ptr;
        this->stride = stride;
    }

    uint8_t& operator*() const {
        return *ptr;
    }

    void inc() {
        ptr += stride;
    }
};


/**
 * Standard NxNxN cube.
 */
class Cube {
private:
    uint8_t* state;

    /**
     * Will add size to sx, sy ONCE if they are below 0.
     */
    int offset(int face, int y, int x) const {
        if (y < 0)
            y += size;
        if (x < 0)
            x += size;
        return (face*size*size) + (y*size) + x;
    }

    uint8_t* address(int face, int y, int x) const {
        return state + offset(face, y, x);
    }

    /**
     * Iterate over one face, stepping dy and dx each time.
     */
    StrideIter get_iter(int face, int sy, int sx, int dy, int dx) {
        int delta = (dy * size) + dx;
        return StrideIter(address(face, sy, sx), delta);
    }

    /**
     * Rotates a face.
     * Does NOT change the lateral sides, which SHOULD be changed.
     * use slice() to achieve that.
     */
    void turn(int face, bool dir) {
        // Go ring by ring
        int num_rings = (size+1) / 2;
        for (int ring = 0; ring < num_rings; ring++) {
            int ring_size = size - 2*ring;
            if (ring_size == 1) {
                // Nothing to do
                continue;
            }
            int padding = (size - ring_size) / 2;
            // Inclusive; reprs bounds for this ring.
            int lbound = padding, ubound = size - padding - 1;

            StrideIter top = get_iter(face, lbound, lbound, 0, 1),
                       right = get_iter(face, lbound, ubound, 1, 0),
                       bottom = get_iter(face, ubound, ubound, 0, -1),
                       left = get_iter(face, ubound, lbound, -1, 0);

            for (int i = 0; i < ring_size-1; i++) {
                if (dir) {
                    uint8_t tmp = *top;
                    *top = *left;
                    *left = *bottom;
                    *bottom = *right;
                    *right = tmp;
                } else {
                    uint8_t tmp = *top;
                    *top = *right;
                    *right = *bottom;
                    *bottom = *left;
                    *left = tmp;
                }
                top.inc();
                right.inc();
                bottom.inc();
                left.inc();
            }
        }
    }

    /**
     * Rotate a slice.
     * Note: if depth is 0, it acts on the face.
     * BUT, only changes the lateral sides; the face itself is not rotated.
     * Call turn() with this to achieve a "real" turn.
     */
    void slice(int face, int depth, bool dir) {
        // First get the iterators for each side.
        // Unfortunately, just manual casework.
        StrideIter iters[4];
        switch (face) {
            case YELLOW:
                iters[0] = get_iter(BLUE, depth, 0, 0, 1);
                iters[1] = get_iter(RED, depth, 0, 0, 1);
                iters[2] = get_iter(GREEN, depth, 0, 0, 1);
                iters[3] = get_iter(ORANGE, depth, 0, 0, 1);
                break;
            case BLUE:
                iters[0] = get_iter(WHITE, depth, 0, 0, 1);
                iters[1] = get_iter(RED, -1, depth, -1, 0);
                iters[2] = get_iter(YELLOW, -depth-1, -1, 0, -1);
                iters[3] = get_iter(ORANGE, 0, -depth-1, 1, 0);
                break;
            case RED:
                iters[0] = get_iter(WHITE, 0, -depth-1, 1, 0);
                iters[1] = get_iter(GREEN, -1, depth, -1, 0);
                iters[2] = get_iter(YELLOW, 0, -depth-1, 1, 0);
                iters[3] = get_iter(BLUE, 0, -depth-1, 1, 0);
                break;
            case GREEN:
                iters[0] = get_iter(WHITE, -depth-1, -1, 0, -1);
                iters[1] = get_iter(ORANGE, -1, depth, -1, 0);
                iters[2] = get_iter(YELLOW, depth, 0, 0, 1);
                iters[3] = get_iter(RED, 0, -depth-1, 1, 0);
                break;
            case ORANGE:
                iters[0] = get_iter(WHITE, -1, depth, -1, 0);
                iters[1] = get_iter(BLUE, -1, depth, -1, 0);
                iters[2] = get_iter(YELLOW, -1, depth, -1, 0);
                iters[3] = get_iter(GREEN, 0, -depth-1, 1, 0);
                break;
            case WHITE:
                iters[0] = get_iter(GREEN, -depth-1, -1, 0, -1);
                iters[1] = get_iter(RED, -depth-1, -1, 0, -1);
                iters[2] = get_iter(BLUE, -depth-1, -1, 0, -1);
                iters[3] = get_iter(ORANGE, -depth-1, -1, 0, -1);
                break;
        }

        for (int i = 0; i < size; i++) {
            uint8_t tmp = *iters[0];
            if (dir) {
                *iters[0] = *iters[1];
                *iters[1] = *iters[2];
                *iters[2] = *iters[3];
                *iters[3] = tmp;
            } else {
                *iters[0] = *iters[3];
                *iters[3] = *iters[2];
                *iters[2] = *iters[1];
                *iters[1] = tmp;
            }
            iters[0].inc();
            iters[1].inc();
            iters[2].inc();
            iters[3].inc();
        }
    }

public:
    int8_t size;

    ~Cube() {
        delete[] state;
    }

    /**
     * Initializes it as solved.
     */
    Cube(int size) {
        state = new uint8_t[6 * size*size];
        this->size = size;

        for (int y = 0; y < size; y++) {
            for (int x = 0; x < size; x++) {
                for (int color = 0; color < 6; color++) {
                    *address(color, y, x) = color;
                }
            }
        }
    }


    /**
     * Prints a net of the cube.
     */
    friend std::ostream& operator<<(std::ostream& os, const Cube& cube) {
        int face_width = cube.size * 2;
        std::string face_sep(face_width, ' ');

        // Yellow
        for (int y = 0; y < cube.size; y++) {
            os << face_sep;
            for (int x = 0; x < cube.size; x++) {
                color_ostream(os, *cube.address(YELLOW, y, x));
                os << "# ";
            }
            os << '\n';
        }

        // Orange, blue, red
        for (int y = 0; y < cube.size; y++) {
            for (int x = 0; x < cube.size; x++) {
                color_ostream(os, *cube.address(ORANGE, y, x));
                os << "# ";
            }
            for (int x = 0; x < cube.size; x++) {
                color_ostream(os, *cube.address(BLUE, y, x));
                os << "# ";
            }
            for (int x = 0; x < cube.size; x++) {
                color_ostream(os, *cube.address(RED, y, x));
                os << "# ";
            }
            os << '\n';
        }

        // White
        for (int y = 0; y < cube.size; y++) {
            os << face_sep;
            for (int x = 0; x < cube.size; x++) {
                color_ostream(os, *cube.address(WHITE, y, x));
                os << "# ";
            }
            os << '\n';
        }

        // Green (reversed)
        for (int y = cube.size-1; y >= 0; y--) {
            os << face_sep;
            for (int x = cube.size-1; x >= 0; x--) {
                color_ostream(os, *cube.address(GREEN, y, x));
                os << "# ";
            }
            os << '\n';
        }

        return os;
    }
};
