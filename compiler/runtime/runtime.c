#include <stdio.h>
#include <stdlib.h>

#define HEAP_SIZE 100000000

typedef unsigned char BYTE8;
typedef unsigned short BYTE16;
typedef unsigned int BYTE32;
typedef unsigned long long BYTE64;
// typedef long long obj;

typedef struct
{
    BYTE64 o;
} obj;


void *INPUT;

obj global[NB_GLOBALS];
obj stack[MAX_STACK];
// obj heap[HEAP_SIZE];
obj *heap;

obj INT2OBJ(BYTE64 i)
{
    obj o;
    o.o = i;
    return o;
}

BYTE64 OBJ2INT(obj o)
{
    return o.o;
}

obj PTR2OBJ(void *p)
{
    obj o;
    o.o = (BYTE64)p;
    return o;
}

void *OBJ2PTR(obj o)
{
    return (void *)o.o;
}


//#define INT2OBJ(n) n
//#define OBJ2INT(o) o

//#define PTR2OBJ(p) ((obj)p)
//#define OBJ2PTR(o) ((obj*)o)

#define FALSEOBJ INT2OBJ(0)
#define TRUEOBJ INT2OBJ(1)

#define GLOBAL(i) global[i]
#define LOCAL(i) stack[i]
#define CLOSURE_REF(self,i) ((obj *)OBJ2PTR(self))[i]

#define TOS() sp[-1]
#define PUSH(x) *sp++ = x
#define POP() *--sp

#define EQ() { obj o1 = POP(); obj o2 = POP(); BYTE64 v1 = o1.o; BYTE64 v2 = o2.o; obj result; result.o = v1 == v2; PUSH(result); }
#define EQPTR() { obj* p = OBJ2PTR(POP()); TOS() = INT2OBJ(OBJ2PTR(TOS()) == p); }
#define LT() { obj y = POP(); TOS() = INT2OBJ(TOS() < y); }
#define ADD() { obj o1 = POP(); obj o2 = POP(); BYTE64 v1 = o1.o; BYTE64 v2 = o2.o; obj result; result.o = v1 + v2; PUSH(result); }
#define ADD3() { obj y = POP(); obj z = POP(); TOS() = TOS() + y + z; }

#define NEWBUFFER() { long long size = OBJ2INT(TOS());  void *p = malloc(size); TOS() = PTR2OBJ(p); }
#define PRINTBUFFER() { unsigned long long i; BYTE64 size = OBJ2INT(POP());  BYTE8 *p  = (BYTE8*)OBJ2PTR(TOS());  TOS() = INT2OBJ(size); for(i = 0; i < size; i++) printf("<%02x> ", p[i]); printf("\n");}
#define GETINPUTBUFFER() { PUSH(PTR2OBJ(INPUT)); }
#define PEEK8() { BYTE64 idx = OBJ2INT(POP()); BYTE8 *buf = (BYTE8*)OBJ2PTR(TOS()); TOS() = INT2OBJ(buf[idx]); }
#define PEEK16() { BYTE64 idx = OBJ2INT(POP()); BYTE16 *buf = (BYTE16*)OBJ2PTR(TOS()); TOS() = INT2OBJ(buf[idx]); }
#define PEEK32() { BYTE64 idx = OBJ2INT(POP()); BYTE32 *buf = (BYTE32*)OBJ2PTR(TOS()); TOS() = INT2OBJ(buf[idx]); }
#define PEEK64() { BYTE64 idx = OBJ2INT(POP()); BYTE64 *buf = (BYTE64*)OBJ2PTR(TOS()); TOS() = INT2OBJ(buf[idx]); }
#define PEEKPTR() { BYTE64 idx = OBJ2INT(POP()); void **buf = (void*)OBJ2PTR(TOS()); TOS() = PTR2OBJ(buf[idx]); }

#define POKE8() { BYTE8 val = OBJ2INT(POP()); BYTE64 idx = OBJ2INT(POP()); BYTE8 *buf = (BYTE8*)OBJ2PTR(TOS()); buf[idx] = (BYTE8)val; TOS() = INT2OBJ(val); }
#define POKE16() { BYTE16 val = OBJ2INT(POP()); BYTE64 idx = OBJ2INT(POP()); BYTE16 *buf = (BYTE16*)OBJ2PTR(TOS()); buf[idx] = (BYTE16)val; TOS() = INT2OBJ(val); }
#define POKE32() { BYTE32 val = OBJ2INT(POP()); BYTE64 idx = OBJ2INT(POP()); BYTE32 *buf = (BYTE32*)OBJ2PTR(TOS()); buf[idx] = (BYTE32)val; TOS() = INT2OBJ(val); }
#define POKE64() { BYTE64 val = OBJ2INT(POP()); BYTE64 idx = OBJ2INT(POP()); BYTE64 *buf = (BYTE64*)OBJ2PTR(TOS()); buf[idx] = (BYTE64)val; TOS() = INT2OBJ(val); }
#define POKEPTR() { void *pointer = OBJ2PTR(POP()); BYTE64 idx = OBJ2INT(POP()); void **buf = OBJ2PTR(TOS()); buf[idx] = pointer; TOS() = PTR2OBJ(pointer); }

#define SUB() { obj o1 = POP(); obj o2 = POP(); BYTE64 v1 = o1.o; BYTE64 v2 = o2.o; obj result; result.o = v2 - v1; PUSH(result); }
#define MUL() { obj y = POP(); TOS() = INT2OBJ(OBJ2INT(TOS()) * OBJ2INT(y)); }
#define DISPLAY() printf ("%lld\n", OBJ2INT(TOS()))
#define HALT() break

obj *gc (obj *sp) { printf("RAN OUT OF HEAP\n"); exit (1); } /* no GC! */

// #define BEGIN_CLOSURE(label,nbfree) if (hp-(nbfree+1) < heap) hp = gc (sp);
void BEGIN_CLOSURE(obj **hp, obj **sp, int label, int nbfree)
{
    if ((*hp)-(nbfree+1) < heap) *hp = gc (*sp);
}

// #define INICLO(i) *--hp = POP()
void INICLO(obj **hpp, obj **spp, int i)
{
    (*spp)--;
    (*hpp)--;
    **hpp = **spp;
}


// #define END_CLOSURE(a, b, label,nbfree) *--hp = INT2OBJ(label); PUSH(PTR2OBJ(hp));
void END_CLOSURE(obj **hpp, obj **spp, int label, int nbfree)
{
    (*hpp)--;
    **hpp = INT2OBJ(label);

    **spp = PTR2OBJ(*hpp);
    (*spp)++;
}

//#define BEGIN_JUMP(nbargs) sp = stack;
void BEGIN_JUMP(obj **sp, int nbargs)
{
    *sp = stack;
}

// #define END_JUMP(nbargs) pc = OBJ2INT(((obj *)OBJ2PTR(LOCAL(0)))[0]); goto jump;
void END_JUMP(int *pc, int nbargs)
{
    *pc = OBJ2INT(((obj *)OBJ2PTR(LOCAL(0)))[0]);
}


#ifndef __STANDALONE_EXE__
#ifdef _OS_IS_WINDOWS_
__declspec(dllexport)
#endif
#endif
obj execute (void *input)
{
  int pc = 0;
  obj *sp = stack;
  heap = malloc(HEAP_SIZE*sizeof(obj));
  obj *hp = &heap[HEAP_SIZE];
  INPUT = input;

  jump: switch (pc) {

//__SCHEME_CODE__
  }
  free(heap);
  return POP();
}

#ifdef __STANDALONE_EXE__
char ptr[4];
int main () { ptr[0]='A'; ptr[1]='B'; ptr[2]='C'; ptr[3]='D';printf ("result = %lld\n", OBJ2INT(execute (ptr))); return 0; }
#endif 
