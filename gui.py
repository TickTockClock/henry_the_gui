#!/usr/bin/python3

'''
This application uses the PyQt5 framework to build a 
graphical user interface and runs on python3.5 or later.
Also the subprocess and signal module are being used
to execute bash commands.

The MainWindow class inherits from QWidget.

'''

import sys
import os
import signal
import subprocess as sp
import json

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDesktopWidget
from PyQt5.QtWidgets import QToolTip, QHBoxLayout, QVBoxLayout, QGridLayout, QBoxLayout
from PyQt5.QtGui import QFont, QIcon

FUNCTIONALITIES = 'functionality.txt'
STYLESHEET = 'stylesheet.css'
WINDOW_DIM = [600, 400]

#     read from files. If _eval for dict.
def read_file_return(file, _eval=False):
    with open(file, 'r') as stream:
        if _eval:
            return eval(stream.read())
        return stream.read()

#     build the app
def build_gui():
    
    application = QApplication(sys.argv)
    MainWindow()
    application.exec_()


class MainWindow(QWidget):

#     CONSTRUCTOR inherits from QWidget
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.funcs = read_file_return(FUNCTIONALITIES, _eval=True)
        self.css = read_file_return(STYLESHEET)
        
        self.quit_btn = None
        self.stop_btn = None
        
        self.running_processes = {}
        self.programs = {}
        
        for i in range(self.funcs['HOWMANYPROGRAMS']):
            self.running_processes['process{}'.format(i)] = None
            self.programs['program{}'.format(i)] = None
        
        print('''
        Hello there Friend.
        
        Welcome to your Henry Volksbot Application...
        
        Below you can see your Functionalities:

        {}
        
        '''.format(json.dumps(self.funcs, indent=6)))
        
        self.init_gui()

#     INITIALIZE GUI
    def init_gui(self):
#     pyqt gui general settings
        self.resize(WINDOW_DIM[0], WINDOW_DIM[1]) # width, hight
        self.move(0, 0) # x, y
        self.setWindowTitle('Henry The Linux App')
        self.setWindowIcon(QIcon('hwr-logo.png'))
        QToolTip.setFont(QFont('SansSerif', 15))
        self.setToolTip(self.funcs['GENERALTOOLTIP'])
        self.setStyleSheet(self.css)

#     class methods
        # self.window_to_center()
        self.init_widgets()

#     init all
        self.show()

#     ALL WIDGETS >> BUTTONS
    def init_widgets(self):

#     check HOWMANYPROGRAMS to create as QPushButtons
        for i in range(self.funcs['HOWMANYPROGRAMS']):
            try:
                com = self.funcs['COMMANDS'][i]
                prog = self.funcs['PROGRAMNAMES'][i]
                tool = self.funcs['TOOLTIPS'][i]
            except:
                com = None
                prog = 'Program{}'.format(i)
                tool = 'Tooltip{}'.format(i)

            self.programs['program{}'.format(i)] = self.create_button(
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
            self.running_processes['process{}'.format(process)] = sp.Popen(
            'xfce4-terminal --hold --disable-server ' +
            '--geometry 0x10+10+10 -e "%s" 2>/dev/null' 
            % command, shell=True, preexec_fn=os.setpgrp
            )
        
            print('''Process: 
            {}
            {} STARTED'''.format(
            self.running_processes['process{}'.format(process)].__class__,
            command))
         
            self.programs['program{}'.format(process)].setEnabled(False)
            self.stop_btn.setEnabled(True)
            return
            
        print('New Unused Button.')
        
#      > QUIT
    def quit_gui(self):
        for i in range(len(self.running_processes)):
            if self.running_processes['process{}'.format(i)]:
                os.killpg(self.running_processes['process{}'.format(i)].pid, signal.SIGINT)
                print('''Process: 
                {}
                {} KILLED'''.format(
                self.running_processes['process{}'.format(i)],
                self.funcs['COMMANDS'][i]))
        
        print('See you next time Friend!')
        QApplication.instance().quit()

#     > STOP
    def stop_bash_process(self):
    
        for i in range(len(self.running_processes)):
            if not self.running_processes['process{}'.format(i)] == None:
                os.killpg(self.running_processes['process{}'.format(i)].pid, signal.SIGINT)
                print('''
                Process: 
                {}
                {} KILLED'''.format(
                self.running_processes['process{}'.format(i)],
                self.funcs['COMMANDS'][i]))
                
                self.running_processes['process{}'.format(i)] = None
                self.programs['program{}'.format(i)].setEnabled(True)
                self.stop_btn.setEnabled(False)
                self.resize(WINDOW_DIM[0], WINDOW_DIM[1])
                self.move(0, 0)

#     << LAYOUTS
    def put_into_layout(self, programs, qbtn, sbtn):
        layout = QBoxLayout(2) # TopToBottom
        upper = QBoxLayout(2)
        lower = QBoxLayout(0) # LeftToRight
        upperboxes = {}

#     calculation of boxlayout
        for i in range(self.funcs['HOWMANYPROGRAMS']):
            columns = self.funcs['COLUMNS']
            if i%columns == 0:
                upperboxes['box{}'.format(i)] = QBoxLayout(0)
                for j in range(columns):
                    try:
                        upperboxes['box{}'.format(i)].addWidget(programs['program{}'.format(j+i)])
                    except:
                        continue
                upper.addLayout(upperboxes['box{}'.format(i)])

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
