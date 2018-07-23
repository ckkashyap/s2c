# s2c - A Scheme to C compiler

This is a translation of the [scheme compiler](https://gist.github.com/nyuichi/1116686) by Marc Feeley (author of [gambit](http://gambitscheme.org/) into Python. More details about Marc's compiler can be found in this [presentation](http://churchturing.org/y/90-min-scc.pdf) and these videos [part1](https://www.youtube.com/watch?v=Bp89aBm9tGU) and [part2](https://www.youtube.com/watch?v=M4dwcdK5bxE). This is my attempt at trying to understand the implementation details. Perhaps the implementation being in Python (3.6.5) would make it accessible to more people.

## Giving it a spin

### Prerequisites
1. [Python](https://www.python.org) version >= 3.6.5
2. A 64bit C compiler. If you only have a 32bit C compiler then please edit runtime.c and change long long to int on line nuber 6 

#### Create a test scheme file, test.scm, with the following content.
```scheme
(+ 1 2)
```
#### Compile test.scm
```bash
python s2c.py test.scm > test.c
```
#### Compile the generated C
```bash
gcc test.c
```
#### Run the generated program
```bash
./a.out
3
```

## Why would anyone do this?

While Marc's "90 minutes scheme to C" is, in my opinion, simply brilliant and it's under 800 lines of code (and mind you, all lines are less than 80 chars long :)) - I found it hard to "get it". For example, I was a little stumped by define-type to start with. The videos and the presentation helped me understand "CPS conversion" and "Closure convesion" but when it came to code generation, it was not so clear.

Another "problem" with Marc's implementation is that it is in scheme. What I mean is that, you need a scheme interpreter/compiler to run the compiler. If you are on Linux, this is not an issue but it become a problem if you are on other platforms. Since I have to spend a lot of my time on Windows, it becomes challenging to set up a scheme compiler that could compile Marc's implementation and also allow me to tweak it to gain understanding.

## Why Python?

This is my second attempt at such a translation. My [first attempt](https://github.com/ckkashyap/scheme-to-c-compiler) was in Clojure. I switched it to Python because not everyone was excited when I told them that they need to install java to try out my compiler :( Python is a good alternative given its general acceptance in the industry and [semantic similarity](http://www.paulgraham.com/lispfaq1.html) with lisp/scheme.
