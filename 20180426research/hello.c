#include <stdio.h>
#include <unistd.h>
void print(int n)
{
    printf("number is %d\n",n);
}

int main()
{
int i=0;
printf ("f() is at %p\n", print);
while(1)
{
 print(i);
 i++;
sleep(1);
}


return 0;
}
