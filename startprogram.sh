#!/bin/bash

nameofenv='test'
pythonpath=$(which python3)

# if no environment exists create a new one
if [ ! -d $nameofenv ]; then

	echo creating virtual environment and installing PyQt5

	virtualenv -p $pythonpath $nameofenv

	source $nameofenv/bin/activate

	pip install -r requirements.txt

fi

## activate your python enviornment
source $nameofenv/bin/activate

## run the app
python ./gui.py
