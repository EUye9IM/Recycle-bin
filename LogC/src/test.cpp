#include <logc/logc.h>

#include <iostream>
using namespace LogC;
int main() {
	if (log_open("test.log")) {
		std::cout << "cannot open file" << std::endl;
		return 0;
	}
	log_open(stdout);
	log_set(LOG_FLAG_DEBUG|LOG_FLAG_UTC);

	log_printf("%s\n", "test printf()");
	log_println("test println()");
	log_debug("test debug() %s:%d\n", __FILE__, __LINE__);
	log_fatal("test fatal() \n");
	std::cout << "log_fatal failed" << std::endl;
	log_close();
	return 0;
}