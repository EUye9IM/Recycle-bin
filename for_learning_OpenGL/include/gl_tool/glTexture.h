#ifndef TEXTURE_H
#define TEXTURE_H

#include <glad/glad.h>

#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
namespace glTool {

class Texture2D {
public:
	unsigned int ID;
	Texture2D(const char *texturePath, bool setFlipVertical=false);
	~Texture2D();
	/*
	 * axisNo = 0, 1
	 * param = GL_REPEAT,
	 *         GL_MIRRORED_REPEAT,
	 *         GL_CLAMP_TO_EDGE,
	 *         GL_CLAMP_TO_BORDER
	 */
	void setWrapping(int axisNo, GLint param);
	/*
	 * param = GL_NEAREST,
	 *         GL_LINEAR,
	 *         GL_NEAREST_MIPMAP_NEAREST,
	 *         GL_LINEAR_MIPMAP_NEAREST,
	 *         GL_NEAREST_MIPMAP_LINEAR,
	 *         GL_LINEAR_MIPMAP_LINEAR
	 */
	void setMinFiltering(GLint param);
	/*
	 * param = GL_NEAREST,
	 *         GL_LINEAR
	 */
	void setMagFiltering(GLint param);
	void use();
};
} // namespace glTool
#endif
