#pragma once

#include <utility>

class ExHilbert {
public:
	ExHilbert();
	~ExHilbert();
	// 设定平面尺寸
	void setSize(int width, int height);
	// 获取遍历序号
	int getSequence(int x, int y);
	// 获取遍历位置
	std::pair<int, int> getLocation(int sequence);

private:
	int cal(int orientation, int cur_seq, std::pair<int, int> left_top,
			std::pair<int, int> right_bottom);
	int width, height, size;
	int *sequence, *locate_w, *locate_h;
};
