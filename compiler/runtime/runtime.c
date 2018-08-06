#include <stdio.h>
#include <stdlib.h>

#define HEAP_SIZE 1000000

typedef long long obj;
void *INPUT;

obj global[NB_GLOBALS];
obj stack[MAX_STACK];
obj heap[HEAP_SIZE];

#define INT2OBJ(n) ((n) << 1)
#define OBJ2INT(o) ((o) >> 1)

#define PTR2OBJ(p) ((obj)(p) + 1)
#define OBJ2PTR(o) ((obj*)((o) - 1))

#define FALSEOBJ INT2OBJ(0)
#define TRUEOBJ INT2OBJ(1)

#define GLOBAL(i) global[i]
#define LOCAL(i) stack[i]
#define CLOSURE_REF(self,i) OBJ2PTR(self)[i]

#define TOS() sp[-1]
#define PUSH(x) *sp++ = x
#define POP() *--sp

#define EQ() { obj y = POP(); TOS() = INT2OBJ(TOS() == y); }
#define LT() { obj y = POP(); TOS() = INT2OBJ(TOS() < y); }
#define ADD() { obj y = POP(); TOS() = TOS() + y; }
#define ADD3() { obj y = POP(); obj z = POP(); TOS() = TOS() + y + z; }
#define NEWVEC() { long long s = OBJ2INT(TOS()); printf("Allocating %lld bytes\n", s); char *p = (char*)malloc(s); sprintf(p, "INPUT STRING %lld\n", s);printf("PTR %0X %s\n", p, p); TOS() = PTR2OBJ(p); }
#define GETINPUTBUFFER() { TOS() = PTR2OBJ(INPUT); }
#define PEEKBYTE() { obj y = OBJ2INT(POP()); void * ss = OBJ2PTR(TOS()); char *s = ss; TOS() = INT2OBJ(s[y]); }
#define PRINTVEC() { long long ss = OBJ2PTR(TOS()); char * s = ss;printf("PTR = %0X\n", s);  printf("STRING =%s\n", s); TOS() = 2*1234; }
#define SUB() { obj y = POP(); TOS() = TOS() - y; }
#define MUL() { obj y = POP(); TOS() = INT2OBJ(OBJ2INT(TOS()) * OBJ2INT(y)); }
#define DISPLAY() printf ("%lld", OBJ2INT(TOS()))
#define HALT() break

#define BEGIN_CLOSURE(label,nbfree) if (hp-(nbfree+1) < heap) hp = gc (sp);
#define INICLO(i) *--hp = POP()
#define END_CLOSURE(label,nbfree) *--hp = label; PUSH(PTR2OBJ(hp));

#define BEGIN_JUMP(nbargs) sp = stack;
#define END_JUMP(nbargs) pc = OBJ2PTR(LOCAL(0))[0]; goto jump;

obj *gc (obj *sp) { exit (1); } /* no GC! */

obj execute (void *input)
{
  int pc = 0;
  obj *sp = stack;
  obj *hp = &heap[HEAP_SIZE];
  INPUT = input;

  jump: switch (pc) {

//__SCHEME_CODE__
  }
  return POP();
}

#ifdef __STANDALONE_EXE__
char *ptr="ABCD";
int main () { printf ("result = %lld\n", OBJ2INT(execute (ptr))); return 0; }
#endif 
