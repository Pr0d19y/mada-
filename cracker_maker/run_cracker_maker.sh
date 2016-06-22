#!/bin/bash

echo "adding directories to PYTHONPATH"
export PYTHONPATH=${PYTHONPATH}:..
echo $PYTHONPATH
echo "running cracker_maker.py"
sudo python cracker_maker.py