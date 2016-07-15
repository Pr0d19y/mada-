#!/bin/bash

echo "adding directories to PYTHONPATH"
export PYTHONPATH=${PYTHONPATH}:..
echo $PYTHONPATH
echo "running tree_player.py"
python tree_player_dbus.py
