#include <SDL2/SDL.h>
#include <stdio.h>

#define SCREEN_SIZE 800
#define SCREEN_WIDTH 640
#define SCREEN_HEIGHT 480
#define LIBRARY "render.dylib"

typedef struct
{
    int width;
    int height;
    unsigned char *pixels;
} INTEROP;

typedef int (*RENDERER_TYPE)(INTEROP*);

RENDERER_TYPE RENDERER;

#include "posix/loader.c"

int main(int argc, char* args[])
{
    SDL_Window* window = NULL;
    SDL_Surface* surface = NULL;

    if (SDL_Init(SDL_INIT_VIDEO) < 0)
    {
        fprintf(stderr, "%s\n", SDL_GetError());
        return 1;
    }

    window = SDL_CreateWindow
        (
            "hello sdl2 video",
            SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
            SCREEN_SIZE, SCREEN_SIZE,
            SDL_WINDOW_SHOWN
        );

    if (window == NULL)
    {
        fprintf(stderr, "%s\n", SDL_GetError());
        return 1;
    }

    surface = SDL_GetWindowSurface(window);
    SDL_FillRect(surface, NULL, SDL_MapRGBA(surface->format, 0xFF, 0x00, 0x00, 0x00));
    INTEROP interop;
    interop.pixels = surface->pixels;
    interop.width = SCREEN_SIZE;
    interop.height = SCREEN_SIZE;
    
    RENDERER = loadRenderer(LIBRARY);

    while(RENDERER(&interop))
    {
        SDL_UpdateWindowSurface(window);
        RENDERER = loadRenderer(LIBRARY);
    }

    SDL_DestroyWindow(window);
    SDL_Quit();
    return 0;
}
