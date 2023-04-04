#include <DES.h>
#include <NTL/ZZ.h>
#include <X917.h>
#include <bitset>
#include <ctime>
#include <random>
using std::bitset;
using namespace NTL;
using namespace DES;
ZZ X917rand(bitset<64> const &seed, int m) {
	Bit64 k1(rand()), k2(rand());
	Bit64 s(seed);
	Bit64 D(bitset<64>(time(NULL)));
	Bit64 l = encipher(decipher(encipher(D, k1), k2), k1);
	Bit64 x;
	ZZ ret(0);
	for (int i = 0; i < m; i++) {
		x = encipher(decipher(encipher(Bit64(l ^ s), k1), k2), k1);
		s = encipher(decipher(encipher(Bit64(l ^ x), k1), k2), k1);
		ret <<= 32;
		ret |= x.content.to_ullong()>>32;
		ret <<= 32;
		ret |= x.content.to_ullong()&(0xffffffff);
	}
	return ret;
}