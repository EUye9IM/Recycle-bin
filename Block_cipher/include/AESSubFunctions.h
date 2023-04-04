#pragma once

typedef unsigned char Byte;
struct ByteBlock {
	Byte content[4][4];
	ByteBlock(){};
	ByteBlock(Byte const b[4][4]) {
		for (int i = 0; i < 4; i++)
			for (int j = 0; j < 4; j++)
				content[i][j] = b[i][j];
	}
};
/* 初始轮
输入：数据块、密钥
输出：加密后数据块
*/
ByteBlock initialRound(ByteBlock const &dataIn, ByteBlock const &key);
/* 一般轮
输入：数据块、密钥
输出：加密后数据块
*/
ByteBlock commonRound(ByteBlock const &dataIn, ByteBlock const &key,
					  bool inverse = 0);
/* 末轮
输入：数据块、密钥
输出：加密后数据块
*/
ByteBlock finalRound(ByteBlock const &dataIn, ByteBlock const &key,
					 bool inverse = 0);
/* 获取子密钥
输入：数据块、密钥
输出：加密后数据块
*/
void getSubKeys(ByteBlock subKeys[11], ByteBlock const &key);