#include "gl_tool/glTexture.h"
#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
namespace glTool {

Texture2D::Texture2D(const char *texturePath, bool setFlipVertical) {
	glGenTextures(1, &ID);
	glBindTexture(GL_TEXTURE_2D, ID);
	setWrapping(0, GL_REPEAT);
	setWrapping(1, GL_REPEAT);
	// set texture filtering parameters
	setMinFiltering(GL_NEAREST_MIPMAP_LINEAR);
	setMagFiltering(GL_LINEAR);

	int width, height, nrChannels;
	if (setFlipVertical)
		stbi_set_flip_vertically_on_load(true);
	else
		stbi_set_flip_vertically_on_load(false);

	unsigned char *data =
		stbi_load(texturePath, &width, &height, &nrChannels, 0);
	if (data) {
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB,
					 GL_UNSIGNED_BYTE, data);
		glGenerateMipmap(GL_TEXTURE_2D);
	} else {
		std::cout << "Failed to load texture" << std::endl;
	}
	stbi_image_free(data);
}
Texture2D::~Texture2D() {}
void Texture2D::setWrapping(int axisNo, GLint param) {
	switch (axisNo) {
	case 0:
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, param);
		break;
	case 1:
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, param);
	}
	return;
}
void Texture2D::setMinFiltering(GLint param) {
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, param);
	return;
}
void Texture2D::setMagFiltering(GLint param) {
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, param);
	return;
}
void Texture2D::use() { glBindTexture(GL_TEXTURE_2D, ID); }

} // namespace glTool