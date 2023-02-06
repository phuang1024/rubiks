#pragma once

#include <iostream>

#include "constants.hpp"


/**
 * Iterate over an array with a stride.
 */
struct StrideIter {
    uint8_t* ptr;
    int stride;

    StrideIter(uint8_t* ptr, int stride) : ptr(ptr), stride(stride) {}

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
    uint8_t size;

    int offset(int face, int y, int x) const {
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

public:
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
        for (int y = 0; y < 3; y++) {
            os << face_sep;
            for (int x = 0; x < 3; x++) {
                color_ostream(os, *cube.address(YELLOW, y, x));
                os << "# ";
            }
            os << '\n';
        }

        // Orange, blue, red
        for (int y = 0; y < 3; y++) {
            for (int x = 0; x < 3; x++) {
                color_ostream(os, *cube.address(ORANGE, y, x));
                os << "# ";
            }
            for (int x = 0; x < 3; x++) {
                color_ostream(os, *cube.address(BLUE, y, x));
                os << "# ";
            }
            for (int x = 0; x < 3; x++) {
                color_ostream(os, *cube.address(RED, y, x));
                os << "# ";
            }
            os << '\n';
        }

        // White
        for (int y = 0; y < 3; y++) {
            os << face_sep;
            for (int x = 0; x < 3; x++) {
                color_ostream(os, *cube.address(WHITE, y, x));
                os << "# ";
            }
            os << '\n';
        }

        // Green (reversed)
        for (int y = 2; y >= 0; y--) {
            os << face_sep;
            for (int x = 2; x >= 0; x--) {
                color_ostream(os, *cube.address(GREEN, y, x));
                os << "# ";
            }
            os << '\n';
        }

        return os;
    }
};
