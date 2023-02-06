#pragma once

#include <iostream>

#include "constants.hpp"


/**
 * Standard NxNxN cube.
 */
class Cube {
public:
    uint8_t* state;
    uint8_t size;

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

    uint8_t* address(int face, int y, int x) const {
        return state + (face*size*size) + (y*size) + x;
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
