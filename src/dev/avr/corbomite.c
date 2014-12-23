#include <avr/pgmspace.h>
#include "corbomite.h"
#include "uart_command_lib.h"
uint8_t countTokens(char *str, char *tokenizers, 
			uint8_t toknum, uint8_t *start, uint8_t *stop);
uint8_t tokenToString(char *tokenLine, char *tokenizers, uint8_t n, 
			char *strDest, uint8_t destLength);

const char labelCmd[] PROGMEM = "label ";
const char buttonCmd[] PROGMEM = "button ";
const char newlineCmd[] PROGMEM = "newline ";
const char progressbarCmd[] PROGMEM = "progressbar ";
const char seekbarCmd[] PROGMEM = "seekbar ";
const char textboxCmd[] PROGMEM = "textbox ";
const char internalName[] PROGMEM = "internal";
const char internalId[] PROGMEM = "i";
const char *typeNames[] = {labelCmd, buttonCmd, newlineCmd, progressbarCmd, 
				seekbarCmd, textboxCmd};
const char sp[] PROGMEM = " ";

void reportLabelData(const CorbomiteLabel *l)
{
	transmitStringP(l->text);
}

void reportButtonData(const CorbomiteButton *b)
{
	transmitStringP(b->text);
}

void reportProgressbarData(const CorbomiteProgressbar *p)
{
	transmitInt(p->max);transmitStringP(sp);
	transmitInt(p->current);transmitStringP(sp);
}

void reportSeekbarData(const CorbomiteSeekbar *s)
{
	transmitInt(s->max);transmitStringP(sp);
	transmitInt(s->current);transmitStringP(sp);
}

void reportTextboxData( const CorbomiteTextbox *t)
{
	transmitInt(t->lines);transmitStringP(sp);
	transmitStringP(t->initialText);
}

void reportWidget(const CorbomiteWidget *w)
{
	if(w->t < LASTTYPE){
		transmitStringP(typeNames[w->t]);
		transmitStringP(w->id);
		transmitStringP(sp);
		transmitInt((uint32_t) w->weight);
		transmitStringP(sp);
		switch(w->t){
			case LABEL:
				reportLabelData(&w->d.label);
				break;
			case BUTTON:
				reportButtonData(&w->d.button);
				break;
			case PROGRESSBAR:
				reportProgressbarData(&w->d.progressbar);
				break;
			case SEEKBAR:
				reportSeekbarData(&w->d.seekbar);
				break;
			case TEXTBOX:
				reportTextboxData(&w->d.textbox);
				break;
			default:
				break;
		}
	}
	transmitStringP(PSTR("\r\n"));
}

void pgm_copy(void const * src, uint8_t *dst, uint8_t len)
{
	while(len--)
		*(uint8_t *)(dst++) = pgm_read_byte(src++);
}
void registeredWidgets()
{
	CorbomiteWidget w;
	uint8_t n = 0;
	pgm_copy(&widgets[0], (uint8_t *)&w, sizeof(w));
	while(w.t != LASTTYPE){
		reportWidget(&w);
		n++;
		pgm_copy(&widgets[n], (uint8_t *)&w, sizeof(w));
	}
}
void processCorbomiteCall(const CorbomiteWidget *w, char *l)
{
	if(w->t < LASTTYPE){
		switch(w->t){
			case LABEL:
				transmitStringP(PSTR("Label has no event"));
				break;
			case BUTTON:
				(w->d.button.callback)();
				break;
			case PROGRESSBAR:
				transmitStringP(PSTR("Progressbar has no event"));
				break;
			case SEEKBAR:
				(w->d.seekbar.callback)((int16_t)getIntParameter(l,2));
				break;
			case TEXTBOX:
				transmitStringP(PSTR("TODO ;D"));
				break;
			default:
				break;
		}
	}
	transmitStringP(PSTR("\r\n"));
	
}

void corbomiteParse(char * line)
{
	CorbomiteWidget w;
	uint8_t ntok, l,i;
	static char token[16];
	ntok=countTokens(line, " \r\n\t", 0, NULL, NULL);
	if(ntok > 0){
		l=tokenToString(line, " \r\n\t", 1, token, 16);
		if(l > 0){
			i=0;
			pgm_copy(&(widgets[0]), (uint8_t *)&w, sizeof(w));
			while(w.t != LASTTYPE){
				i++;
				if(strcmp_pn(w.id, token)==0){
					PORTB = 1;
					processCorbomiteCall(&w, line);
					PORTB = 0;
					return;
				}
				pgm_copy(&widgets[i], (uint8_t *)&w, sizeof(w));
			}
			transmitStringP(PSTR("ERROR: Command not found\r\n"));
		}
        }

}
