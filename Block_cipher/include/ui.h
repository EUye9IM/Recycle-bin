#pragma once
#include <string>
namespace ui {
struct OptionC {
	char c;
	std::string str;
};
struct OptionI {
	int i;
	std::string str;
};
const OptionC END_OPTC = {0, ""};
const OptionI END_OPTI = {-1, ""};

// functions
void showOptionC(const OptionC *);
int inputOptionC(const OptionC *);
void showOptionI(const OptionI *);
int inputOptionI(const OptionI *);
void printTitle(std::string const &title);
void pause(std::string const &hint = "");
void cleanInputBuf();
std::string inputPassword(std::string const &hint = "");
/* 设置代码页
utf-8, GB18030
*/
void setcoder(const char *);
void progressBar(unsigned long long now, unsigned long long total = 0);
void clearScreen();
void getLine(std::string &str, std::string const &def = "");
} // namespace ui
