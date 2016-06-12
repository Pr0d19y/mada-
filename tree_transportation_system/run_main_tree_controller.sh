#!/bin/bash

echo "adding directories to PYTHONPATH"
export PYTHONPATH=${PYTHONPATH}:..
echo $PYTHONPATH
echo "starting pigpiod"
sudo pigpiod
echo "running main_tree_controller.py"
sudo python main_tree_controller.py