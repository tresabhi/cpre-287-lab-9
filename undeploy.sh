#!/bin/bash

USAGE_ERROR="Usage error. Correct usage: ./undeploy.sh <path>\n"
USAGE_ERROR="${USAGE_ERROR}<path> should be the path to the mounted USB drive of the node\n"
USAGE_ERROR="${USAGE_ERROR}\te.g. '/d' for D: on Windows\n"

# Do some basic argument checking
if [ $# -ne 1 ]; then
	printf "%b" "$USAGE_ERROR"
	exit 0
fi

# Confirm
echo -n "This will delete all .py files in $1 - are you sure? (y/n) "
read input
if [ -z "${input}" ]; then
	exit 0
fi

if [ "${input}" != "y" ]; then
	exit 0
fi

# Remove all .py files in the given directory
rm --verbose $1/*.py

echo "Done!"
