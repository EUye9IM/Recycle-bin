#include <AES.h>
#include <AESSubFunctions.h>
#include <DES.h>
#include <NTL/ZZ.h>
#include <RSA.h>
#include <X917.h>
#include <fstream>
#include <iostream>
#include <string>
#include <ui.h>
using namespace std;
using namespace NTL;
namespace AES {

unsigned int const Scale = 40000;

ByteBlock operator^(ByteBlock const &A, ByteBlock const &B) {
	ByteBlock C;
	for (int i = 0; i < 4; i++)
		for (int j = 0; j < 4; j++)
			C.content[i][j] = A.content[i][j] ^ B.content[i][j];
	return C;
}
struct FileHead {
	Byte ckey[256]; // 加密后的密钥
	ByteBlock iv;	// 16Byte
};					// 272Byte

ByteBlock decryptOneBlock(ByteBlock const &dataIn, ByteBlock const &key) {
	ByteBlock keys[11];
	getSubKeys(keys, key);
	ByteBlock out = finalRound(dataIn, keys[10], 1);
	for (int i = 9; i >= 1; i--)
		out = commonRound(out, keys[i], 1);
	out = initialRound(out, keys[0]);
	return out;
}
ByteBlock encryptOneBlock(ByteBlock const &dataIn, ByteBlock const &key) {
	ByteBlock keys[11];
	getSubKeys(keys, key);
	ByteBlock out = initialRound(dataIn, keys[0]);
	for (int i = 1; i < 10; i++)
		out = commonRound(out, keys[i]);
	out = finalRound(out, keys[10]);
	return out;
}
unsigned long long getFileSize(ifstream &file) {
	file.seekg(0, ios::end);
	unsigned long long l = (unsigned long long)file.tellg();
	file.seekg(0, ios::beg);
	return l;
}
void encipher() {
	// filename
	string ifname, ofname, keyFName;
	// file stream
	ifstream iFile;
	ofstream oFile;
	// keys
	RSA::publicKey rsaKey;
	ZZ zzkey;
	ByteBlock bbkey;
	// 准备文件头
	FileHead fileHead;
	// iv
	ByteBlock bbiv;

	// begin
	ui::printTitle("  文件加密  ");

	// 打开文件
	cout << "请输入待加密文件文件名：" << endl;
	ui::getLine(ifname);
	iFile.open(ifname, ios::in | ios::binary);
	if (!iFile.is_open()) {
		ui::pause("\n待加密文件无法打开\n任意键继续……");
		return;
	}
	cout << "请输入加密后文件文件名（默认 " << ifname << ".aes ）：" << endl;
	ui::getLine(ofname, ifname + ".aes");
	// 添加后缀
	if (ofname.rfind(".aes") != ofname.length() - 4)
		ofname += ".aes";
	oFile.open(ofname, ios::out | ios::binary);
	if (!oFile.is_open()) {
		iFile.close(); // 关闭之前的文件
		ui::pause("\n加密后文件无法打开\n任意键继续……");
		return;
	}
	cout << "请输入公钥文件文件名（默认 rsa.pub ）：" << endl;
	ui::getLine(keyFName, "rsa.pub");
	if (RSA::loadPublicKey(rsaKey, keyFName)) {
		iFile.close(); // 关闭之前的文件
		oFile.close(); // 关闭之前的文件
		ui::pause("\n公钥文件无法打开\n任意键继续……");
		return;
	}

	// 随机一个 128bit key
	Byte bKey128[16];
	zzkey = X917rand(bitset<64>(rand()), 2);
	BytesFromZZ(bKey128, zzkey, 16);
	for (int i = 0; i < 4; i++)
		for (int j = 0; j < 4; j++)
			bbkey.content[j][i] = bKey128[i * 4 + j]; // [j][i]因为先填列
	// 准备文件头
	// 加密 128bitkey
	BytesFromZZ(fileHead.ckey, RSA::encipher(zzkey, rsaKey),
				sizeof(fileHead.ckey));
	// fileHead.iv
	Byte biv[16];
	BytesFromZZ(biv, X917rand(bitset<64>(rand()), 2), 16);
	for (int i = 0; i < 4; i++)
		for (int j = 0; j < 4; j++)
			// 应该先填列，想想区别不大，算了
			bbiv.content[i][j] = biv[i * 4 + j];

	fileHead.iv = bbiv;
	oFile.write((char const *)&fileHead, sizeof(fileHead));

	// 准备写入
	unsigned long long wroted = 0, fileSize = getFileSize(iFile);
	ui::progressBar(wroted, fileSize);
	ByteBlock bbC, bbP;
	unsigned int count = 0;
	// 检查一个 byteblock 可以被填满
	while (wroted + sizeof(ByteBlock) <= fileSize) {
		iFile.read((char *)&bbP, sizeof(ByteBlock));
		bbP = bbP ^ bbiv;
		bbC = encryptOneBlock(bbP, bbkey);
		// 更新iv
		bbiv = bbC;
		oFile.write((char const *)&bbC, sizeof(ByteBlock));
		wroted += sizeof(ByteBlock);
		count++;
		if (count == Scale) {
			count = 1;
			ui::progressBar(wroted);
		}
	}
	// 最后一个 byteblock
	Byte x = wroted + sizeof(ByteBlock) - fileSize;
	for (int i = 0; i < 4; i++)
		for (int j = 0; j < 4; j++) {
			bbP.content[i][j] = x;
		}

	if (x != sizeof(ByteBlock)) // 还有多的数据
		iFile.read((char *)&bbP, 16 - x);
	bbP = bbP ^ bbiv;
	bbC = encryptOneBlock(bbP, bbkey);
	oFile.write((char const *)&bbC, sizeof(ByteBlock));
	// 关闭文件
	iFile.close();
	oFile.close();
	ui::progressBar(fileSize);
	ui::pause("\n\n加密完成。任意键继续……");
	return;
}
void decipher() {
	// filename
	string ifname, ofname, keyFName;
	// file stream
	ifstream iFile;
	ofstream oFile;
	// keys
	RSA::privateKey rsaKey;
	ZZ zzkey;
	ByteBlock bbkey;
	// 准备文件头
	FileHead fileHead;
	// iv
	ByteBlock bbiv;

	// begin
	ui::printTitle("  文件解密  ");

	// 打开文件
	cout << "请输入待解密文件文件名：" << endl;
	ui::getLine(ifname);
	// 检查后缀
	if (ifname.length() > 4 && ifname.rfind(".aes") != ifname.length() - 4) {
		ui::pause("\n待解密文件应以 .aes 为后缀\n任意键继续……");
		return;
	}
	iFile.open(ifname, ios::in | ios::binary);
	if (!iFile.is_open()) {
		ui::pause("\n待加密文件无法打开\n任意键继续……");
		return;
	}
	cout << "请输入加密后文件文件名（默认 "
		 << ifname.substr(0, ifname.length() - 4) << " ）：" << endl;
	ui::getLine(ofname, ifname.substr(0, ifname.length() - 4));
	oFile.open(ofname, ios::out | ios::binary);
	if (!oFile.is_open()) {
		iFile.close(); // 关闭之前的文件
		ui::pause("\n加密后文件无法打开\n任意键继续……");
		return;
	}
	cout << "请输入公钥文件文件名（默认 rsa.pri ）：" << endl;
	ui::getLine(keyFName, "rsa.pri");
	if (RSA::loadPrivateKey(rsaKey, keyFName)) {
		iFile.close(); // 关闭之前的文件
		oFile.close(); // 关闭之前的文件
		ui::pause("\n私钥文件无法打开\n任意键继续……");
		return;
	}

	// 准备写入
	unsigned long long wroted = 0,
					   fileSize = getFileSize(iFile) - sizeof(fileHead);
	ByteBlock bbC, bbP;
	// 读取文件头
	iFile.read((char *)&fileHead, sizeof(FileHead));

	// 获得 128bit key
	Byte bKey128[16] = {0};
	zzkey = RSA::decipher(ZZFromBytes(fileHead.ckey, 256), rsaKey);
	BytesFromZZ(bKey128, zzkey, 16);
	for (int i = 0; i < 4; i++)
		for (int j = 0; j < 4; j++)
			bbkey.content[j][i] = bKey128[i * 4 + j]; // [j][i]因为先填列

	// iv
	bbiv = fileHead.iv;
	ui::progressBar(wroted, fileSize);
	unsigned int count=0;
	// 检查一个 byteblock 可以被填满
	while (wroted + sizeof(ByteBlock) < fileSize) {
		iFile.read((char *)&bbC, sizeof(ByteBlock));
		bbP = decryptOneBlock(bbC, bbkey);
		bbP = bbP ^ bbiv;
		// 更新iv
		bbiv = bbC;
		oFile.write((char const *)&bbP, sizeof(ByteBlock));
		wroted += sizeof(ByteBlock);
		count++;
		if (count == Scale) {
			count = 1;
			ui::progressBar(wroted);
		}
	}

	// 最后一个 byteblock
	iFile.read((char *)&bbC, sizeof(ByteBlock));
	bbP = decryptOneBlock(bbC, bbkey);
	bbP = bbP ^ bbiv;
	// 更新iv
	bbiv = bbC;
	Byte x = 16 - ((Byte const *)&bbP)[15];
	if (x != 0)
		oFile.write((char const *)&bbP, x);
	ui::progressBar(fileSize);

	// 关闭文件
	iFile.close();
	oFile.close();
	ui::progressBar(fileSize);
	ui::pause("\n\n解密完成。任意键继续……");
	return;
}
} // namespace AES