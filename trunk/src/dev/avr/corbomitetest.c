#include "corbomite.h"


void testButton();
void testSeekbar(int16_t v);
void testTextBox(char *newtext);
CorbomiteWidget *widgets = {
	{LABEL, "l1", { .label = {"label"}}},
	{BUTTON, "b1", {.button = {testButton, "Button"}}},
	{PROGRESSBAR, "pb1", {.progressbar = {0, 256, 256}}},
	{SEEKBAR, "pb1", {.seekbar = {testSeekbar, 0, 256, 256}}},
	{TEXT_BOX, "tb1", {.textBox = {testTextBpx, "Type words here", 4}}}
}
