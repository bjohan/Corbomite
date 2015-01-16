//macros for backward compability, should be in compat/depreached.h but for
//they are not in my system.
#ifndef __BACKWARDS_H
#define __BACKWARDS_H
///sets bit number n in a
#define sbi(a, n) ((a) |= (1 << (n)))
//clears bit number n in a
#define cbi(a, n) ((a) &= ~(1 << (n)))
#endif
