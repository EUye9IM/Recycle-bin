#include <cfgps/cfgps.h>
#include <cfgps/check.h>
#include <cstring>
#include <iostream>
using namespace std;
using namespace cfgps;
int main(int argc, const char **argv) {
	Parser p;
	p.set("num", 10);
	p.set(Type::STR,"app","string",Value{.Str="false"},CHECK_STR_VERIFY_YNTF);
	p.readFile("test.cfg");
	cout << p.success() << endl;
	cout << p.getInt("num") << endl;
	const char *s = p.getStr("app","string");
	cout << (CHECK_STR_VERIFY_T(Value{.Str = s}) ||
			 CHECK_STR_VERIFY_Y(Value{.Str = s}))
		 <<s<< endl;
	return 0;
}
