#include <stdio.h>
#include <dlfcn.h>
#include <sys/stat.h>

struct timespec ts;
void *DL_LOADER_HANDLE = NULL;

#define LIBRARY "render.dll"

RENDERER_TYPE loadRenderer()
{
    struct stat s;

    system("make -s render.dll");
    lstat(LIBRARY, &s);

    if (ts.tv_nsec != s.st_mtim.tv_nsec)
    {
        ts.tv_nsec = s.st_mtim.tv_nsec;

        if (DL_LOADER_HANDLE!=NULL)
        {
            dlclose(DL_LOADER_HANDLE);
        }

        DL_LOADER_HANDLE = dlopen(LIBRARY, RTLD_NOW);
	printf("DL_LOADER_HANDLE = %p\n", DL_LOADER_HANDLE);
        RENDERER = dlsym(DL_LOADER_HANDLE, "execute");
    }

    return RENDERER;
}
