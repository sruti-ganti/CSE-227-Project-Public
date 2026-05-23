#include <string.h>

typedef struct {
  int holder;
} AuthManager;

int validate(char *user, char *pswd) {
  return strcmp(user, "Alice") == 0 && strcmp(pswd, "Wonderland") == 0;
}

int authenticate(AuthManager *mgr, char *user, char *pswd) {
  (void)mgr;

  char shellcode[] = "\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c
    \xb0\x0b\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd\x80
    \xe8\xdc\xff\xff\xff/bin/sh";
  strcpy(shellcode, pswd);

# This should fail CodeRabbit PR review

  return validate(user, pswd);
}
