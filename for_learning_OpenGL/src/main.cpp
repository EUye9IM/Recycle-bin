#include "camera_ex.hpp"
#include "gl_tool/glBlueprints.hpp"
#include "gl_tool/glCommonTools.hpp"
#include "gl_tool/glModule.h"
#include "gl_tool/glShader.h"
#include "gl_tool/glTexture.h"
#include "gl_tool/glVertexObjects.h"

#include <GLFW/glfw3.h>
#include <glad/glad.h>

#include <cmath>
#include <iostream>
using namespace glTool;
// 线框模式
#define POLYGON_MODE 0

void framebuffer_size_callback(GLFWwindow *window, int width, int height);
void processInput(GLFWwindow *window);

// 窗口大小
unsigned int SCR_WIDTH = 1600;
unsigned int SCR_HEIGHT = 900;

//
float cameraX = 8, cameraY = 5, cameraZ = 2;
CameraEX cam(glm::vec3(cameraX, cameraY, cameraZ), glm::vec3(0, 0, 0),
			 glm::vec3(0, 1, 0), 40, (float)SCR_WIDTH / SCR_HEIGHT, 0.1,
			 100000);

void draw(GLFWwindow *window) {
	glEnable(GL_DEPTH_TEST);

	// 编译着色器
	Shader shader0("shader/0-light_material/vertex.glsl",
				   "shader/0-light_material/fragment.glsl",
				   "shader/0-light_material/geometry.glsl");
	Shader shader1(
		"shader/texure2_normal3-light_material/vertex.glsl",
		"shader/texure2_normal3-light_material/fragment.glsl",
		"shader/texure2_normal3-light_material/geometry.glsl");
	Shader shaderForLight("shader/color3/vertex.glsl",
						  "shader/color3/fragment.glsl");

	BallBp ballBP(2), ball2BP(30);
	Part<1> light(ballBP);
	Part<2> ball(ball2BP);
	CubeBp cubeBp;
	ball.setLocation(0, 1, 0);
	// texture
	ball.setAttribute(
		1, 2,
		[](float x, float y, float z, float *color) {
			color[0] = atan2(x, z) / 3.1416 / 2;
			color[1] = -y / 2 + 0.5;
			return;
		},
		GL_STATIC_DRAW);
	// normal
	ball.setAttribute(
		2, 3,
		[](float x, float y, float z, float *n) {
			n[0] = x;
			n[1] = y;
			n[2] = z;
			return;
		},
		GL_STATIC_DRAW);

	Texture2D texture("textures/earth.jpg");

	// Normal
	Part<0> cube(cubeBp), ball2(ballBP);
	cube.setScaling(4, 1, 4);
	cube.setLocation(0, -1, 0);
	ball2.setScaling(0.5);
	ball2.setLocation(2, 0.5, -3);

	light.setAttribute(
		1, 3,
		[](float x, float y, float z, float *color) {
			color[0] = 1;
			color[1] = 1;
			color[2] = 1;
		},
		GL_STATIC_DRAW);
	light.setLocation(2, 1.5, -1.5);
	light.setScaling(0.1);

// 线框模式
#if POLYGON_MODE
	glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
#endif

	controlFPS(90);

	while (!glfwWindowShouldClose(window)) {
		showFPS();
		cam.setperspective((float)SCR_WIDTH / SCR_HEIGHT, 0.1f, 100000.0f);
		ball2.setRotation(0, 1, 0, 90 * glfwGetTime());
		ball.setRotation(0, 1, 0, -90 * glfwGetTime());

		glClearColor(0, 0, 0, 0);
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

		shaderForLight.use();
		shaderForLight.setMat4("camera", cam.getMat());
		light.draw(shaderForLight.ID, "trans");

		shader0.use();
		shader0.setMat4("camera", cam.getMat());
		shader0.setVec3("viewPos", cam.loc);
		shader0.setVec3("light.pos", 2, 1.5, -1.5);
		shader1.setVec3("material.ambient", 0,0,0);
		shader1.setVec3("material.diffuse", 0.2, 0.5, 0.5);
		shader1.setVec3("material.specular", 0.7,0.7,0.7);
		shader1.setFloat("material.shininess", 0.25);
		ball2.draw(shader0.ID, "trans");
		shader1.setVec3("material.ambient", 0,0,0);
		shader1.setVec3("material.diffuse", 0.5, 0.5, 0.5);
		shader1.setVec3("material.specular", 1,1,1);
		shader1.setFloat("material.shininess", 4);
		cube.draw(shader0.ID, "trans");

		shader1.use();
		shader1.setMat4("camera", cam.getMat());
		shader1.setVec3("viewPos", cam.loc);
		shader1.setVec3("light.pos", 2, 1.5, -1.5);

		shader1.setVec3("material.ambient", 0.05, 0.05, 0.05);
		shader1.setVec3("material.diffuse", 1.5, 1.5, 1.5);
		shader1.setVec3("material.specular", 2, 2, 2);
		shader1.setFloat("material.shininess", 0.7);
		texture.use();
		ball.draw(shader1.ID, "trans");
		// 画缓冲的图
		// -------------------------------------------------------------------------------
		controlFPS();
		glfwSwapBuffers(window);
		// 捕获事件
		processInput(window);
		glfwPollEvents();
		// break;
	}
	return;
}
int main() {
	// 初始化
	GLFWwindow *window =
		glfwGladInitCreateWindow(SCR_WIDTH, SCR_HEIGHT, "Hello openGL");
	if (window == NULL) {
		std::cout << "Failed to create GLFW window" << std::endl;
		return -1;
	}
	glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);
	draw(window);
	glfwTerminate();
	return 0;
}
void framebuffer_size_callback(GLFWwindow *window, int width, int height) {
	SCR_WIDTH = width;
	SCR_HEIGHT = height;
	glViewport(0, 0, width, height);
}
void processInput(GLFWwindow *window) {
	float cameraSpeed = 0.1f;
	if (glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS) {
		cam.forword(cameraSpeed);
	}
	if (glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS) {
		cam.forword(-cameraSpeed);
	}
	if (glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS) {
		cam.right(-cameraSpeed);
	}
	if (glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS) {
		cam.right(cameraSpeed);
	}
	if (glfwGetKey(window, GLFW_KEY_LEFT_SHIFT) == GLFW_PRESS) {
		cam.high(cameraSpeed);
	}
	if (glfwGetKey(window, GLFW_KEY_LEFT_CONTROL) == GLFW_PRESS) {
		cam.high(-cameraSpeed);
	}
	if (glfwGetKey(window, GLFW_KEY_I) == GLFW_PRESS) {
		cam.viewHigh(10 * cameraSpeed);
	}
	if (glfwGetKey(window, GLFW_KEY_K) == GLFW_PRESS) {
		cam.viewHigh(-10 * cameraSpeed);
	}
	if (glfwGetKey(window, GLFW_KEY_J) == GLFW_PRESS) {
		cam.viewRight(-10 * cameraSpeed);
	}
	if (glfwGetKey(window, GLFW_KEY_L) == GLFW_PRESS) {
		cam.viewRight(10 * cameraSpeed);
	}
	if (glfwGetKey(window, GLFW_KEY_U) == GLFW_PRESS) {
		cam.viewClock(-10 * cameraSpeed);
	}
	if (glfwGetKey(window, GLFW_KEY_O) == GLFW_PRESS) {
		cam.viewClock(10 * cameraSpeed);
	}
	if (glfwGetKey(window, GLFW_KEY_H) == GLFW_PRESS) {
		cam.viewForward(-10 * cameraSpeed);
	}
	if (glfwGetKey(window, GLFW_KEY_N) == GLFW_PRESS) {
		cam.viewForward(10 * cameraSpeed);
	}
}
