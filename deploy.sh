#!/bin/bash

USAGE_ERROR="Usage error. Correct usage: ./deploy.sh <node_type> <zone_id> <path>\n"
USAGE_ERROR="${USAGE_ERROR}<node_type> should be:\n"
USAGE_ERROR="${USAGE_ERROR}\t0 for a simulated system\n"
USAGE_ERROR="${USAGE_ERROR}\t1 for the primary control node\n"
USAGE_ERROR="${USAGE_ERROR}\t2 for the secondary control node\n"
USAGE_ERROR="${USAGE_ERROR}\t3 for a temperature measurement node\n"
USAGE_ERROR="${USAGE_ERROR}<zone_id> should be the zone where the node is located (1-3), applicable for temperature measurement nodes\n"
USAGE_ERROR="${USAGE_ERROR}<path> should be the path to the mounted USB drive of the node\n"
USAGE_ERROR="${USAGE_ERROR}\te.g. '/d' for D: on Windows\n"

# Do some basic argument checking
if [ $# -ne 3 ] || ! [ "$1" -eq "$1" ] 2>/dev/null || [ "$1" -lt 0 ] || [ "$1" -gt 3 ]; then
	printf "%b" "$USAGE_ERROR"
	exit 0
fi

# Copy all .py files in this directory to the given destination
echo "Copying files into place..."
cp --verbose *.py $3/

# Update the node type, stored in node_config.py
echo "Configuring node_config.py..."
sed -i "s/node_type = ./node_type = $1/g" $3/node_config.py

# If this is a temp measurement node, update the zone_id
if [ $1 -eq 3 ]; then
	ZONE=`expr $2 - 1`
	echo $ZONE
	sed -i "s/zone_id = ./zone_id = $ZONE/g" $3/node_config.py
fi

echo "Done!"
