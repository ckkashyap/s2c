@echo off

python ../../../s2c.py -dll ../render.scm > render.c
cl /D_OS_IS_WINDOWS_ /LD render.c /Fe:_render.dll
