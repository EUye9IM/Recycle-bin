#include "application.h"
#include "imgui/imgui.h"

// Our state
bool isMainOn = true;

void show_main() {
	// Create a window called
	ImGui::Begin("helloworld", &isMainOn,
				 ImGuiWindowFlags_NoResize | ImGuiWindowFlags_NoCollapse);
	static bool isDemoOn=false;
	if(ImGui::Button("demo"))
		isDemoOn=true;
				 
	ImGui::TextUnformatted("Hello world!");
	ImGui::End();
	if(isDemoOn)
		ImGui::ShowDemoWindow(&isDemoOn);
}
void callback_close(){};
int main_init(const int &argc, char **const &argv) { return 0; }
int main_loop(const int &argc, char **const &argv) {
	if (isMainOn)
		show_main();
	else
		callback_close();

	return !isMainOn;
}
