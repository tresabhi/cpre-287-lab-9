#!/bin/bash

# Attempts to open a PuTTY serial connection to ALL COM ports.
# Seems to always be one irrelevant COM port on Windows machines.

PUTTY_PATH="/c/Program Files/ExtraPuTTY/Bin/putty.exe"
if [ -f "$PUTTY_PATH" ]; then
	echo "Using ExtraPuTTY at $PUTTY_PATH"
else
	PUTTY_PATH="/c/Program Files/PuTTY/putty.exe"
	echo "Using PuTTY at $PUTTY_PATH"
fi

for tty in `ls -1 /dev/ttyS*`; do
	TTY_NUM=${tty#/dev/ttyS}
	if [ "$TTY_NUM" -eq "$TTY_NUM" ]; then
		COM_NUM=`expr $TTY_NUM + 1`
		"$PUTTY_PATH" -serial COM$COM_NUM -sercfg 115200 &
	fi
done