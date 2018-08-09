#include <stdio.h>
#include <dlfcn.h>
#include <sys/stat.h>

struct timespec ts;
void *DL_LOADER_HANDLE = NULL;

RENDERER_TYPE loadRenderer(char *library)
{
    struct stat s;
    lstat(library, &s);

    if (ts.tv_nsec != s.st_mtimespec.tv_nsec)
    {
        ts.tv_nsec = s.st_mtimespec.tv_nsec;

        if (DL_LOADER_HANDLE!=NULL)
        {
            dlclose(DL_LOADER_HANDLE);
        }

        DL_LOADER_HANDLE = dlopen(library, RTLD_NOW);
        RENDERER = dlsym(DL_LOADER_HANDLE, "execute");
    }

    return RENDERER;
}
