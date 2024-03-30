CC = clang 
CFLAGS = -Wall -pedantic -std=c99 
SWIG = swig

all: _phylib.so

phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -fPIC -c phylib.c -o phylib.o

libphylib.so: phylib.o
	$(CC) -shared -o libphylib.so phylib.o -lm

phylib_wrap.c: phylib.i libphylib.so
	$(SWIG) -python phylib.i

phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -c phylib_wrap.c -I/usr/include/python3.11/ -fPIC -o phylib_wrap.o

_phylib.so: phylib_wrap.o libphylib.so
	$(CC) $(CFLAGS) -shared phylib_wrap.o -L. -L/usr/include/python/3.11 -lpython3.11 -lphylib -o _phylib.so

clean:
	rm -f *.o *.so *.exe *.svg

# export LD_LIBRARY_PATH=`pwd`
