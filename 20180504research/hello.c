#include <stdio.h>
#include <unistd.h>
int print(int n,char* s)
{
printf ("number is %d\n", n);
if(n==10000)
  printf ("string is %s\n", s);
return 0;
}

int main()
{
int i=0;
printf ("!!!f() is at %p\n", print);
while(1)
{
 print(i,"ok");
 i++;
sleep(1);
}


return 0;
}
