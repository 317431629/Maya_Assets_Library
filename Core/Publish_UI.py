# _*_ coding:utf-8 _*_ #
# @Time     :2019/12/31 17:20
# @Author   :Fighter
# @Software :Heater
# @E-mail    :317431629@qq.com
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
import sys


class PublishUI(QtWidgets.QDialog):
	def __init__(self):
		super(PublishUI, self).__init__()
		self.setWindowTitle('Publish Assets to Library')
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		self.setGeometry(150, 150, 600, 500)

		self.main_layout = QtWidgets.QVBoxLayout(self)

		self.assets_group_box = QtWidgets.QGroupBox('Assets_Setting')
		self.assets_layout = QtWidgets.QVBoxLayout(self.assets_group_box)

		self.renderer_layout = QtWidgets.QHBoxLayout()
		self.renderer_type_label = QtWidgets.QLabel("Renderer：")
		self.renderer_type = QtWidgets.QComboBox()
		self.renderer_type.addItem("Arnold")
		self.renderer_type.addItem("Redshift")

		self.assets_name_layout = QtWidgets.QHBoxLayout()
		self.assets_name_label = QtWidgets.QLabel('Assets_Name:')
		self.assets_name_line = QtWidgets.QLineEdit()
		self.assets_name_line.setPlaceholderText('Place Input Assets Name')
		self.assets_name_line.setMinimumHeight(35)

		self.assets_type_layout = QtWidgets.QHBoxLayout()
		self.assets_type_label = QtWidgets.QLabel('Assets_Type:')
		self.assets_type_line = QtWidgets.QLineEdit()
		self.assets_type_line.setPlaceholderText('Place Input Assets Type')
		self.assets_type_line.setMinimumHeight(35)

		self.assets_image_layout = QtWidgets.QHBoxLayout()
		self.assets_image_label = QtWidgets.QLabel('Assets_Image:')
		self.assets_image_line = QtWidgets.QLineEdit()
		self.assets_image_line.setPlaceholderText('Place Choice Assets Image')
		self.assets_image_line.setReadOnly(True)
		self.assets_image_line.setMinimumHeight(35)
		self.assets_image_button = QtWidgets.QPushButton('Open')

		self.assets_proxy_layout = QtWidgets.QHBoxLayout()
		self.assets_proxy = QtWidgets.QCheckBox("Export Proxy")

		self.preview_group_box = QtWidgets.QGroupBox('Assets Preview')
		self.preview_layout = QtWidgets.QHBoxLayout(self.preview_group_box)

		self.show_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
		self.show_list_label = QtWidgets.QLabel()
		pix_map = QtGui.QPixmap("{}/Icon/Not_Found_Image.png".format(sys.path[-1]))
		self.show_list_label.setPixmap(pix_map)
		self.show_list_label.setMinimumSize(120, 120)
		self.show_list_text = QtWidgets.QTextEdit()
		self.show_list_text.setText("\n\b\b\n".join(["Assets_name:", "Assets_type:", "Renderer:", ""]))
		self.show_list_text.setReadOnly(True)

		self.publish_group_box = QtWidgets.QGroupBox('Publish')
		self.publish_layout = QtWidgets.QHBoxLayout(self.publish_group_box)
		self.publish_button = QtWidgets.QPushButton('Publish To Library')

		self.setup_ui()
		self.set_stylesheet()

	def setup_ui(self):
		self.renderer_layout.addStretch()
		self.renderer_layout.addWidget(self.renderer_type_label)
		self.renderer_layout.addWidget(self.renderer_type)

		self.assets_name_layout.addWidget(self.assets_name_label)
		self.assets_name_layout.addWidget(self.assets_name_line)

		self.assets_type_layout.addWidget(self.assets_type_label)
		self.assets_type_layout.addWidget(self.assets_type_line)

		self.assets_proxy_layout.addWidget(self.assets_proxy)

		self.assets_image_layout.addWidget(self.assets_image_label)
		self.assets_image_layout.addWidget(self.assets_image_line)
		self.assets_image_layout.addWidget(self.assets_image_button)

		self.show_splitter.addWidget(self.show_list_label)
		self.show_splitter.addWidget(self.show_list_text)

		self.publish_layout.addStretch()
		self.publish_layout.addWidget(self.publish_button)

		self.assets_layout.addLayout(self.renderer_layout)
		self.assets_layout.addLayout(self.assets_name_layout)
		self.assets_layout.addLayout(self.assets_type_layout)
		self.assets_layout.addLayout(self.assets_image_layout)
		self.assets_layout.addLayout(self.assets_proxy_layout)

		self.preview_layout.addWidget(self.show_splitter)

		self.main_layout.addWidget(self.assets_group_box)
		self.main_layout.addWidget(self.preview_group_box)
		self.main_layout.addStretch()
		self.main_layout.addWidget(self.publish_group_box)

	def set_preview_data(self):
		assets_name = self.assets_name_line.text()
		assets_type = self.assets_type_line.text()
		renderer = self.renderer_type.currentText()
		data = "\n\b\b{}\n".join(["Assets_name:", "Assets_type:", "Renderer:", ""]).format(assets_name, assets_type, renderer)
		self.show_list_text.setText(data)

	def set_stylesheet(self):
		self.setStyleSheet('''
							QLineEdit{
								background:transparent;
								border-width:0;border-style:outset;
								font: 75 9pt "Sitka Small";}
							QLabel{
							font: 75 9pt "Sitka Small";
							}
							QGroupBox{
							font: 75 9pt "Sitka Small";
							border: 2px solid gray;
							border-radius: 6px;
							}
							QPushButton{
							font: 75 9pt "Sitka Small";
							}
							QPushButton:hover{color:black}
							''')


if __name__ == '__main__':
	library = PublishUI()
	library.show()
