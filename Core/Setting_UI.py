# _*_ coding:utf-8 _*_ #
# @Time     :2019/12/26 15:34
# @Author   :Fighter
# @Software :Heater
# @E-mail    :317431629@qq.com
from PySide2 import QtWidgets


class SettingUi(QtWidgets.QWidget):
	def __init__(self):
		super(SettingUi, self).__init__()
		self.setGeometry(100, 200, 400, 450)
		self.main_layout = QtWidgets.QVBoxLayout(self)
		# _____________Assets_Name_____________#
		self.assets_name_Layout = QtWidgets.QHBoxLayout()
		self.assets_name_label = QtWidgets.QLabel('Assets Name:')
		self.assets_name_line = QtWidgets.QLineEdit()
		self.assets_name_line.setPlaceholderText(u'输入置产名字')
		self.assets_name = self.assets_name_line.text()

		self.assets_name_Layout.addWidget(self.assets_name_label)
		self.assets_name_Layout.addWidget(self.assets_name_line)
		# _____________Assets_Type_____________#
		self.assets_type_Layout = QtWidgets.QHBoxLayout()
		self.assets_type_label = QtWidgets.QLabel('Assets Type:')
		self.assets_type_combobox = QtWidgets.QComboBox()
		self.assets_type = self.assets_type_combobox.currentText()

		self.assets_type_Layout.addWidget(self.assets_type_label)
		self.assets_type_Layout.addWidget(self.assets_type_combobox)
		# _____________Publish_____________#
		self.publish_layout = QtWidgets.QHBoxLayout()
		self.publish_button = QtWidgets.QPushButton('Publish')
		self.publish_button.setMinimumWidth(80)
		self.publish_button.setMinimumHeight(80)
		self.publish_button.setStyleSheet("border: 1px solid gray;border-radius: 40px;")

		self.publish_layout.addStretch()
		self.publish_layout.addWidget(self.publish_button)

		self.setup_ui()

	def setup_ui(self):
		self.main_layout.addLayout(self.assets_name_Layout)
		self.main_layout.addLayout(self.assets_type_Layout)
		self.main_layout.addLayout(self.publish_layout)


if __name__ == '__main__':
	library = SettingUi()
	library.show()
