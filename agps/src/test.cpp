#include <agps/agps.h>
#include <agps/check.h>
#include <cstring>
#include <iostream>
using namespace std;
using namespace agps;

int main(int argc, const char **argv) {
	Parser pa;
	pa.add(Type::FLAG, 'h', "help", "show ussage page");
	pa.add(Type::INT, 0, "port", "port number [0-65535] default 80", false,
		   Value{.Int = 80}, CHECK_INT_BETWEEN(0, 65535));
	pa.add(Type::DEC, 0, "dec", "some double-type number default 114.514", false,
		   Value{.Dec = 114.514});
	pa.add(Type::STR, 'p', "ip", "ip address", true, VALUE_NONE,
		   CHECK_STR_IPADDR);
	pa.add(Type::STR, 0, "debug", "debug mode [y/n]", false, Value{.Str = "no"},
		   CHECK_STR_VERIFY);
	pa.parse(argc, argv);

	if (pa.get("help").Exist) {
		pa.printUsage();
		return 0;
	}
	if (!pa.success()) {
		cout << "Error : " << endl;
		cout << pa.error() << endl << endl;
		pa.printUsage();
		return 0;
	} else {
		cout << "success." << endl << endl;
		cout << "deamon " << pa.get("deamon").Exist << endl;
		cout << "port   " << pa.get("port").Int << endl;
		cout << "double " << pa.get("dec").Dec << endl;
		cout << "ip     " << pa.get("ip").Str << endl;
		cout << "debug  " << pa.get("debug").Str << endl << endl;

		cout << "rest cnt : " << pa.restCnt() << endl;
		for (int i = 0; i < pa.restCnt(); i++) {
			cout << pa.rest(i) << endl;
		}
	}
	return 0;
}