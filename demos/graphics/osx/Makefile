video.exe: ../video.c loader.c
	gcc -D_OS_IS_OSX_ ../video.c -o video.exe -lSDL2

render.dll: ../render.scm
	python3 ../../../s2c.py -dll ../render.scm > render.c
	gcc -D_OS_IS_OSX_ -dynamiclib render.c -o render.dll
