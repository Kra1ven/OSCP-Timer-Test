from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys
import time
import datetime
import threading

Running = True

Finished = [0, 0]
CurrentMachine = 0
Switch = False
ExamTime = 85500
Timer = False
ExamTimer = False

# m0 = {"name":"Cronos", "time":0, "user":"", "root":"", "points":10}
# m1= {"name":"Active", "time":0, "user":"", "root":"", "points":20}
# m2= {"name":"Beep", "time":0, "user":"", "root":"", "points":20}
# m3= {"name":"Jeeves", "time":0, "user":"", "root":"", "points":25}
# m4= {"name":"BoF 8", "time":0, "user":"", "root":"", "points":25}

data = [
{"name":"Cronos", "time":0, "user":"", "root":"", "points":10},
{"name":"Active", "time":0, "user":"", "root":"", "points":20},
{"name":"Beep", "time":0, "user":"", "root":"", "points":20},
{"name":"Jeeves", "time":0, "user":"", "root":"", "points":25},
{"name":"BoF 8", "time":0, "user":"", "root":"", "points":25}
]

machines = [
"Poison - 10 points",
"Friendzone - 20 points",
"jerry - 20 points",
"Devops - 25 points",
"BoF 8 - 25 points"]

def DetailReport():
	report = []
	for i in data:
		tmp = ""
		tmp += "Name of the box: " + i["name"] + "\n"
		tmp += "Time spent: " + str(datetime.timedelta(seconds=i["time"])) + "\n"
		tmp += "User: " + i["user"] + "\n"
		tmp += "Root: " + i["root"] + "\n"
		tmp += "Total points for the machine: " + str(i["points"]) + "\n"
		report.append(tmp)
	return "\n".join(report)

def FinishedMsg(arg=0):
	msg = QMessageBox()
	msg.setIcon(QMessageBox.Information)
	msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
	msg.setInformativeText("By pressing OK, you will continue\nPressing Cancel will do a full reset\n\nTo see a detailed report of the machines, press Show Detailes")
	msg.setWindowTitle("Points alert")
	msg.setDetailedText(DetailReport())
	if arg == 70:
		msg.setText("You got enough points for the exam")
	if arg == 100:
		msg.setText("Wow, you aced it. Maximum points earned")
	retval = msg.exec_()

	#1024 ok
	#4194304 cancel

def Closing():
	global Running
	Running = False
	quit()

def CurrentState():
	global Switch
	global CurrentMachine
	x = ui.comboBox.currentIndex()
	if x != CurrentMachine:
		Switch = True
		ui.Root_input.setText(str(data[x]["root"]))
		ui.User_input.setText(str(data[x]["user"]))
	CurrentMachine = x
	points = 0
	users = 0
	roots = 0
	for i in data:
		if i["root"] != "":
			points += i["points"]
			roots += 1
			users += 1
		elif i["user"] != "":
			if i["points"] == 10:
				points += 5
			else:
				points += 10
			users += 1

	if Finished[1] == 0:
		if points == 100:
			FinishedMsg(100)
			Finished[1] = 1
	if Finished[0] == 0:
		if points >= 70:
			FinishedMsg(70)
			Finished[0] = 1

	ui.Points.setText(str(points))
	ui.Roots.setText(str(roots))
	ui.Users.setText(str(users))
	ui.Time_left.setText(str(datetime.timedelta(seconds=ExamTime)))
	ui.Timer.setText(str(datetime.timedelta(seconds=data[CurrentMachine]["time"])))

def ExamCounter():
	global ExamTime
	while Running:
		if ExamTimer == False:
			break
		ExamTime -= 1
		time.sleep(1)

def MachineCounter(machine):
	global data
	global Timer
	global Switch
	while Running:
		if Switch:
			Switch = False
			break
		data[machine]["time"] = data[machine]["time"] + 1
		time.sleep(1)
	Timer = False

def LocalReset(machine):
	global Switch
	ui.Root_input.setText("")
	ui.User_input.setText("")
	Switch = True
	time.sleep(1)

	data[machine]["user"] = ""
	data[machine]["root"] = ""
	data[machine]["time"] = 0

def FullReset():
	global ExamTimer
	global data
	global ExamTime
	global Timer
	global Switch
	global CurrentMachine

	ui.Root_input.setText("")
	ui.User_input.setText("")

	Switch = True
	time.sleep(1)

	for i in data:
		i["user"] = ""
		i["root"] = ""
		i["time"] = 0

	CurrentMachine = 0
	ExamTimer = False
	time.sleep(1)

	ExamTime = 85500
	Timer = False

def Handler(arg):
	global data
	global Timer
	global Switch
	global ExamTimer
	if arg == "Submit_user":
		data[CurrentMachine]["user"] = str(ui.User_input.text())
	if arg == "Submit_root":
		data[CurrentMachine]["root"] = str(ui.Root_input.text())
	if arg == "Start_timer":
		if not Timer:
			Timer = True
			x = threading.Thread(target=MachineCounter, args=(CurrentMachine,))
			x.start()
		if not ExamTimer:
			ExamTimer = True	
			x = threading.Thread(target=ExamCounter)
			x.start()
	if arg == "Pause_timer":
		if not Timer:
			return
		Switch = True
	if arg == "Reset":
		x = threading.Thread(target=LocalReset, args=(CurrentMachine,))
		x.start()
	if arg == "Full_reset":
		x = threading.Thread(target=FullReset)
		x.start()

class Ui_MainWindow(object):
	def __init__(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(431, 295)
		MainWindow.setMinimumSize(QtCore.QSize(431, 295))
		MainWindow.setMaximumSize(QtCore.QSize(431, 295))
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.comboBox = QtWidgets.QComboBox(self.centralwidget)
		self.comboBox.setGeometry(QtCore.QRect(10, 10, 321, 31))
		self.comboBox.addItems(machines)
		font = QtGui.QFont()
		font.setPointSize(12)
		self.comboBox.setFont(font)
		self.comboBox.setObjectName("comboBox")
		self.label = QtWidgets.QLabel(self.centralwidget)
		self.label.setGeometry(QtCore.QRect(10, 130, 81, 31))
		font = QtGui.QFont()
		font.setFamily("Segoe UI Historic")
		font.setPointSize(12)
		self.label.setFont(font)
		self.label.setObjectName("label")
		self.Timer = QtWidgets.QLabel(self.centralwidget)
		self.Timer.setGeometry(QtCore.QRect(60, 130, 81, 31))
		font = QtGui.QFont()
		font.setFamily("Segoe UI Historic")
		font.setPointSize(12)
		self.Timer.setFont(font)
		self.Timer.setObjectName("Timer")
		self.label_3 = QtWidgets.QLabel(self.centralwidget)
		self.label_3.setGeometry(QtCore.QRect(10, 90, 81, 31))
		font = QtGui.QFont()
		font.setFamily("Segoe UI Historic")
		font.setPointSize(12)
		self.label_3.setFont(font)
		self.label_3.setObjectName("label_3")
		self.label_4 = QtWidgets.QLabel(self.centralwidget)
		self.label_4.setGeometry(QtCore.QRect(10, 50, 81, 31))
		font = QtGui.QFont()
		font.setFamily("Segoe UI Historic")
		font.setPointSize(12)
		self.label_4.setFont(font)
		self.label_4.setObjectName("label_4")
		self.Pause_timer = QtWidgets.QPushButton(self.centralwidget)
		self.Pause_timer.setGeometry(QtCore.QRect(70, 160, 51, 31))
		self.Pause_timer.clicked.connect(lambda: Handler("Pause_timer"))
		font = QtGui.QFont()
		font.setPointSize(11)
		self.Pause_timer.setFont(font)
		self.Pause_timer.setObjectName("Pause_timer")
		self.Start_timer = QtWidgets.QPushButton(self.centralwidget)
		self.Start_timer.setGeometry(QtCore.QRect(10, 160, 51, 31))
		self.Start_timer.clicked.connect(lambda: Handler("Start_timer"))
		font = QtGui.QFont()
		font.setPointSize(11)
		self.Start_timer.setFont(font)
		self.Start_timer.setObjectName("Start_timer")
		self.User_input = QtWidgets.QLineEdit(self.centralwidget)
		self.User_input.setGeometry(QtCore.QRect(50, 60, 211, 16))
		self.User_input.setObjectName("User_input")
		self.Root_input = QtWidgets.QLineEdit(self.centralwidget)
		self.Root_input.setGeometry(QtCore.QRect(50, 100, 211, 16))
		self.Root_input.setObjectName("Root_input")
		self.line = QtWidgets.QFrame(self.centralwidget)
		self.line.setGeometry(QtCore.QRect(0, 186, 571, 31))
		self.line.setFrameShape(QtWidgets.QFrame.HLine)
		self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line.setObjectName("line")
		self.Full_reset = QtWidgets.QPushButton(self.centralwidget)
		self.Full_reset.setGeometry(QtCore.QRect(10, 240, 411, 31))
		self.Full_reset.clicked.connect(lambda: Handler("Full_reset"))
		font = QtGui.QFont()
		font.setPointSize(11)
		self.Full_reset.setFont(font)
		self.Full_reset.setObjectName("Full_reset")
		self.label_9 = QtWidgets.QLabel(self.centralwidget)
		self.label_9.setGeometry(QtCore.QRect(350, 80, 81, 31))
		font = QtGui.QFont()
		font.setFamily("Segoe UI Historic")
		font.setPointSize(12)
		self.label_9.setFont(font)
		self.label_9.setObjectName("label_9")
		self.Roots = QtWidgets.QLabel(self.centralwidget)
		self.Roots.setGeometry(QtCore.QRect(400, 80, 61, 31))
		font = QtGui.QFont()
		font.setFamily("Segoe UI Historic")
		font.setPointSize(12)
		self.Roots.setFont(font)
		self.Roots.setObjectName("Roots")
		self.label_11 = QtWidgets.QLabel(self.centralwidget)
		self.label_11.setGeometry(QtCore.QRect(350, 40, 81, 31))
		font = QtGui.QFont()
		font.setFamily("Segoe UI Historic")
		font.setPointSize(12)
		self.label_11.setFont(font)
		self.label_11.setObjectName("label_11")
		self.Users = QtWidgets.QLabel(self.centralwidget)
		self.Users.setGeometry(QtCore.QRect(400, 40, 61, 31))
		font = QtGui.QFont()
		font.setFamily("Segoe UI Historic")
		font.setPointSize(12)
		self.Users.setFont(font)
		self.Users.setObjectName("Users")
		self.Reset = QtWidgets.QPushButton(self.centralwidget)
		self.Reset.setGeometry(QtCore.QRect(180, 160, 151, 31))
		self.Reset.clicked.connect(lambda: Handler("Reset"))
		font = QtGui.QFont()
		font.setPointSize(11)
		self.Reset.setFont(font)
		self.Reset.setObjectName("Reset")
		self.Submit_root = QtWidgets.QPushButton(self.centralwidget)
		self.Submit_root.setGeometry(QtCore.QRect(270, 100, 61, 16))
		self.Submit_root.clicked.connect(lambda: Handler("Submit_root"))
		font = QtGui.QFont()
		font.setPointSize(7)
		self.Submit_root.setFont(font)
		self.Submit_root.setObjectName("Submit_root")
		self.Submit_user = QtWidgets.QPushButton(self.centralwidget)
		self.Submit_user.setGeometry(QtCore.QRect(270, 60, 61, 16))
		self.Submit_user.clicked.connect(lambda: Handler("Submit_user"))
		font = QtGui.QFont()
		font.setPointSize(7)
		self.Submit_user.setFont(font)
		self.Submit_user.setObjectName("Submit_user")
		self.line_2 = QtWidgets.QFrame(self.centralwidget)
		self.line_2.setGeometry(QtCore.QRect(330, -20, 20, 221))
		self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
		self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_2.setObjectName("line_2")
		self.label_13 = QtWidgets.QLabel(self.centralwidget)
		self.label_13.setGeometry(QtCore.QRect(350, 120, 81, 31))
		font = QtGui.QFont()
		font.setFamily("Segoe UI Historic")
		font.setPointSize(12)
		self.label_13.setFont(font)
		self.label_13.setObjectName("label_13")
		self.Points = QtWidgets.QLabel(self.centralwidget)
		self.Points.setGeometry(QtCore.QRect(400, 120, 61, 31))
		font = QtGui.QFont()
		font.setFamily("Segoe UI Historic")
		font.setPointSize(12)
		self.Points.setFont(font)
		self.Points.setObjectName("Points")
		self.Time_left = QtWidgets.QLabel(self.centralwidget)
		self.Time_left.setGeometry(QtCore.QRect(220, 210, 61, 31))
		font = QtGui.QFont()
		font.setFamily("Segoe UI Historic")
		font.setPointSize(12)
		self.Time_left.setFont(font)
		self.Time_left.setObjectName("Time_left")
		self.label_16 = QtWidgets.QLabel(self.centralwidget)
		self.label_16.setGeometry(QtCore.QRect(140, 210, 101, 31))
		font = QtGui.QFont()
		font.setFamily("Segoe UI Historic")
		font.setPointSize(12)
		self.label_16.setFont(font)
		self.label_16.setObjectName("label_16")
		self.label_2 = QtWidgets.QLabel(self.centralwidget)
		self.label_2.setGeometry(QtCore.QRect(190, 130, 131, 31))
		font = QtGui.QFont()
		font.setFamily("Segoe UI Historic")
		font.setPointSize(12)
		self.label_2.setFont(font)
		self.label_2.setObjectName("label_2")
		MainWindow.setCentralWidget(self.centralwidget)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "OSCP Exam"))
		self.label.setText(_translate("MainWindow", "Timer: "))
		self.Timer.setText(_translate("MainWindow", "00:00:00"))
		self.label_3.setText(_translate("MainWindow", "Root:"))
		self.label_4.setText(_translate("MainWindow", "User:"))
		self.Pause_timer.setText(_translate("MainWindow", "Pause"))
		self.Start_timer.setText(_translate("MainWindow", "Start"))
		self.Full_reset.setText(_translate("MainWindow", "Reset"))
		self.label_9.setText(_translate("MainWindow", "Roots:"))
		self.Roots.setText(_translate("MainWindow", "0"))
		self.label_11.setText(_translate("MainWindow", "Users:"))
		self.Users.setText(_translate("MainWindow", "0"))
		self.Reset.setText(_translate("MainWindow", "Reset"))
		self.Submit_root.setText(_translate("MainWindow", "Submit"))
		self.Submit_user.setText(_translate("MainWindow", "Submit"))
		self.label_13.setText(_translate("MainWindow", "Points:"))
		self.Points.setText(_translate("MainWindow", "0"))
		self.Time_left.setText(_translate("MainWindow", "00:00:00"))
		self.label_16.setText(_translate("MainWindow", "Time Left:"))
		self.label_2.setText(_translate("MainWindow", "Local Reset Button"))

	def closeEvent(self, event):
		# do stuff
		if can_exit:
			event.accept() # let the window close
		else:
			event.ignore()

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow(MainWindow)
MainWindow.show()
app.aboutToQuit.connect(Closing)
timer = QtCore.QTimer()
timer.timeout.connect(CurrentState)
timer.start(20)
sys.exit(app.exec_())
