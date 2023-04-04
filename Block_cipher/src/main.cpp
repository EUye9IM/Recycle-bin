#include <AES.h>
#include <NTL/ZZ.h>
#include <RSA.h>
#include <UI.h>
#include <iostream>
using namespace std;
using namespace NTL;
void saveRSAKey(int bits) {
	ui::printTitle("  生成RSA密钥  ");

	cout << endl << "生成密钥中……" << endl;
	RSA::privateKey priK;
	RSA::publicKey pubK;
	RSA::makeKey(priK, pubK, bits);

	cout << endl;
	cout << "private key:" << endl << endl;
	cout << "p=" << priK.p << endl << endl;
	cout << "q=" << priK.q << endl << endl;
	cout << "d=" << priK.d << endl << endl;
	cout << endl;
	cout << "public key:" << endl << endl;
	cout << "n=" << pubK.n << endl << endl;
	cout << "e=" << pubK.e << endl << endl;
	cout << endl;
	ui::pause("\n任意键继续……");
	ui::OptionC opt[] = {{'1', "保存到文件"}, {'0', "不保存"}, ui::END_OPTC};
	ui::showOptionC(opt);
	int choice = ui::inputOptionC(opt);
	if (opt[choice].c == '1') {
		string priFile = "rsa.pri", pubFile = "rsa.pub";
		cout << "请输入私钥文件文件名（默认 rsa.pri ）：" << endl;
		ui::getLine(priFile, "rsa.pri");
		cout << "请输入公钥文件文件名（默认 rsa.pub ）：" << endl;
		ui::getLine(pubFile, "rsa.pub");
		RSA::savePublicKey(pubK, pubFile);
		RSA::savePrivateKey(priK, priFile);
	}
	return;
}

void makeRSAKey() {
	ui::printTitle("  选择生成密钥位数  ");
	ui::OptionC const opt[] = {
		{'1', "512"}, {'2', "1024"}, {'0', "离开"}, ui::END_OPTC};
	ui::showOptionC(opt);
	int choice = ui::inputOptionC(opt);
	if (opt[choice].c == '0')
		return;

	int m;
	if (opt[choice].c == '1')
		m = 512;
	if (opt[choice].c == '2')
		m = 1024;
	saveRSAKey(m);
	return;
}
void title() {
	ui::OptionC const opt[] = {{'1', "生成RSA密钥"}, {'2', "文件加密"},
							   {'3', "文件解密"},
							   {'0', "离开"},		 ui::END_OPTC};
	while (1) {
		ui::printTitle("  AES加密工具  ");
		ui::showOptionC(opt);
		int choice = ui::inputOptionC(opt);
		if (opt[choice].c == '0')
			break;
		if (opt[choice].c == '1')
			makeRSAKey();
		if (opt[choice].c == '2')
			AES::encipher();
		if (opt[choice].c == '3')
			AES::decipher();
	}
	return;
}

int main() {
	ui::setcoder("utf-8");
	title();
	return 0;
}
