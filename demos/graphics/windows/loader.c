#include <windows.h>
#include <sys/stat.h>

HANDLE DL_LOADER_HANDLE = NULL;
SYSTEMTIME time;
BOOL FIRSTCALL = TRUE;

BOOL hasFileChanged()
{
    FILETIME ftCreate, ftAccess, ftWrite;
    SYSTEMTIME tempTime;
    DWORD dwRet;

    HANDLE hFile = CreateFile("../render.scm", GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, 0, NULL);

    // Retrieve the file times for the file.
    if (!GetFileTime(hFile, &ftCreate, &ftAccess, &ftWrite))
        return FALSE;
    CloseHandle(hFile);
    FileTimeToSystemTime(&ftWrite, &tempTime);

    if (
            tempTime.wYear > time.wYear  ||
            tempTime.wMonth > time.wMonth  ||
            tempTime.wDayOfWeek > time.wDayOfWeek  ||
            tempTime.wDay > time.wDay  ||
            tempTime.wHour > time.wHour  ||
            tempTime.wMinute > time.wMinute  ||
            tempTime.wSecond > time.wSecond  ||
            tempTime.wMilliseconds > time.wMilliseconds
       )
    {
        time = tempTime;
        return TRUE;
    }
    else
    {
        return FALSE;
    }
}

RENDERER_TYPE loadRenderer()
{
    if (hasFileChanged())
    {
        system("rebuild.bat");
        if (DL_LOADER_HANDLE != NULL || FIRSTCALL)
        {
            FreeLibrary(DL_LOADER_HANDLE);
            CopyFile("_render.dll", "render.dll", 0);
        }

        printf("Loading library...\n");
        DL_LOADER_HANDLE = LoadLibrary("render.dll");
        printf("%p\n", DL_LOADER_HANDLE);
        RENDERER = (RENDERER_TYPE)GetProcAddress(DL_LOADER_HANDLE, "execute");
    }

    FIRSTCALL = FALSE;
    return RENDERER;
}
