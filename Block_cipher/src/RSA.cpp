//#include <DES.h>
#include <NTL/ZZ.h>
#include <RSA.h>
#include <X917.h>
#include <fstream>
#include <json.hpp>
#include <random>
#include <sstream>
#include <string>
using nlohmann::json;
using namespace NTL;
using namespace std;
namespace RSA {
template <typename T> string tostr(T t) {
	stringstream buf;
	buf << t;
	return buf.str();
}
ZZ atozz(string in) {
	ZZ zz;
	stringstream buf(in);
	buf >> zz;
	return zz;
}
bool is_Prime(const ZZ &n, long t) {
	if (n <= 1)
		return 0;
	// first, perform trial division by primes up to 2000
	PrimeSeq s; // a class for quickly generating primes in sequence
	long p;
	p = s.next(); // first prime is always 2
	while (p && p < 2000) {
		if ((n % p) == 0)
			return (n == p);
		p = s.next();
	}
	// second, perform t Miller-Rabin tests
	ZZ x;
	int i;
	for (i = 0; i < t; i++) {
		x = RandomBnd(n); // random number between 0 and n-1
		if (MillerWitness(n, x))
			return 0;
	}
	return 1;
}

ZZ getPrime(int bits) {
	ZZ prim;
	while (1) {
		prim = X917rand(bitset<64>(rand()), bits / 64);
		if (is_Prime(prim, bits))
			break;
	}
	return prim;
}
void savePrivateKey(privateKey const &key, std::string const &file) {
	json keyJson;
	keyJson["p"] = tostr(key.p);
	keyJson["q"] = tostr(key.q);
	keyJson["d"] = tostr(key.d);
	ofstream out(file, ios::out);
	out << keyJson.dump();
	out.close();
	return;
}
void savePublicKey(publicKey const &key, std::string const &file) {
	json keyJson;
	keyJson["n"] = tostr(key.n);
	keyJson["e"] = tostr(key.e);
	ofstream out(file, ios::out);
	out << keyJson.dump();
	out.close();
	return;
}
int loadPrivateKey(privateKey &priK, std::string const &file) {
	try {
		json keyJson;
		ifstream in(file, ios::in);
		in >> keyJson;
		in.close();
		priK.d = atozz(keyJson["d"].get<string>());
		priK.p = atozz(keyJson["p"].get<string>());
		priK.q = atozz(keyJson["q"].get<string>());
	} catch (exception const &e) {
		return 1;
	}
	return 0;
}
int loadPublicKey(publicKey &pubK, std::string const &file) {
	try {
		json keyJson;
		ifstream in(file, ios::in);
		in >> keyJson;
		in.close();
		pubK.e = atozz(keyJson["e"].get<string>());
		pubK.n = atozz(keyJson["n"].get<string>());
	} catch (exception const &e) {
		return 1;
	}
	return 0;
}

void makeKey(privateKey &priK, publicKey &pubK, int bits) {
	ZZ &p = priK.p, &q = priK.q, &n = pubK.n, &d = priK.d, &e = pubK.e;
	// p
	p = getPrime(bits);
	// q
	q = getPrime(bits);
	// n
	n = priK.p * priK.q;
	// e,d
	ZZ phyN = (p - 1) * (q - 1);
	while (1) {
		e = RandomBnd(phyN);
		if (InvModStatus(d, e, phyN) == 0)
			break;
	}
	return;
}
ZZ encipher(NTL::ZZ data, publicKey const &key) {
	return PowerMod(data, key.e, key.n);
}
ZZ decipher(NTL::ZZ data, privateKey const &key) {
	return PowerMod(data, key.d, key.p * key.q);
}
} // namespace RSA