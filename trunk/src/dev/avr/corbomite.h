#include <stdlib.h>
#include <string.h>
#include <avr/io.h>

extern const char internalName[9];
extern const char internalId[2];
typedef const enum {
	LABEL,
	BUTTON,
	NEWLINE,
	PROGRESSBAR,
	SEEKBAR,
	TEXTBOX,
	LASTTYPE,
} CorbomiteType;

typedef struct{
	const char *text;
} CorbomiteLabel;

typedef void (*const ButtonCallback)();
typedef struct{
	ButtonCallback callback;
	const char *text;
} CorbomiteButton;

typedef struct{
	const int16_t max;
	const int16_t current;
}CorbomiteProgressbar;

typedef void (* const SeekbarCallback)(int16_t);

typedef struct{
	SeekbarCallback callback;
	const int16_t max;
	const int16_t current;
} CorbomiteSeekbar;

typedef void (* const TextBoxCallback)(char *);
typedef struct{
	TextBoxCallback callback;
	const char *initialText;
	const uint16_t lines;
}CorbomiteTextbox;

typedef union{
	const CorbomiteLabel label;
	const CorbomiteButton button;
	const CorbomiteProgressbar progressbar;
	const CorbomiteSeekbar seekbar;
	const CorbomiteTextbox textbox;
} CorbomiteData;

typedef struct{
	const CorbomiteType t;
	const uint8_t weight;
	const char *id;
	const CorbomiteData d;
} CorbomiteWidget;

void registeredWidgets();
extern const CorbomiteWidget widgets[];
