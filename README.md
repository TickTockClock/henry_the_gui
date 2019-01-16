
# Henry the GUI Application

## This branch works only with Python3.5 or later and is designed for the Raspberry Pi!

This is the GUI application.

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

