#pragma once
#include<NTL/ZZ.h>
#include<bitset>
// 随机 返回 m*64 位 / 8 字节  二进制
NTL::ZZ X917rand(std::bitset<64> const&seed,int m);