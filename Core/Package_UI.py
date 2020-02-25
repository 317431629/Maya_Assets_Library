# _*_ coding:utf-8 _*_ #
# @Time     :2020/2/19 9:19
# @Author   :Fighter
# @Software :Heater
# @E-mail    :317431629@qq.com

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui


class PackageUI(QtWidgets.QWidget):
	def __init__(self):
		super(PackageUI, self).__init__()

		self.check_groupbox = QtWidgets.QGroupBox('Check Scene')
