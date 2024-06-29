#include <iostream>
#include <windows.h>
#include "Window.h"

int WINAPI wWinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPWSTR lpCmdLine, int nCmdShow)
{
    std::cout << "Creating Window\n";

    Window* pWindow = new Window();

    bool running = true;
    while (running)
    {
        if (!pWindow->ProcessMessages())
        {
            std::cout << "Closing Window\n";
            running = false;
        }

        // Render

        Sleep(10);
    }

    delete pWindow;
    return 0;
}