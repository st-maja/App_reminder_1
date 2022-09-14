from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sqlite3
from datetime import date, datetime
import datetime

global not_text
not_text = ""


class Notification_window(QMainWindow):
	window_closed = pyqtSignal()

	def __init__(self, *args, **kwargs):
		super(Notification_window, self).__init__(*args, **kwargs)

	def setup(self, notification_window):
		notification_window.setObjectName("notification_window")

		notification_window.setFixedSize(260, 50)
		notification_window.move(2300, 150)

		notification_window.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
		notification_window.setAttribute(QtCore.Qt.WA_TranslucentBackground)

		self.centralwidget = QtWidgets.QWidget(notification_window)
		self.centralwidget.setObjectName("centralwidget")
		self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
		self.gridLayout.setObjectName("gridLayout")

		self.frame = QtWidgets.QFrame(self.centralwidget)
		self.frame.setGeometry(QtCore.QRect(0, 0, 255, 45))
		self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
		self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
		self.frame.setObjectName("frame")

		self.frame.setStyleSheet("QFrame#frame{border: 1px solid #DCD4D4;"
		                         "                     border-radius: 6px;"
		                         "                     background: #EFECEC;}")
		shadow = QGraphicsDropShadowEffect()
		# setting blur radius
		shadow.setBlurRadius(15)
		shadow.setColor(QColor(96, 91, 91))
		shadow.setOffset(0, 0)
		# adding shadow to the label
		self.frame.setGraphicsEffect(shadow)
		self.frame.lower()

		self.notification_label = QtWidgets.QLabel(self.frame)
		self.notification_label.setGeometry(QtCore.QRect(0, 0, 210, 35))
		self.notification_label.setObjectName("notification_label")
		self.notification_label.setAlignment(QtCore.Qt.AlignCenter)
		self.notification_label.setStyleSheet('font-size: 12pt; font-family: JetBrains Mono NL ;')

		self.close_not_btn = QtWidgets.QPushButton(self.frame)
		self.close_not_btn.setGeometry(QtCore.QRect(210, 1, 30, 30))
		self.close_not_btn.setObjectName("close_not_btn")
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("cancel_mark.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.close_not_btn.setIcon(icon)
		self.close_not_btn.setIconSize(QtCore.QSize(30, 30))
		self.close_not_btn.setCheckable(False)
		self.close_not_btn.setFlat(True)

		self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
		notification_window.setCentralWidget(self.centralwidget)

		self.retranslateUi(notification_window)
		QtCore.QMetaObject.connectSlotsByName(notification_window)

		# not the cutest solution but events are screwed
		self.close_not_btn.clicked.connect(self.not_event)
		self.close_not_btn.clicked.connect(notification_window.close)

		global not_text
		self.notification_label.setText(not_text)

	def not_event(self):
		self.window_closed.emit()

	def retranslateUi(self, notification_window):
		_translate = QtCore.QCoreApplication.translate
		notification_window.setWindowTitle(_translate("notification_window", "MainWindow"))


class Ui_MainWindow(QObject):

	def __init__(self, *args, **kwargs):
		super(Ui_MainWindow, self).__init__(*args, **kwargs)

		self.notification_win_active = 0

	def setupUi(self, MainWindow):
		MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		MainWindow.setObjectName("MainWindow")

		MainWindow.setFixedSize(210, 270)

		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")

		self.frame = QtWidgets.QFrame(self.centralwidget)
		self.frame.setGeometry(QtCore.QRect(5, 5, 200, 260))
		self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
		self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
		self.frame.setObjectName("frame")
		self.frame.mouseMoveEvent = self.mouseMoveEvent

		self.frame.setStyleSheet("QFrame#frame{border: 1px solid #DCD4D4;"
		                         "                     border-radius: 20px;"
		                         "                     background: #EFECEC;}")
		shadow = QGraphicsDropShadowEffect()
		# setting blur radius
		shadow.setBlurRadius(15)
		shadow.setColor(QColor(96, 91, 91))
		shadow.setOffset(0, 0)
		# adding shadow to the label
		self.frame.setGraphicsEffect(shadow)
		self.frame.lower()

		self.listWidget = QtWidgets.QListWidget(self.frame)
		self.listWidget.setGeometry(QtCore.QRect(20, 130, 160, 100))
		self.listWidget.setObjectName("listWidget")

		self.formLayoutWidget = QtWidgets.QWidget(self.frame)
		self.formLayoutWidget.setGeometry(QtCore.QRect(20, 10, 161, 91))
		self.formLayoutWidget.setObjectName("formLayoutWidget")

		self.verticalLayout = QtWidgets.QVBoxLayout(self.formLayoutWidget)
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout.setObjectName("verticalLayout")

		self.dateTimeEdit = QtWidgets.QDateTimeEdit(self.formLayoutWidget)
		self.dateTimeEdit.setAlignment(QtCore.Qt.AlignCenter)
		self.dateTimeEdit.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
		self.dateTimeEdit.setCurrentSection(QtWidgets.QDateTimeEdit.DaySection)
		self.dateTimeEdit.setObjectName("dateTimeEdit")
		self.verticalLayout.addWidget(self.dateTimeEdit)
		self.dateTimeEdit.setStyleSheet('font-size: 12pt; font-family: JetBrains Mono NL ;')

		self.new_task_btn = QtWidgets.QPushButton(self.frame)
		self.new_task_btn.setObjectName("new_task_btn")
		self.new_task_btn.setGeometry(60, 95, 30, 30)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("check_mark.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.new_task_btn.setIcon(icon)
		self.new_task_btn.setIconSize(QtCore.QSize(30, 30))
		self.new_task_btn.setCheckable(False)
		self.new_task_btn.setFlat(True)

		self.task_text = QtWidgets.QLineEdit(self.formLayoutWidget)
		self.task_text.setObjectName("task_text")
		self.verticalLayout.addWidget(self.task_text)
		self.task_text.setStyleSheet('font-size: 12pt; font-family: JetBrains Mono NL ;')

		self.remove_one_btn = QtWidgets.QPushButton(self.frame)
		self.remove_one_btn.setGeometry(QtCore.QRect(100, 95, 30, 30))
		self.remove_one_btn.setObjectName("remove_one_btn")
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("cancel_mark.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.remove_one_btn.setIcon(icon)
		self.remove_one_btn.setIconSize(QtCore.QSize(30, 30))
		self.remove_one_btn.setCheckable(False)
		self.remove_one_btn.setFlat(True)
		self.remove_one_btn.clicked.connect(self.remove_one)

		# minimize btn
		self.min_btn = QtWidgets.QPushButton(self.frame)
		self.min_btn.setGeometry(0, 225, 30, 30)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("min_black.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.min_btn.setIcon(icon)
		self.min_btn.setIconSize(QtCore.QSize(15, 15))
		self.min_btn.setCheckable(False)
		self.min_btn.setFlat(True)
		self.min_btn.clicked.connect(self.minimize)

		# close btn
		self.close_btn = QtWidgets.QPushButton(self.frame)
		self.close_btn.setGeometry(170, 225, 30, 30)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("close_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.close_btn.setIcon(icon)
		self.close_btn.setIconSize(QtCore.QSize(15, 15))
		self.close_btn.setCheckable(False)
		self.close_btn.setFlat(True)
		self.close_btn.clicked.connect(self.shutdown)
		self.close_btn.clicked.connect(MainWindow.close)

		MainWindow.setCentralWidget(self.centralwidget)
		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

		# actual code things
		self.dateTimeEdit.setDateTime(QtCore.QDateTime.currentDateTime())
		self.new_task_btn.clicked.connect(self.new_task)
		self.remove_one_btn.clicked.connect(self.remove_one)
		self.create_db()

		self.timer_check()
		self.show_tasks()
		self.check_dates()

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
		self.dateTimeEdit.setDisplayFormat(_translate("MainWindow", "d-M-yy @ H:mm"))

	# lame threading
	def timer_check(self):
		self.timer = QTimer()
		self.timer.timeout.connect(self.check_dates)
		self.timer.start(30000)

	# this will fire the notification
	def check_dates(self):
		db = sqlite3.connect("tasks_db.db")
		cursor = db.cursor()
		today = date.today()
		d1 = today.strftime("%d/%m/%Y")
		current = datetime.datetime.now().time()

		cursor = db.execute("SELECT * from (SELECT * FROM TASKS ORDER BY DATE DESC) ORDER BY TIME")
		for row in cursor:
			if row[1] == d1:
				global not_text
				not_text = row[0]
				t1 = row[2].split(':')
				end = datetime.time(int(t1[0]), int(t1[1]), 0)

				if self.time_in_range(end, current):
					self.open_notification()
		db.close()

	def time_in_range(self, end, current):
		return current >= end

	def create_db(self):
		db = sqlite3.connect("tasks_db.db")
		cursor = db.cursor()
		cursor.execute('''CREATE TABLE IF NOT EXISTS TASKS
                 (TASK_NAME  TEXT,
                 DATE   DATE,
                 TIME   TEXT);''')
		db.close()

	def new_task(self):
		# get date
		date_time = self.dateTimeEdit.dateTime().toPyDateTime()
		date = date_time.strftime("%d/%m/%Y")
		time = date_time.strftime("%H:%M")

		# get text
		new_task = str(self.task_text.text())

		if self.task_text.text() != "":
			db = sqlite3.connect("tasks_db.db")
			cursor = db.cursor()
			query = "INSERT INTO tasks(task_name, date, time) VALUES (?,?,?)"
			row = (new_task, date, time)
			cursor.execute(query, row)
			db.commit()
			db.close()
		else:
			self.task_text.setPlaceholderText("Add a task")

		self.check_table()
		self.dateTimeEdit.setDateTime(QtCore.QDateTime.currentDateTime())

	def check_table(self):
		self.check_dates()
		self.show_tasks()

	def show_tasks(self):
		self.listWidget.clear()
		db = sqlite3.connect("tasks_db.db")
		cursor = db.cursor()
		cursor = db.execute("SELECT * from (SELECT * FROM TASKS ORDER BY DATE DESC) ORDER BY TIME")

		for row in cursor:
			item = QListWidgetItem(str(row[0]))
			item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
			item.setCheckState(QtCore.Qt.Unchecked)
			self.listWidget.addItem(item)
		db.close()

	def remove_one(self):
		db = sqlite3.connect("tasks_db.db")
		cursor = db.cursor()
		for i in range(self.listWidget.count()):
			item = self.listWidget.item(i)

			if item.checkState() == 2:
				task_deletion = item.text()
				db.execute("DELETE from tasks where task_name = ?", (task_deletion,))
				db.commit()
		self.show_tasks()
		db.close()

	def not_window(self):
		self.window = QtWidgets.QMainWindow()
		self.ui = Notification_window()
		self.ui.setup(self.window)
		self.window.show()

		self.ui.window_closed.connect(self.closed_notification)

	def closed_notification(self):
		self.notification_win_active = 0

	def open_notification(self):
		if not self.notification_win_active:
			self.not_window()
			self.notification_win_active = 1

	def minimize(self):
		self.showMinimized()

	def shutdown(self, event):
		self.window = QtWidgets.QMainWindow()
		self.ui = Notification_window()
		self.ui.setup(self.window)
		self.window.close()


class MyWin(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.dragPos = QtCore.QPoint()

	def mousePressEvent(self, event):
		self.dragPos = event.globalPos()

	def mouseMoveEvent(self, event):
		if event.buttons() == QtCore.Qt.LeftButton:
			self.move(self.pos() + event.globalPos() - self.dragPos)
			self.dragPos = event.globalPos()
			event.accept()


if __name__ == "__main__":
	import sys

	app = QtWidgets.QApplication(sys.argv)
	w = MyWin()
	w.show()
	sys.exit(app.exec_())
