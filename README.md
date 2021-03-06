
# Henry the GUI Application

## This branch works only with Python3.6 or later and is designed for Ubuntu 16!
This is the desktop application.

Clone this branch by running:
```bash
git clone git@github.com:TickTockClock/henry_the_gui.git
```

The script will create a virtual environment and install the required modules before executing `gui.py`.

Open the `startprogram.sh` to rename the environment  `nameofenv` or specify the `pythonpath`if needed.

### Run the app
The program can be executed by running:
```bash
source startprogram.sh
# or
. startporgram.sh
```
or by simply double clicking it.

`startprogram.sh` should be set up as an executable Shell script, so you can double click it to run it. If that is not the case then please check out [this article](https://askubuntu.com/questions/138908/how-to-execute-a-script-just-by-double-clicking-like-exe-files-in-windows#answer-305776) on how to enable this feature.

## functionalities
In the `functionalities.txt` you can edit the following parameters: 
* HOWMANYPROGRAMS
	* Determine how many buttons you want to apply.
* COLUMNS
	* Determine how the buttons are divided into columns.
* PROGRAMNAMES
	* Name your buttons from top left to bottom right.
* TOOLTIPS
	* Create your tooltips from top left to bottom right.
* COMMANDS
	* Insert your bash commands from top left to bottom right.
* GENERALTOOLTIP
	* Appears when hovering over the application.

*Note this is supposed to be a python dictionary so be aware of the syntax.*

## stylesheet
Here you can style the application with simple `css`. Use the `PyQt` classes for reference.

