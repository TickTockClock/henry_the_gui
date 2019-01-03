#!/usr/bin/python3

'''
This application uses the PyQt5 framework to build a 
graphical user interface and runs on python3.6 or later.
Also the subprocess and signal module are being used
to execute bash commands.

The MainWindow class inherits from QWidget.

The init_gui() initializes the GUI by:
    * Using a QWidget Stylesheet (see below).
    * Setting up the Frame.
    * Moving the Window to the center (see below).
    * Creating and adjusting the widgets (see below).
    * And Building them all.
'''

import sys
import os
import signal
import subprocess as sp
import json

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDesktopWidget
from PyQt5.QtWidgets import QToolTip, QHBoxLayout, QVBoxLayout, QGridLayout, QBoxLayout
from PyQt5.QtGui import QFont, QIcon

functionalities = 'functionality.txt'
stylesheet = 'stylesheet.css'

#     Read from files. If _eval for dict
def read_file_return(file, _eval=False):
    with open(file, 'r') as stream:
        if _eval:
            return eval(stream.read())
        return stream.read()

#     
def build_gui():
    
    application = QApplication(sys.argv)
    MainWindow()
    application.exec_()


class MainWindow(QWidget):


#     CONSTRUCTOR inherits from QWidget
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.FX = read_file_return(functionalities, _eval=True)
        self.CSS = read_file_return(stylesheet)
        
        self.quit_btn = None
        self.stop_btn = None
        
        self.running_processes = {}
        self.programs = {}
        
        for i in range(self.FX['HOWMANYPROGRAMS']):
            self.running_processes[f'process{i}'] = None
            self.programs[f'program{i}'] = None
        
        print(f'''
        Hello there Friend.
        
        Welcome to your Henry Volksbot Application...
        
        Below you can see your Functionalities:

        {json.dumps(self.FX, indent=6)}
        
        ''')
        
        self.init_gui()

#     INITIALIZE GUI
    def init_gui(self):
    
#     pyqt gui general settings
        self.resize(1000, 600,) # width, hight
        self.move(0, 0) # x, y
        self.setWindowTitle('Henry The Linux App')
        self.setWindowIcon(QIcon('hwr-logo.png'))
        QToolTip.setFont(QFont('SansSerif', 15))
        self.setToolTip(self.FX['GENERALTOOLTIP'])
        self.setStyleSheet(self.CSS)

#     class methods
        # self.window_to_center()
        self.init_widgets()

#     init all
        self.show()


#     ALL WIDGETS >> BUTTONS
    def init_widgets(self):

#     check HOWMANYPROGRAMS to create as QPushButtons
        for i in range(self.FX['HOWMANYPROGRAMS']):
            try:
                com = self.FX['COMMANDS'][i]
                prog = self.FX['PROGRAMNAMES'][i]
                tool = self.FX['TOOLTIPS'][i]
            except:
                com = None
                prog = f'Program{i}'
                tool = f'Tooltip{i}'

            self.programs[f'program{i}'] = self.create_button(
                btn_label=prog,
                tooltip=tool,
                command=com,
                process=i,
                action=self.start_bash_process)

        self.quit_btn = self.create_button(
            btn_label='Quit',
            tooltip='Quit the Application. Program will be shutdown before.',
            action=lambda: self.quit_gui())

        self.stop_btn = self.create_button(
            btn_label='Stop',
            tooltip='Stop your Autodrive program.',
            enabled=False,
            action=lambda: self.stop_bash_process())

        self.setLayout(self.put_into_layout(
            self.programs,
            self.quit_btn,
            self.stop_btn))

#     > CREATE NEW BUTTON
    def create_button(self, btn_label, tooltip, command=None, process=None, enabled=True, action=None):
        btn = QPushButton(btn_label, self)
        btn.setEnabled(enabled)
        btn.setToolTip(tooltip)
        if command:
            btn.clicked.connect(lambda: action(command, process))
        else:
            btn.clicked.connect(action)

        return btn

#     > START
    def start_bash_process(self, command, process=None):
        print(command)
        if command:
            self.running_processes[f'process{process}'] = sp.Popen(
            'gnome-terminal --disable-factory -e "%s"' % command, shell=True, preexec_fn=os.setpgrp)
        
            print(f'''Process: 
            {self.running_processes[f'process{process}'].__class__}
            {command} STARTED''')
         
            self.programs[f'program{process}'].setEnabled(False)
            self.stop_btn.setEnabled(True)
            return
            
        print('New Unused Button.')
        
#      > QUIT
    def quit_gui(self):
        for i in range(len(self.running_processes)):
            if self.running_processes[f'process{i}']:
                os.killpg(self.running_processes[f'process{i}'].pid, signal.SIGINT)
                print(f'''Process: 
                {self.running_processes[f'process{i}']}
                {self.FX['COMMANDS'][i]} KILLED''')
        
        print(f'See you next time Friend!')
        QApplication.instance().quit()

#     > STOP
    def stop_bash_process(self):
    
        for i in range(len(self.running_processes)):
            if not self.running_processes[f'process{i}'] == None:
                os.killpg(self.running_processes[f'process{i}'].pid, signal.SIGINT)
                print(f'''Process: {self.running_processes[f'process{i}']}
                {self.FX['COMMANDS'][i]} KILLED''')
                self.running_processes[f'process{i}'] = None
                self.programs[f'program{i}'].setEnabled(True)
                self.stop_btn.setEnabled(False)
                self.resize(1000, 600,)
                self.move(0, 0)


#     << LAYOUTS
    def put_into_layout(self, programs, qbtn, sbtn):
        layout = QBoxLayout(2) # TopToBottom
        upper = QBoxLayout(2)
        lower = QBoxLayout(0) # LeftToRight
        upperboxes = {}

#     calculation of boxlayout
        for i in range(self.FX['HOWMANYPROGRAMS']):
            columns = self.FX['COLUMNS']
            if i%columns == 0:
                upperboxes[f'box{i}'] = QBoxLayout(0)
                for j in range(columns):
                    try:
                        upperboxes[f'box{i}'].addWidget(programs[f'program{j+i}'])
                    except:
                        continue
                upper.addLayout(upperboxes[f'box{i}'])

        lower.addWidget(qbtn)
        lower.addWidget(sbtn)
        layout.addLayout(upper)
        layout.addLayout(lower)

        return layout

#     << CENTER WINDOW
    def window_to_center(self):
        geo = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        geo.moveCenter(center)
        self.move(geo.topLeft())



#       Run the script
if __name__ == '__main__':
    build_gui()
