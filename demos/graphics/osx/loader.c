#include <stdio.h>
#include <dlfcn.h>
#include <sys/stat.h>

struct timespec ts;
void *DL_LOADER_HANDLE = NULL;

#define LIBRARY "render.dll"

RENDERER_TYPE loadRenderer()
{
    struct stat s;
    lstat(LIBRARY, &s);

    system("make render.dll");

    if (ts.tv_nsec != s.st_mtimespec.tv_nsec)
    {
        ts.tv_nsec = s.st_mtimespec.tv_nsec;

        if (DL_LOADER_HANDLE!=NULL)
        {
            dlclose(DL_LOADER_HANDLE);
        }

        DL_LOADER_HANDLE = dlopen(LIBRARY, RTLD_NOW);
        RENDERER = dlsym(DL_LOADER_HANDLE, "execute");
    }

    return RENDERER;
}
