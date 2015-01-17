#!/usr/bin/python
"""This is a signal source for test usage.
This program generates csv signals on stdout. The program tries to generate
the signal at the specified sample rate, or as quick as possible if the
specified rate is too fast.

Options:
--time-stamp    Will print the sample time in the first column.

--sample-time   Print the sample number instead of the time in seconds. This
                option does not do anything unless the --time-stamp option is
                specified.

--rate R        Sets the sample rate to R.

--sin F		Adds a sinewave with the frequency F. This option can be used
                multiple times to add many waves. The signals will in columns
                in the same order as they are specified.
"""

import sys
import time
import math
import fcntl
import os

withTimeStamp = False
sampleTime = False
sines = []
rate = 1

fd = sys.stdin.fileno()
fl = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

for n in range(len(sys.argv)):
    if sys.argv[n] == '--time-stamp':
        withTimeStamp = True
    if sys.argv[n] == '--sample-time':
        sampleTime = True
    if sys.argv[n] == '--sin':
        sines.append(float(sys.argv[n + 1]))
    if sys.argv[n] == '--rate':
        rate = float(sys.argv[n + 1])

n = 0
t0 = time.time()
while True:
    t = time.time() - t0
    s = ''
    if withTimeStamp:
        if sampleTime:
            s += str(n) + ', '
        else:
            s += str(t) + ', '
    for w in sines:
        s += str(math.sin(t * w)) + ', '
    sys.stdout.write(s[0:-2] + '\n')
    sys.stdout.flush()
    n += 1
    time.sleep(max((1 / rate - (time.time() - t - t0)), 0))
    try:
        i = sys.stdin.readline().strip()
        if (i == 'exit') or i == ('quit'):
            break
    except:
        pass
