#include <DES.h>
#include <bitset>
namespace DES {

int const INITIAL_PERMUTATION[64] = {
	58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
	62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
	57, 49, 41, 33, 25, 17, 9,	1, 59, 51, 43, 35, 27, 19, 11, 3,
	61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7};
int const FINAL_PERMUTATION[64] = {
	40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
	38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
	36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
	34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9,  49, 17, 57, 25};
int const EXPANSION_PERMUTATION[48] = {
	32, 1,	2,	3,	4,	5,	4,	5,	6,	7,	8,	9,	8,	9,	10, 11,
	12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 10, 21, 20, 21,
	22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1};
int const S_BOXES[8][4][16] = {
	{{14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7},
	 {0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8},
	 {4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0},
	 {15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13}},
	{{15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10},
	 {3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5},
	 {0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15},
	 {13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9}},
	{{10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8},
	 {13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1},
	 {13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7},
	 {1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12}},
	{{7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15},
	 {13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9},
	 {10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4},
	 {3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14}},
	{{2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9},
	 {14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6},
	 {4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14},
	 {11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3}},
	{{12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11},
	 {10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8},
	 {9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6},
	 {4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13}},
	{{4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1},
	 {13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6},
	 {1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2},
	 {6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12}},
	{{13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7},
	 {1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2},
	 {7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8},
	 {2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11}}};
int const P_BOX[32] = {16, 7, 20, 21, 29, 12, 28, 17, 1,  15, 23,
					   26, 5, 18, 31, 10, 2,  8,  24, 14, 32, 27,
					   3,  9, 19, 13, 30, 6,  22, 11, 4,  25};
int const PERMUTED_CHOICE_1[56] = {
	57, 49, 41, 33, 25, 17, 9,	1,	58, 50, 42, 34, 26, 18, 10, 2,	59, 51, 43,
	35, 27, 19, 11, 3,	60, 52, 44, 36, 63, 55, 47, 39, 31, 23, 15, 7,	62, 54,
	46, 38, 30, 22, 14, 6,	61, 53, 45, 37, 29, 21, 13, 5,	28, 20, 12, 4};
int const PERMUTED_CHOICE_2[48] = {
	14, 17, 11, 24, 1,	5,	3,	28, 15, 6,	21, 10, 23, 19, 12, 4,
	26, 8,	16, 7,	27, 20, 13, 2,	41, 52, 31, 37, 47, 55, 30, 40,
	51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32};
int const LEFT_SHIFTS[16] = {1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1};
/*Bite64类*/

Bit64::Bit64(){};
Bit64::Bit64(std::bitset<64> const &bs) { content = bs; }
Bit64::Bit64(char const *data) {
	for (int i = 0; i < 8; i++)
		for (int j = 0; j < 8; j++)
			content[i * 8 + j] = bool(data[i] & (1 << j));
}
Bit64::Bit64(std::string const data) {
	for (int i = 0; i < 8; i++)
		for (int j = 0; j < 8; j++)
			content[i * 8 + j] = bool(data[i] & (1 << j));
}
std::string Bit64::to_string() const {
	std::string retstr;
	char data[9] = {0};
	for (int i = 0; i < 8; i++)
		for (int j = 0; j < 8; j++)
			if (content[i * 8 + j])
				data[i] |= (1 << j);
	retstr = data;
	return retstr;
}
void Bit64::to_cstr(char *cstr) const {
	for (int i = 0; i < 8; i++)
		for (int j = 0; j < 8; j++)
			if (content[i * 8 + j])
				cstr[i] |= (1 << j);
	return;
}
Bit64 Bit64::operator^(Bit64 const &x) const {
	Bit64 ret(this->content ^ x.content);
	return ret;
}

/*内部函数*/

std::bitset<64> permutate(std::bitset<64> const &dataIn,
						  int const *PermutationTable) {
	std::bitset<64> dataOut;
	for (int i = 0; i < 64; i++)
		dataOut[i] = dataIn[PermutationTable[i] - 1];
	return dataOut;
}
std::bitset<32> pPermutate(std::bitset<32> const &dataIn) {
	std::bitset<32> dataOut;
	for (int i = 0; i < 32; i++)
		dataOut[i] = dataIn[P_BOX[i] - 1];
	return dataOut;
}
std::bitset<56> permutateChoice1(std::bitset<64> const &dataIn) {
	std::bitset<56> dataOut;
	for (int i = 0; i < 56; i++)
		dataOut[i] = dataIn[PERMUTED_CHOICE_1[i] - 1];
	return dataOut;
}
std::bitset<48> permutateChoice2(std::bitset<56> const &dataIn) {
	std::bitset<48> dataOut;
	for (int i = 0; i < 48; i++)
		dataOut[i] = dataIn[PERMUTED_CHOICE_2[i] - 1];
	return dataOut;
}
std::bitset<48> expand(std::bitset<32> const &dataIn) {
	std::bitset<48> dataOut;
	for (int i = 0; i < 48; i++)
		dataOut[i] = dataIn[EXPANSION_PERMUTATION[i] - 1];
	return dataOut;
}
std::bitset<32> compress(std::bitset<48> const &dataIn) {
	std::bitset<32> dataOut;
	for (int i = 0; i < 8; i++) {
		dataOut <<= 4;
		dataOut |= std::bitset<32>(
			S_BOXES[i][dataIn[i * 8] * 2 + dataIn[i * 8 + 5]]
				   [dataIn[i * 8 + 1] * 8 + dataIn[i * 8 + 2] * 4 +
					dataIn[i * 8 + 3] * 2 + dataIn[i * 8 + 4]]);
	}
	return dataOut;
}
std::bitset<32> fFunction(std::bitset<32> const &dataIn,
						  std::bitset<48> const &K) {
	return pPermutate(compress(expand(dataIn) ^ K));
}
inline void leftShift(std::bitset<28> &k) {
	bool l = k[27];
	k <<= 1;
	k |= l;
	return;
}
void getSubKeys(std::bitset<48> subKey[16], Bit64 const &key) {
	std::bitset<56> key56 = permutateChoice1(key.content);
	std::bitset<28> lKey = std::bitset<28>(key56.to_ullong() & 0xFFFFFFF);
	std::bitset<28> rKey =
		std::bitset<28>((key56 >> 28).to_ullong() & 0xFFFFFFF);
	for (int i = 0; i < 16; i++) {
		for (int j = 0; j < LEFT_SHIFTS[i]; j++) {
			leftShift(lKey);
			leftShift(rKey);
		}
		subKey[i] = permutateChoice2(
			std::bitset<56>((rKey.to_ullong() << 28) | lKey.to_ullong()));
	}
	return;
}
/*外部函数*/
void DES(Bit64 &dataOut, Bit64 const &key, Bit64 const &dataIn,
		 bool encryptMode) {
	std::bitset<48> K[16];
	std::bitset<32> lData[2], rData[2];
	std::bitset<64> data;

	getSubKeys(K, key);

	data = permutate(dataIn.content, INITIAL_PERMUTATION);
	lData[0] = std::bitset<32>(data.to_ullong() & 0xFFFFFFFF);
	rData[0] = std::bitset<32>((data >> 32).to_ullong() & 0xFFFFFFFF);
	if (encryptMode)
		for (int i = 0; i < 16; i++) {
			lData[(i + 1) % 2] = fFunction(rData[i % 2], K[i]);
			rData[(i + 1) % 2] = lData[i % 2] ^ lData[(i + 1) % 2];
			lData[(i + 1) % 2] = rData[i % 2];
		}
	else
		for (int i = 0; i < 16; i++) {
			lData[(i + 1) % 2] = fFunction(rData[i % 2], K[15 - i]);
			rData[(i + 1) % 2] = lData[i % 2] ^ lData[(i + 1) % 2];
			lData[(i + 1) % 2] = rData[i % 2];
		}

	dataOut.content = permutate(
		std::bitset<64>((lData[0].to_ullong() << 32) | rData[0].to_ullong()),
		FINAL_PERMUTATION);

	return;
};
void encipher(char *dataOut, char const *dataIn, char const *key) {
	Bit64 out;
	DES(out, key, Bit64(dataIn), 1);
	out.to_cstr(dataOut);
	return;
};
void decipher(char *dataOut, char const *dataIn, char const *key) {
	Bit64 out;
	DES(out, key, Bit64(dataIn), 0);
	out.to_cstr(dataOut);
	return;
};
Bit64 encipher(Bit64 const &dataIn, Bit64 const &key) {
	Bit64 out;
	DES(out, key, dataIn, 0);
	return out;
}
Bit64 decipher(Bit64 const &dataIn, Bit64 const &key) {
	Bit64 out;
	DES(out, key, dataIn, 1);
	return out;
}
} // namespace DES