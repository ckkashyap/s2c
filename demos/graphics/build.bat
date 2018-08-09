@echo off

cl /D_OS_IS_WINDOWS_ video.c /I include lib\x64\SDL2.lib  /Fe:video.exe
python ../../s2c.py -dll render.scm > render.c
cl /D_OS_IS_WINDOWS_ /LD render.c 
