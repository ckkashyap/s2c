#include <stdio.h>
#include <stdlib.h>

#define HEAP_SIZE 1000000

typedef unsigned char BYTE8;
typedef unsigned short BYTE16;
typedef unsigned int BYTE32;
typedef unsigned long long BYTE64;
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
#define EQPTR() { obj* p = OBJ2PTR(POP()); TOS() = INT2OBJ(OBJ2PTR(TOS()) == p); }
#define LT() { obj y = POP(); TOS() = INT2OBJ(TOS() < y); }
#define ADD() { obj y = POP(); TOS() = TOS() + y; }
#define ADD3() { obj y = POP(); obj z = POP(); TOS() = TOS() + y + z; }

#define NEWBUFFER() { long long size = OBJ2INT(TOS());  void *p = malloc(size); TOS() = PTR2OBJ(p); }
#define PRINTBUFFER() { unsigned long long i; obj size = OBJ2INT(POP());  BYTE8 *p  = (BYTE8*)OBJ2PTR(TOS());  TOS() = INT2OBJ(size); for(i = 0; i < size; i++) printf("<%02x> ", p[i]); printf("\n");}
#define GETINPUTBUFFER() { PUSH(PTR2OBJ(INPUT)); }
#define PEEK8() { obj idx = OBJ2INT(POP()); BYTE8 *buf = (BYTE8*)OBJ2PTR(TOS()); TOS() = INT2OBJ(buf[idx]); }
#define PEEK16() { obj idx = OBJ2INT(POP()); BYTE16 *buf = (BYTE16*)OBJ2PTR(TOS()); TOS() = INT2OBJ(buf[idx]); }
#define PEEK32() { obj idx = OBJ2INT(POP()); BYTE32 *buf = (BYTE32*)OBJ2PTR(TOS()); TOS() = INT2OBJ(buf[idx]); }
#define PEEK64() { obj idx = OBJ2INT(POP()); BYTE64 *buf = (BYTE64*)OBJ2PTR(TOS()); TOS() = INT2OBJ(buf[idx]); }
#define PEEKPTR() { obj idx = OBJ2INT(POP()); obj *buf = (obj*)OBJ2PTR(TOS()); TOS() = PTR2OBJ(buf[idx]); }

#define POKE8() { obj val = OBJ2INT(POP()); obj idx = OBJ2INT(POP()); BYTE8 *buf = (BYTE8*)OBJ2PTR(TOS()); buf[idx] = (BYTE8)val; TOS() = INT2OBJ(val); }
#define POKE16() { obj val = OBJ2INT(POP()); obj idx = OBJ2INT(POP()); BYTE16 *buf = (BYTE16*)OBJ2PTR(TOS()); buf[idx] = (BYTE16)val; TOS() = INT2OBJ(val); }
#define POKE32() { obj val = OBJ2INT(POP()); obj idx = OBJ2INT(POP()); BYTE32 *buf = (BYTE32*)OBJ2PTR(TOS()); buf[idx] = (BYTE32)val; TOS() = INT2OBJ(val); }
#define POKE64() { obj val = OBJ2INT(POP()); obj idx = OBJ2INT(POP()); BYTE64 *buf = (BYTE64*)OBJ2PTR(TOS()); buf[idx] = (BYTE64)val; TOS() = INT2OBJ(val); }
#define POKEPTR() { obj *val = OBJ2PTR(POP()); obj idx = OBJ2INT(POP()); obj *buf = OBJ2PTR(TOS()); buf[idx] = (obj)val; TOS() = PTR2OBJ(val); }

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
char ptr[4];
int main () { ptr[0]='A'; ptr[1]='B'; ptr[2]='C'; ptr[3]='D';printf ("result = %lld\n", OBJ2INT(execute (ptr))); return 0; }
#endif 
