#pragma once
#include <NTL/ZZ.h>
#include <string>
namespace RSA {
struct privateKey {
	NTL::ZZ p, q, d; // a=d
};
struct publicKey {
	NTL::ZZ n, e; // b=e
};
void makeKey(privateKey &priK, publicKey &pubK, int bits);
void savePrivateKey(privateKey const &key, std::string const &file);
void savePublicKey(publicKey const &key, std::string const &file);
/*  读取私钥
返回：0（成功） / 1（失败）
*/
int loadPrivateKey(privateKey &priK, std::string const &file);
/*  读取公钥
返回：0（成功） / 1（失败）
*/
int loadPublicKey(publicKey &pubK, std::string const &file);
NTL::ZZ encipher(NTL::ZZ data, publicKey const &key);
NTL::ZZ decipher(NTL::ZZ data, privateKey const &key);
} // namespace RSA