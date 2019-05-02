#ifndef _ERRORES_
#define _ERRORES_
#include <stdio.h>
#define error_fatal(codigo, texto) do{
    fprintf(stderr,"%s %d: Error %s-%s",\
    _FILE_ , _LINE_, texto, stderror(codigo));
    abort();
} while(0);
#endif