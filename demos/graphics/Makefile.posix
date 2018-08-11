video.exe: video.c posix/loader.c
	gcc video.c -o video.exe -lSDL2

render.dll: render.scm
	python3 ../../s2c.py -dll render.scm > render.c
	gcc -dynamiclib render.c -o render.dll
