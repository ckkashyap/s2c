video.exe: ../video.c loader.c
	gcc -D_OS_IS_LINUX_ ../video.c -o video.exe -lSDL2 -ldl

render.dll: ../render.scm
	python3 ../../../s2c.py -dll ../render.scm > render.c
	gcc -D_OS_IS_LINUX_ -shared -fPIC render.c -o render.dll

clean:
	rm -f render.dll render.c video.exe
