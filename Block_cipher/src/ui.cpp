#include "ui.h"
#include <Windows.h>
#include <conio.h>
#include <cstdio>
#include <cstring>
#include <iostream>
#include <string>
using namespace std;
namespace ui {
int static getStrlenUTF8(const char *str) {
	if (!str)
		return 0;
	int len = strlen(str);
	int ret = 0;
	for (const char *sptr = str; (sptr - str) < len && *sptr;) {
		unsigned char ch = (unsigned char)*sptr;
		if (ch < 0x80) {
			sptr++; // ascii
			ret++;
		} else if (ch < 0xc0) {
			sptr++;
		} else if (ch < 0xe0) {
			sptr += 2;
			ret++;
		} else if (ch < 0xf0) {
			sptr += 3; // chinese
			ret += 2;
		} else {
			sptr += 4;
			ret++;
		}
	}
	return ret;
}
void printTitle(string const &title) {
	clearScreen();
	int w = getStrlenUTF8(title.c_str());
	for (int i = 0; i < w; i++)
		putchar('=');
	putchar('\n');
	printf("%s\n", title.c_str());
	for (int i = 0; i < w; i++)
		putchar('=');
	putchar('\n');
	return;
}
void pause(string const &hint) {
	if (hint != "")
		printf("%s\n", hint.c_str());
	getch();
	return;
}
void showOptionC(const OptionC *opt) {
	const OptionC *p = opt;
	while (p->c) {
		printf(" %c.%s\n", p->c, p->str.c_str());
		p++;
	}
	return;
}
int inputOptionC(const OptionC *opt) {
	char c = 0;
	while (1) {
		int i = 0;
		c = getch();
		while (opt[i].c) {
			if (opt[i].c == c)
				return i;
			i++;
		}
	}
}

void showOptionI(const OptionI *opt) {
	const OptionI *p = opt;
	while (p->i >= 0) {
		printf(" %-4d %s\n", p->i, p->str.c_str());
		p++;
	}
	return;
}
int inputOptionI(const OptionI *opt) {
	int c = 0, t = 0;
	while (1) {
		int i = 0;
		c = scanf("%d", &t);
		cleanInputBuf();
		if (!c)
			continue;
		while (opt[i].i >= 0) {
			if (opt[i].i == t)
				return i;
			i++;
		}
	}
}
void cleanInputBuf() {
	while (getchar() != '\n')
		;
	return;
}
string inputPassword(string const &hint) {
	if (hint != "")
		printf("%s\n", hint.c_str());
	string ret = "";
	int c;
	int i = 0;
	while ((c = _getch())) {
		if (c == 13) {
			putchar('\n');
			ret.push_back(0);
			return ret;
		} else if (c == 8) {
			if (i) {
				i--;
				putchar('\b');
				putchar(' ');
				putchar('\b');
				ret.pop_back();
			}
		} else {
			putchar('*');
			i++;
			ret.push_back(char(c));
		}
	}
	return ret;
}
void progressBar(unsigned long long now, unsigned long long total) {
	static int p = 0;
	static unsigned long long t = 0;

	if (total != 0) {
		t = total;
		p = -1;
	}
	if (p != (int)(now * 1000 / t)) {
		CONSOLE_SCREEN_BUFFER_INFO binfo;
		static const HANDLE __hout = GetStdHandle(STD_OUTPUT_HANDLE);
		GetConsoleScreenBufferInfo(__hout, &binfo);

		p = (int)(now * 1000 / t);
		int len = binfo.srWindow.Right - binfo.srWindow.Left - 9;
		int n = ((now)*len / t);
		printf("\r[");
		for (int i = 0; i < len; i++)
			if (i <= n)
				printf("#");
			else
				printf("-");
		printf("] %.1f%%", (now < t ? now : t) * 100.0 / t);
	}
	return;
}
void setcoder(const char *str) {
	if (!strcmp(str, "utf-8"))
		system("CHCP 65001>nul");
	if (!strcmp(str, "GB18030"))
		system("CHCP 54936>nul");
	return;
}
void clearScreen() {
	system("cls");
	return;
}
void getLine(std::string &str, std::string const &def) {
	getline(cin, str);
	if (str == "") {
		str = def;
	}
	return;
}
} // namespace ui