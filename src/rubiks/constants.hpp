#pragma once

#include "iostream"


constexpr unsigned char
    YELLOW = 0,
    BLUE = 1,
    RED = 2,
    GREEN = 3,
    ORANGE = 4,
    WHITE = 5;


void color_ostream(std::ostream& os, unsigned char color) {
    switch (color) {
        case YELLOW: os << "\033[1;33m"; break;
        case BLUE:   os << "\033[1;34m"; break;
        case RED:    os << "\033[1;31m"; break;
        case GREEN:  os << "\033[1;32m"; break;
        case ORANGE: os << "\033[38;5;214m"; break;
        case WHITE:  os << "\033[1;37m"; break;
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
