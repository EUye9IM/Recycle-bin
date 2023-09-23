#include "exhilbert.hpp"
#include <cmath>
#include <iomanip>
#include <iostream>

using namespace std;

int main(int argc, const char **argv) {
	int width = 0, height;
	if (argc == 3) {
		char c;
		int res1 = sscanf(argv[1], "%d%c", &width, &c);
		int res2 = sscanf(argv[2], "%d%c", &height, &c);
		if (res1 != 1 || res2 != 1 || width <= 0 || height <= 0) {
			width = 0;
		}
	}
	if (!width) {
		width = 4;
		height = 4;
	}

	ExHilbert exhilbert;
	exhilbert.setSize(width, height);

	int tab_width = log10(width * height) + 2;
	for (int i = 0; i < height; i++) {
		for (int j = 0; j < width; j++) {
			cout << setw(tab_width) << exhilbert.getSequence(j, i);
		}
		cout << endl;
	}
}
