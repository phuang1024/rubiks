#include <iostream>

#include <rubiks.hpp>


int main() {
    Cube cube(3);
    std::cout << "Original\n" << cube << std::endl;
    cube.asdf();
}
