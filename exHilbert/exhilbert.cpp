#include "exhilbert.hpp"
#include <utility>

using std::pair;

/*
 * 表示遍历方向
 * 第一个字母表示方向（东南西北）
 * 第二个字母表示顺序（顺时针逆时针）
 * 例如 N|C 表示北面、顺时针，即左上角到右上角
 */
enum { N = 1, S = 2, W = 4, E = 8 };
enum { C = 16, A = 32 };

ExHilbert::ExHilbert()
	: width(0), height(0), size(0), sequence(nullptr), locate_w(nullptr),
	  locate_h(nullptr) {}
ExHilbert::~ExHilbert() { setSize(0, 0); }

#define GET_INDEX(x, y) (x + y * width)
#define SET_SEQ(x, y, i)                                                       \
	{                                                                          \
		locate_w[i] = x;                                                       \
		locate_h[i] = y;                                                       \
		sequence[GET_INDEX(x, y)] = i;                                         \
	}
using Pair = pair<int, int>;
int ExHilbert::cal(int orientation, int cur_seq, std::pair<int, int> left_top,
				   std::pair<int, int> right_bottom) {
	int seq = cur_seq;
	if (right_bottom.first - left_top.first > 1 &&
		right_bottom.second - left_top.second > 1) {
		// 分成四块
		int mid_x = (right_bottom.first + left_top.first) / 2;
		int mid_y = (right_bottom.second + left_top.second) / 2;
		if (right_bottom.first - left_top.first == 2 &&
			(orientation & (N | S))) {
			int ori = orientation ^ (N | S);
			if (orientation == (N | C) || orientation == (S | A)) {
				seq = cal(ori, seq, left_top,
						  Pair(left_top.first + 1, right_bottom.second));
				seq = cal(orientation, seq,
						  Pair(left_top.first + 1, left_top.second),
						  right_bottom);
			} else {
				seq = cal(ori, seq, Pair(left_top.first + 1, left_top.second),
						  right_bottom);
				seq = cal(orientation, seq, left_top,
						  Pair(left_top.first + 1, right_bottom.second));
			}
			return seq;
		}
		if (right_bottom.second - left_top.second == 2 &&
			(orientation & (W | E))) {
			int ori = orientation ^ (W | E);
			if (orientation == (W | A) || orientation == (E | C)) {
				seq = cal(ori, seq, left_top,
						  Pair(right_bottom.first, left_top.second + 1));
				seq = cal(orientation, seq,
						  Pair(left_top.first, left_top.second + 1),
						  right_bottom);
			} else {
				seq = cal(ori, seq, Pair(left_top.first, left_top.second + 1),
						  right_bottom);
				seq = cal(orientation, seq, left_top,
						  Pair(right_bottom.first, left_top.second + 1));
			}
			return seq;
		}
		if (right_bottom.first - left_top.first >
				right_bottom.second - left_top.second &&
			(orientation & (N | S))) {
			Pair tp(mid_x, left_top.second), bp(mid_x, right_bottom.second);
			if (orientation == (N | C) || orientation == (S | A)) {
				seq = cal(orientation, seq, left_top, bp);
				seq = cal(orientation, seq, tp, right_bottom);
			} else {
				seq = cal(orientation, seq, tp, right_bottom);
				seq = cal(orientation, seq, left_top, bp);
			}
			return seq;
		}
		if (right_bottom.first - left_top.first <
				right_bottom.second - left_top.second &&
			(orientation & (W | E))) {
			Pair lp(left_top.first, mid_y), rp(right_bottom.first, mid_y);
			if (orientation == (W | A) || orientation == (E | C)) {
				seq = cal(orientation, seq, left_top, rp);
				seq = cal(orientation, seq, lp, right_bottom);
			} else {
				seq = cal(orientation, seq, lp, right_bottom);
				seq = cal(orientation, seq, left_top, rp);
			}
			return seq;
		}
		switch (orientation) {
		case N | C:
			seq = cal(W | A, seq, left_top, Pair(mid_x, mid_y)); // 左上
			seq = cal(N | C, seq, Pair(left_top.first, mid_y),
					  Pair(mid_x, right_bottom.second));			 // 左下
			seq = cal(N | C, seq, Pair(mid_x, mid_y), right_bottom); // 右下
			seq = cal(E | A, seq, Pair(mid_x, left_top.second),
					  Pair(right_bottom.first, mid_y)); // 右上
			break;
		case N | A:
			seq = cal(E | C, seq, Pair(mid_x, left_top.second),
					  Pair(right_bottom.first, mid_y));				 // 右上
			seq = cal(N | A, seq, Pair(mid_x, mid_y), right_bottom); // 右下
			seq = cal(N | A, seq, Pair(left_top.first, mid_y),
					  Pair(mid_x, right_bottom.second));		 // 左下
			seq = cal(W | C, seq, left_top, Pair(mid_x, mid_y)); // 左上
			break;
		case S | C:
			seq = cal(E | A, seq, Pair(mid_x, mid_y), right_bottom); // 右下
			seq = cal(S | C, seq, Pair(mid_x, left_top.second),
					  Pair(right_bottom.first, mid_y));			 // 右上
			seq = cal(S | C, seq, left_top, Pair(mid_x, mid_y)); // 左上
			seq = cal(W | A, seq, Pair(left_top.first, mid_y),
					  Pair(mid_x, right_bottom.second)); // 左下
			break;
		case S | A:
			seq = cal(W | A, seq, Pair(left_top.first, mid_y),
					  Pair(mid_x, right_bottom.second));		 // 左下
			seq = cal(S | C, seq, left_top, Pair(mid_x, mid_y)); // 左上
			seq = cal(S | C, seq, Pair(mid_x, left_top.second),
					  Pair(right_bottom.first, mid_y));				 // 右上
			seq = cal(E | A, seq, Pair(mid_x, mid_y), right_bottom); // 右下
			break;
		case W | C:
			seq = cal(S | A, seq, Pair(left_top.first, mid_y),
					  Pair(mid_x, right_bottom.second));			 // 左下
			seq = cal(W | C, seq, Pair(mid_x, mid_y), right_bottom); // 右下
			seq = cal(W | C, seq, Pair(mid_x, left_top.second),
					  Pair(right_bottom.first, mid_y));			 // 右上
			seq = cal(N | A, seq, left_top, Pair(mid_x, mid_y)); // 左上
			break;
		case W | A:
			seq = cal(N | C, seq, left_top, Pair(mid_x, mid_y)); // 左上
			seq = cal(W | A, seq, Pair(mid_x, left_top.second),
					  Pair(right_bottom.first, mid_y));				 // 右上
			seq = cal(W | A, seq, Pair(mid_x, mid_y), right_bottom); // 右下
			seq = cal(S | C, seq, Pair(left_top.first, mid_y),
					  Pair(mid_x, right_bottom.second)); // 左下
			break;
		case E | C:
			seq = cal(N | A, seq, Pair(mid_x, left_top.second),
					  Pair(right_bottom.first, mid_y));			 // 右上
			seq = cal(E | C, seq, left_top, Pair(mid_x, mid_y)); // 左上
			seq = cal(E | C, seq, Pair(left_top.first, mid_y),
					  Pair(mid_x, right_bottom.second));			 // 左下
			seq = cal(S | A, seq, Pair(mid_x, mid_y), right_bottom); // 右下
			break;
		case E | A:
			seq = cal(S | C, seq, Pair(mid_x, mid_y), right_bottom); // 右下
			seq = cal(E | A, seq, Pair(left_top.first, mid_y),
					  Pair(mid_x, right_bottom.second));		 // 左下
			seq = cal(E | A, seq, left_top, Pair(mid_x, mid_y)); // 左上
			seq = cal(N | C, seq, Pair(mid_x, left_top.second),
					  Pair(right_bottom.first, mid_y)); // 右上
			break;
		};
		return seq;
	} else if (right_bottom.first - left_top.first > 1) {
		// 横的长条
		switch (orientation) {
		case N | C:
		case E | C:
		case E | A:
		case S | A:
			for (int i = left_top.first; i < right_bottom.first; i++) {
				SET_SEQ(i, left_top.second, seq)
				++seq;
			}
			break;
		default:
			for (int i = right_bottom.first - 1; i >= left_top.first; i--) {
				SET_SEQ(i, left_top.second, seq)
				++seq;
			}
			break;
		}
		return seq;
	} else {
		// 竖的长条
		switch (orientation) {
		case W | C:
		case S | C:
		case S | A:
		case E | A:
			for (int i = left_top.second; i < right_bottom.second; i++) {
				SET_SEQ(left_top.first, i, seq)
				++seq;
			}
			break;
		default:
			for (int i = right_bottom.second - 1; i >= left_top.second; i--) {
				SET_SEQ(left_top.first, i, seq)
				++seq;
			}
			break;
		}
		return seq;
	}
	return -1;
}
void ExHilbert::setSize(int width, int height) {
	if (sequence) {
		delete[] sequence;
	}
	if (locate_w) {
		delete[] locate_w;
	}
	if (locate_h) {
		delete[] locate_h;
	}
	this->width = 0;
	this->height = 0;
	size = 0;
	if (width <= 0 || height <= 0) {
		return;
	}
	this->width = width;
	this->height = height;
	size = width * height;
	sequence = new int[size];
	locate_w = new int[size];
	locate_h = new int[size];

	int orient = 0;
	if (width > height)
		orient = N | C;
	else
		orient = W | A;

	cal(orient, 0, Pair(0, 0), Pair(width, height));
}
int ExHilbert::getSequence(int x, int y) {
	if (x < 0 || x >= width || y < 0 || y >= height)
		return -1;
	return sequence[GET_INDEX(x, y)];
}
pair<int, int> ExHilbert::getLocation(int sequence) {
	if (sequence < 0 || sequence >= size)
		return pair<int, int>{-1, -1};
	return pair<int, int>{locate_w[sequence], locate_h[sequence]};
}
