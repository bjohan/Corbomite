#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/eeprom.h>
#include <string.h>
#include <stdlib.h>
#include <avr/pgmspace.h>
#include "uart_command_lib.h"
#include "corbomite.h"
uint32_t count = 0;
uint32_t count2 = 0;
void testButton(){
	transmitStringP(PSTR("Btn dutton pressed!!!!\r\n"));
	transmitStringP(PSTR("l1 button pressed "));
	transmitInt(count++);
	transmitStringP(PSTR(" times"));
	transmitStringP(PSTR("\r\n"));
	transmitStringP(PSTR("tb1 set"));
	transmitStringP(PSTR("\r\n"));
	
}
void testButton2(){
	transmitStringP(PSTR("b2 "));
	transmitInt(count2++);
	transmitStringP(PSTR("\r\n"));
	transmitStringP(PSTR("tb2 app button"));
	transmitStringP(PSTR("\r\n"));
	transmitStringP(PSTR("tb2 apps"));
	transmitStringP(PSTR("\r\n"));
	transmitStringP(PSTR("tb2 app was pressed"));
	transmitStringP(PSTR("\r\n"));
	transmitStringP(PSTR("tb2 appnl"));
	transmitStringP(PSTR("\r\n"));
	transmitStringP(PSTR("tb2 app ##"));
	transmitStringP(PSTR("\r\n"));
}
void testSeekbar(int16_t v){
	transmitStringP(PSTR("Seekbar!!!!"));
	transmitInt(v);
	transmitStringP(PSTR("\r\n"));
	transmitStringP(PSTR("pb1 "));
	transmitInt(v);
	transmitStringP(PSTR("\r\n"));

}
void testTextBox(char *newtext){}

CorbomiteWidget widgets[] = {
	{LABEL, 1, "l1", { .label = {"Kickass button"}}},
	{BUTTON, 2, "b1", {.button = {testButton, "Button"}}},
	{NEWLINE, 1, "nl0",{.label={"lab"}}},
	{BUTTON, 1, "b2", {.button = {testButton2, "Another button"}}},
	{NEWLINE, 1, "nl1",{.label={"lab"}}},
	{PROGRESSBAR, 1, "pb1", {.progressbar = {256, 256}}},
	{NEWLINE, 1, "nl1",{.label={"lab"}}},
	{LABEL, 1, "l2", { .label = {"Servo position"}}},
	{SEEKBAR, 1, "sb", {.seekbar = {testSeekbar, 256, 256}}},
	{NEWLINE, 1, "nl1",{.label={"lab"}}},
	{TEXTBOX, 1, "tb1", {.textbox = {testTextBox, "Type words here", 4}}},
	{TEXTBOX, 1, "tb2", {.textbox = {testTextBox, "", 4}}},
	{BUTTON, 1, "i", {.button = {registeredWidgets, "internal"}}},
	{LASTTYPE, 1, ""}
};

/**new line stored in progmem*/
const char nl[] PROGMEM = "\r\n";


/** Main function for the automatically tuned loop antenna.
 * This function initializes hardware and then enters a main loop.
 * The main loop checks the command line to see if a new command has been 
 * entered. If so the command line library tries to execute the command using
 * the processor associated with the command in the #Commands array.
 * The mainloop also runs enabled background tasks. The background tasks are
 * - auto servo, enabled by the 'as' command. Continously sweeps the full range
 *   of both servos.
 * - track tune, enabled by the 'tt' command. Continously tune as the radio
 *   frequency setting is change.
 * - stream meter, enabled by the 'sm' command. Continously print the adc
 *   value of the current channel. 
*/
int main(void) 
{
CLKPR = _BV(CLKPCE);
	CLKPR = 0;
	DDRB |= _BV(0);
	PORTB = 0;
	initUsart();
	transmitString("Serial port initialized\r\n");
	while(1){
		PORTB = 0;
		commandLine();
		PORTB = 0;
	}
}
