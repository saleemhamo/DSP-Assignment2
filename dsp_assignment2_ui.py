from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QEventLoop, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox

from data_management import *


class Ui_MainWindow(object):

	def speak(self):
		self.image_label.setPixmap(QtGui.QPixmap("./images/voice.png"))
		self.image_label.setStyleSheet("border: 3px solid black;")
		loop = QEventLoop()
		QTimer.singleShot(10, loop.quit)
		loop.exec_()
		record_and_save("test.wav")

		data = read_wav_signal("test.wav")
		yes_data = read_json("./data_record/yes_data.json")
		no_data = read_json("./data_record/no_data.json")
		data_energy = find_energy(data)
		data_zcc = find_ZCR(data)
		psd_ = psd(data)
		psd_ = psd_[0]
		# my_plot(psd_, "PSD")
		low = psd_[0:int(len(data) / 2)]
		high = psd_[int(len(data) / 2):]
		psd_ = np.sum(psd_)
		low = np.sum(low)
		high = np.sum(high)

		print("Energy = {}, ZCC = {}, PSD = {}, low = {}, high = {}".format(data_energy[0], data_zcc, psd_, low,
											     high))
		yes_vector = [yes_data["average"]["avg_energy"], yes_data["average"]["avg_zcc"],
				yes_data["average"]["avg_psd"],
				yes_data["average"]["avg_psd_high"], yes_data["average"]["avg_psd_high"]]
		no_vector = [no_data["average"]["avg_energy"], no_data["average"]["avg_zcc"],
			      no_data["average"]["avg_psd"],
			      no_data["average"]["avg_psd_high"], no_data["average"]["avg_psd_high"]]
		sample_vector = [data_energy[0], data_zcc, psd_, low, high]

		d_yes = distance(yes_vector, sample_vector)
		d_no = distance(no_vector, sample_vector)

		print(d_yes)
		print(d_no)

		if d_yes < d_no:
			self.image_label.setPixmap(QtGui.QPixmap("./images/yes.png"))
			print("YES")
		else:
			print("NO")
			self.image_label.setPixmap(QtGui.QPixmap("./images/no.png"))
		self.enable_btns()

	def signal(self):

		data = read_wav_signal("test.wav")
		my_plot(data, "Your Voice")
		msg = QMessageBox()
		msg.setWindowTitle("Decoded Signal")
		msg.setIconPixmap(QPixmap("./images/test.png"))
		x = msg.exec_()

	def ft(self):
		data = read_wav_signal("test.wav")
		plot_ft(data)
		msg = QMessageBox()
		msg.setWindowTitle("Decoded Signal")
		msg.setIconPixmap(QPixmap("./images/test_ft.png"))
		x = msg.exec_()

	def more_info(self):
		data = read_wav_signal("test.wav")
		data_energy = find_energy(data)
		data_zcc = find_ZCR(data)
		psd_ = psd(data)
		psd_ = psd_[0]
		low = psd_[0:int(len(data) / 2)]
		high = psd_[int(len(data) / 2):]
		psd_ = np.sum(psd_)
		low = np.sum(low)
		high = np.sum(high)
		info = ("Energy = {}\nZCC = {}\nPSD = {}\nPower in lower part = {}\nPower in higher part = {}".format(
			data_energy[0], data_zcc, psd_, low,
			high))
		msg = QMessageBox()
		msg.setWindowTitle("Problem Formulation")
		# msg.setText("Problem Formulation")
		msg.setText(info)
		msg.setStyleSheet(
			"QLabel{min-width:1400 px;min-height:700 px; font: 20pt \"Arial Rounded MT Bold\";} QPushButton{ width:250px; font-size: 18px; }");

		x = msg.exec_()

	def psd_plot(self):
		data = read_wav_signal("test.wav")
		p = psd(data)
		my_plot(p[0], "Power Spectral Density")
		msg = QMessageBox()
		msg.setWindowTitle("Decoded Signal")
		msg.setIconPixmap(QPixmap("./images/test.png"))
		x = msg.exec_()

	def enable_btns(self):
		self.speeak_ptn.setEnabled(False)
		self.signal_btn.setEnabled(True)
		self.ft_btn.setEnabled(True)
		self.psd_btn.setEnabled(True)
		self.more_info_btn.setEnabled(True)

	def disable_btns(self):
		self.speeak_ptn.setEnabled(True)
		self.signal_btn.setEnabled(False)
		self.ft_btn.setEnabled(False)
		self.psd_btn.setEnabled(False)
		self.more_info_btn.setEnabled(False)

	def reset(self):
		self.disable_btns()
		self.image_label.setPixmap(QtGui.QPixmap("../../PycharmProjects/DSP-Assignment2/images/start.PNG"))

	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(1128, 888)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.background_label = QtWidgets.QLabel(self.centralwidget)
		self.background_label.setGeometry(QtCore.QRect(0, 0, 1181, 861))
		self.background_label.setText("")
		self.background_label.setPixmap(
			QtGui.QPixmap("../../PycharmProjects/DSP-Assignment2/images/background.PNG"))
		self.background_label.setScaledContents(True)
		self.background_label.setWordWrap(False)
		self.background_label.setObjectName("background_label")
		self.image_label = QtWidgets.QLabel(self.centralwidget)
		self.image_label.setGeometry(QtCore.QRect(410, 110, 321, 281))
		self.image_label.setText("")
		self.image_label.setPixmap(QtGui.QPixmap("../../PycharmProjects/DSP-Assignment2/images/start.PNG"))
		self.image_label.setScaledContents(True)
		self.image_label.setObjectName("image_label")
		self.image_label.setStyleSheet("border: 3px solid black;")

		self.speeak_ptn = QtWidgets.QPushButton(self.centralwidget)
		self.speeak_ptn.setGeometry(QtCore.QRect(360, 420, 421, 111))
		self.speeak_ptn.setStyleSheet("  background-color:rgb(1, 66, 127);\n"
						  "  border: none;\n"
						  "  color: white;\n"
						  "  padding: 15px 32px;\n"
						  "  text-align: center;\n"
						  "  text-decoration: none;\n"
						  "  display: inline-block;\n"
						  "  font-size: 40px;\n"
						  "border-radius: 20px;")
		self.speeak_ptn.setObjectName("speeak_ptn")
		self.reset_btn = QtWidgets.QPushButton(self.centralwidget)
		self.reset_btn.setGeometry(QtCore.QRect(410, 710, 331, 111))
		self.reset_btn.setStyleSheet("  background-color:rgb(1, 66, 127);\n"
						 "  border: none;\n"
						 "  color: white;\n"
						 "  padding: 15px 32px;\n"
						 "  text-align: center;\n"
						 "  text-decoration: none;\n"
						 "  display: inline-block;\n"
						 "  font-size: 40px;\n"
						 "border-radius: 20px;")
		self.reset_btn.setObjectName("reset_btn")
		self.label = QtWidgets.QLabel(self.centralwidget)
		self.label.setGeometry(QtCore.QRect(10, 720, 111, 121))
		self.label.setStyleSheet("font: 75 10pt \"Goudy Old Style\";")
		self.label.setObjectName("label")
		self.label_2 = QtWidgets.QLabel(self.centralwidget)
		self.label_2.setGeometry(QtCore.QRect(230, 30, 961, 61))
		self.label_2.setStyleSheet("font: 75 26pt \"Goudy Old Style\";")
		self.label_2.setObjectName("label_2")
		self.ft_btn = QtWidgets.QPushButton(self.centralwidget)
		self.ft_btn.setGeometry(QtCore.QRect(360, 560, 201, 91))
		self.ft_btn.setStyleSheet("  background-color:rgb(127, 127, 127);\n"
					     "  border: none;\n"
					     "  color: white;\n"
					     "  text-align: center;\n"
					     "  text-decoration: none;\n"
					     "  display: inline-block;\n"
					     "  font-size: 40px;\n"
					     "border-radius: 20px;")
		self.ft_btn.setObjectName("ft_btn")
		self.more_info_btn = QtWidgets.QPushButton(self.centralwidget)
		self.more_info_btn.setGeometry(QtCore.QRect(800, 560, 201, 91))
		self.more_info_btn.setStyleSheet("  background-color:rgb(127, 127, 127);\n"
						     "  border: none;\n"
						     "  color: white;\n"
						     "  text-align: center;\n"
						     "  text-decoration: none;\n"
						     "  display: inline-block;\n"
						     "  font-size: 40px;\n"
						     "border-radius: 20px;")
		self.more_info_btn.setObjectName("more_info_btn")
		self.psd_btn = QtWidgets.QPushButton(self.centralwidget)
		self.psd_btn.setGeometry(QtCore.QRect(580, 560, 201, 91))
		self.psd_btn.setStyleSheet("  background-color:rgb(127, 127, 127);\n"
					      "  border: none;\n"
					      "  color: white;\n"
					      "  text-align: center;\n"
					      "  text-decoration: none;\n"
					      "  display: inline-block;\n"
					      "  font-size: 40px;\n"
					      "border-radius: 20px;")
		self.psd_btn.setObjectName("psd_btn")
		self.signal_btn = QtWidgets.QPushButton(self.centralwidget)
		self.signal_btn.setGeometry(QtCore.QRect(150, 560, 201, 91))
		self.signal_btn.setStyleSheet("  background-color:rgb(127, 127, 127);\n"
						  "  border: none;\n"
						  "  color: white;\n"
						  "  text-align: center;\n"
						  "  text-decoration: none;\n"
						  "  display: inline-block;\n"
						  "  font-size: 40px;\n"
						  "border-radius: 20px;")
		self.signal_btn.setObjectName("signal_btn")
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 1128, 26))
		self.menubar.setObjectName("menubar")
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

		self.speeak_ptn.clicked.connect(self.speak)
		self.signal_btn.clicked.connect(self.signal)
		self.ft_btn.clicked.connect(self.ft)
		self.psd_btn.clicked.connect(self.psd_plot)
		self.reset_btn.clicked.connect(self.reset)
		self.more_info_btn.clicked.connect(self.more_info)

		self.disable_btns()

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "DSP Assignment 2"))
		self.speeak_ptn.setText(_translate("MainWindow", "Speak"))
		self.reset_btn.setText(_translate("MainWindow", "Reset"))
		self.label.setText(_translate("MainWindow", "Done By:\n"
								  "Saleem Hamo\n"
								  "1170381"))
		self.label_2.setText(_translate("MainWindow", "Digital Signal Processing - Assignment 2"))
		self.ft_btn.setText(_translate("MainWindow", "FT"))
		self.more_info_btn.setText(_translate("MainWindow", "More Info"))
		self.psd_btn.setText(_translate("MainWindow", "PSD"))
		self.signal_btn.setText(_translate("MainWindow", "Signal"))


if __name__ == "__main__":
	import sys

	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())
