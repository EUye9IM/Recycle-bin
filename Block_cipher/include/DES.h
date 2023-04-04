#pragma once
#include <bitset>
#include <string>
namespace DES {
struct Bit64 {
	std::bitset<64> content;
	Bit64();
	Bit64(std::bitset<64> const &bs);
	Bit64(char const *data);
	Bit64(std::string const data);
	void to_cstr(char *cstr)const;
	std::string to_string()const;
	Bit64 operator^(Bit64 const &x)const;
};
void DES(Bit64 &dataOut, Bit64 const &key, Bit64 const &dataIn,
		 bool encryptMode);
void encipher(char *dataOut, char const *dataIn, char const *key);
void decipher(char *dataOut, char const *dataIn, char const *key);
Bit64 encipher(Bit64 const &dataIn, Bit64 const &key);
Bit64 decipher(Bit64 const &dataIn, Bit64 const &key);
} // namespace DES