#include <windows.h>
#include <sys/stat.h>

//struct timespec ts;
HANDLE DL_LOADER_HANDLE = NULL;

RENDERER_TYPE loadRenderer(char *library)
{
    // struct stat s;
    // lstat(library, &s);

    // if (ts.tv_nsec != s.st_mtimespec.tv_nsec)
    {
        // ts.tv_nsec = s.st_mtimespec.tv_nsec;

        if (DL_LOADER_HANDLE != NULL)
        {
            FreeLibrary(DL_LOADER_HANDLE);
        }

        printf("Loading %s\n", library);
        DL_LOADER_HANDLE = LoadLibrary(library);
        printf("%p\n", DL_LOADER_HANDLE);
        RENDERER = GetProcAddress(DL_LOADER_HANDLE, "execute");
    }

    return RENDERER;
}

