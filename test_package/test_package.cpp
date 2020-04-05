#include <iostream>
#ifdef _WIN32
    #include <windows.h>
#endif
#ifdef __APPLE__
    #include <OpenGl/gl.h>
    #include <OpenGl/glu.h>
#else
    #include <GL/gl.h>
    #include <GL/glu.h>
#endif

int main()
{
    std::cout << "Bincrafters\n";
    return 0;
}
