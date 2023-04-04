/*--------------------------------
 * 类 C 语言词法分析，语法分析测试文件
 * 该 cpp 内容包含过程调用以及多种测试
 *------------------------------*/
// begin
// global variable
int a;
int b;
int c;

// program function
int program(int a, int b, int c)
{
    int i;
    int j;
    // assign sentence
	i = 0;
	// if sentence
    if(a>b)
    {
        j=a+(b*c+1);
    }
    else
    {
        j=a;
    }
//     while sentence
    while(i<=100)   // single line comment test
    {
        i=j*2;
    }
    return i;       // return test
}

// demo function
int demo(int a)
{
    a=a+2;
    return a*2;
}

/*****************************
* main 函数
*****************************/
int main(void)
{
    int a;
    int b;
    int c;
    if (1) {return;}
    a=3;
    b=4;
    c=2;
    a=program(a,b,demo(c));
    return;
}
// end all