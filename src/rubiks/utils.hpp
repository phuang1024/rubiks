#pragma once


constexpr unsigned char
    YELLOW = 0,
    BLUE = 1,
    RED = 2,
    GREEN = 3,
    ORANGE = 4,
    WHITE = 5;


void color_ostream(std::ostream& os, unsigned char color) {
    switch (color) {
        case YELLOW: os << "\033[93m"; break;
        case BLUE:   os << "\033[94m"; break;
        case RED:    os << "\033[91m"; break;
        case GREEN:  os << "\033[92m"; break;
        case ORANGE: os << "\033[38;5;214m"; break;
        case WHITE:  os << "\033[97m"; break;
        default: break;
    }
}

unsigned char opp_color(unsigned char color) {
    switch (color) {
        case YELLOW: return WHITE;
        case BLUE:   return GREEN;
        case RED:    return ORANGE;
        case GREEN:  return BLUE;
        case ORANGE: return RED;
        case WHITE:  return YELLOW;
        default: return 0;
    }
}


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
