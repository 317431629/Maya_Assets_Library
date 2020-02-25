# _*_ coding:utf-8 _*_ #
# @Time     :2019/12/23 13:18
# @Author   :Fighter
# @Software :Maya
# @E-mail   :317431629@qq.com
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
from Core import Creat_Data
from Core import Publish_Method
from Script import Custom_SearchBox
import os
import sys
from pprint import pprint

reload(Creat_Data)
reload(Publish_Method)
reload(Custom_SearchBox)


class LibraryWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super(LibraryWindow, self).__init__()
		self.data_path = "{}/Data/data.db".format(sys.path[-1])
		self.database = Creat_Data.DataBase(self.data_path)
		self.data = self.database.get_all_data()
		# pprint(self.data)
		self.publish_ui = Publish_Method.PublishFoo()
		self.about_ui = AboutUI()
		self.setting_ui = ProjectSetUI()
		self.setWindowTitle(u'Assets_Library')
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		self.assets_data = []
		self.model = []
		self.ma_image = QtGui.QIcon("{}/Icon/hsFileMayaMA.png".format(sys.path[-1]))
		self.mb_image = QtGui.QIcon("{}/Icon/hsFileMayaMB.png".format(sys.path[-1]))
		self.setGeometry(100, 100, 1350, 660)
		self.image_size = QtCore.QSize(220, 220)
		self.setup_ui()
		self.set_stylesheet()
		self.connect_ui()

	def set_stylesheet(self):
		self.setStyleSheet('''
							font: 75 9pt "Sitka Small";
							QPushButton{
							border: 2px solid gray;
							border-radius: 3px;
							}
							QComboBox{
							font: 9pt "Sitka Small";
									}
							QPushButton:hover{color:black}
							QTextEdit{
							border: 2px solid gray;
							border-radius: 3px;
									}
							''')

	def setup_ui(self):
		# __________________menu_________________#
		self.menu = self.menuBar()
		self.file_menu = self.menu.addMenu('File')
		self.edit_menu = self.menu.addMenu('Edit')
		self.help_menu = self.menu.addMenu('Help')

		self.import_assets_Action = QtWidgets.QAction('Import Assets', self)
		self.file_menu.addAction(self.import_assets_Action)

		self.setting_Action = QtWidgets.QAction('setting', self)
		self.edit_menu.addAction(self.setting_Action)

		self.about_Action = QtWidgets.QAction('About_User', self)
		self.help_menu.addAction(self.about_Action)
		# _________________widget________________#
		self.frame = QtWidgets.QFrame()
		self.main_layout = QtWidgets.QVBoxLayout(self.frame)

		self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
		# ________________stacked_________________#
		self.listview_frame = QtWidgets.QFrame()
		self.listview_layout = QtWidgets.QVBoxLayout(self.listview_frame)

		self.list_view = CustomListView()
		self.list_view.setViewMode(QtWidgets.QListView.IconMode)
		self.list_view.setMovement(QtWidgets.QListView.Static)
		self.list_view.setIconSize(self.image_size)

		self.search_line = Custom_SearchBox.CustomSearch()
		self.search_line.setMinimumHeight(30)
		self.search_line.setPlaceholderText('Search to anything...')

		self.slider_frame = QtWidgets.QWidget()
		self.slider_layout = QtWidgets.QHBoxLayout(self.slider_frame)
		self.refresh_button = QtWidgets.QPushButton('Refresh Library')
		self.refresh_button.setMinimumHeight(30)

		self.slider_layout.addStretch()
		self.slider_layout.addWidget(self.refresh_button)

		self.listview_layout.addWidget(self.search_line)
		self.listview_layout.addWidget(self.list_view)
		self.listview_layout.addWidget(self.slider_frame)
		# _____________Setting Mod__________________#
		self.setting_frame = QtWidgets.QFrame()
		self.setting_frame.setMaximumWidth(self.splitter.width()/5)
		self.setting_layout = QtWidgets.QVBoxLayout(self.setting_frame)
		# _____________Type_Combobox__________________#
		self.type_combobox = QtWidgets.QComboBox()
		for assets_type in self.database.get_type():
			self.type_combobox.addItem(assets_type[0])
		self.type_combobox.setMinimumHeight(40)
		# ____________Second level Type________________#
		# todo: 还未完善此功能，后期完善
		self.second_level_layout = QtWidgets.QVBoxLayout()

		self.setting_layout.addWidget(self.type_combobox)
		self.setting_layout.addStretch()
		# _____________Information______________#
		self.information_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)

		self.information_group = QtWidgets.QGroupBox("Information")
		self.information_group.setMaximumSize(180, 220)
		self.information_layout = QtWidgets.QHBoxLayout(self.information_group)
		self.information_text = QtWidgets.QTextEdit()
		self.information_text.setMaximumWidth(self.splitter.width()/3)
		self.information_text.setReadOnly(True)
		self.information_layout.addWidget(self.information_text)

		self.file_group = QtWidgets.QGroupBox("File_List")
		self.file_layout = QtWidgets.QHBoxLayout(self.file_group)
		self.file_list = QtWidgets.QListWidget()
		self.file_list.setIconSize(QtCore.QSize(50, 50))
		self.file_layout.addWidget(self.file_list)

		self.information_splitter.addWidget(self.information_group)
		self.information_splitter.addWidget(self.file_group)
		# self.information_text.setStyleSheet('background-color:black')
		self.splitter.addWidget(self.setting_frame)
		self.splitter.addWidget(self.listview_frame)
		self.splitter.addWidget(self.information_splitter)
		# _____________Button___________________#
		self.button_layout = QtWidgets.QHBoxLayout()

		self.remove_button = QtWidgets.QPushButton('Remove Assets from Library')
		self.import_button = QtWidgets.QPushButton('Import to Scene')
		self.import_proxy_button = QtWidgets.QPushButton("Import Proxy to Scene")
		self.publish_button = QtWidgets.QPushButton('Publish Assets to Library')
		self.remove_button.setMinimumHeight(30)
		self.import_button.setMinimumHeight(30)
		self.publish_button.setMinimumHeight(30)

		self.button_layout.addStretch()
		self.button_layout.addWidget(self.remove_button)
		self.button_layout.addWidget(self.import_button)
		self.button_layout.addWidget(self.import_proxy_button)
		self.button_layout.addWidget(self.publish_button)

		self.main_layout.addWidget(self.splitter)
		self.main_layout.addLayout(self.button_layout)

		self.setCentralWidget(self.frame)

	def connect_ui(self):
		self.set_mode()
		self.type_combobox.currentIndexChanged.connect(self.set_mode)
		self.search_line.textChanged.connect(self.search_assets)
		self.list_view.clicked.connect(self.file_list_information)
		self.file_list.clicked.connect(self.set_information)
		self.publish_button.clicked.connect(self.publish_ui.show)
		self.about_Action.triggered.connect(self.about_ui.show)
		self.setting_Action.triggered.connect(self.setting_ui.show)

	def create_mod(self, assets_type, assets_filter):
		assets_names = []
		try:
			list_mod = QtGui.QStandardItemModel()
		except AttributeError:
			list_mod = QtCore.QStandardItemModel()
		if isinstance(assets_filter, int) or assets_filter == 'combobox':
			for data in self.database.get_type_data(assets_type):
				assets_name = data[0].split('.ma')[0][:-3]
				if assets_name not in assets_names:
					assets_image = data[-1]
					item = self.creat_list_item(assets_image, assets_name)
					list_mod.appendRow(item)
					assets_names.append(assets_name)
		else:
			for data in self.database.get_filter_data(assets_type, assets_filter):
				assets_name = data[0].split('.ma')[0][:-3]
				if assets_name not in assets_names:
					assets_image = data[-1]
					item = self.creat_list_item(assets_image, assets_name)
					list_mod.appendRow(item)
					assets_names.append(assets_name)
		return list_mod

	@staticmethod
	def creat_list_item(assets_image, assets_name):
		item = QtGui.QStandardItem(QtGui.QIcon(assets_image), assets_name)
		return item

	def set_mode(self, assets_filter='combobox'):
		assets_type = self.type_combobox.currentText()
		self.model = self.create_mod(assets_type, assets_filter)
		self.list_view.setModel(self.model)
		return self.model

	def get_data_for_sel(self, model_index):
		assets = model_index.data()
		return self.database.get_sel_data(assets)

	def file_list_information(self, model_index):
		self.file_list.clear()
		for data in self.get_data_for_sel(model_index):
			assets_name, assets_type, assets_path, renderer, assets_image = data
			list_item = QtWidgets.QListWidgetItem(self.ma_image, assets_name)
			self.file_list.addItem(list_item)

	def set_information(self):
		def format_size(assets_bytes):
			assets_bytes = float(assets_bytes)
			kb = assets_bytes / 1024
			if kb >= 1024:
				M = kb / 1024
				if M >= 1024:
					G = M / 1024
					return "%fG" % (G)
				else:
					return "%fM" % (M)
			else:
				return "%fkb" % (kb)
		self.assets_data = self.database.get_sel_data(self.file_list.currentItem().text())[0]
		assets_name, assets_type, assets_path, renderer, assets_image = self.assets_data
		assets_size = format_size(os.path.getsize(assets_path))
		information = "\n\b\b{}\n".join(["Assets_name:", "Assets_type:", "Assets_path:", "Renderer:", "Assets_size:", ""]).format(
						assets_name[:-3], assets_type, assets_path, renderer, assets_size)
		self.information_text.setText(information)
		return self.assets_data

	def search_assets(self):
		assets_filter = "%{}%".format(self.search_line.text())
		self.set_mode(assets_filter)

	def closeEvent(self, event):
		# self.database.cursor.execute("DROP DATABASE {}".format(self.data_path))
		event.accept


class CustomListView(QtWidgets.QListView):
	def __init__(self):
		super(CustomListView, self).__init__()
		self.set_stylesheet()

	# 实时监控空间大小
	def resizeEvent(self, event):
		width = self.width()
		image_size = QtCore.QSize((width - 5)/3, (width - 5)/3)
		self.setIconSize(image_size)

	# def wheelEvent(self, event):
	# 	print 'wheelEvent'

	def set_stylesheet(self):
		self.setStyleSheet('''
								border: 2px solid gray;
								border-radius: 3px;
								font: 75 10pt "Sitka Small";
							''')


class AboutUI(QtWidgets.QDialog):
	def __init__(self):
		super(AboutUI, self).__init__()
		self.user_information_path = "{}/Data/About.config".format(sys.path[-1])
		self.logo_path = "{}Icon/Logo.png".format(sys.path[-1])
		with open(self.user_information_path) as f:
			self.user_information = f.read()
		self.setWindowTitle('About_Author')
		self.setMinimumSize(500, 500)
		self.setMaximumSize(500,500)
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		self.main_layout = QtWidgets.QVBoxLayout(self)

		self.logo_layout = QtWidgets.QHBoxLayout()

		self.logo_image = QtGui.QPixmap(self.logo_path)
		self.logo_label = QtWidgets.QLabel()
		self.logo_label.setPixmap(self.logo_image)

		self.logo_layout.addStretch()
		self.logo_layout.addWidget(self.logo_label)
		self.logo_layout.addStretch()

		self.about_text = QtWidgets.QTextEdit()
		self.about_text.setReadOnly(True)
		self.about_text.setText(self.user_information)

		self.check_layout = QtWidgets.QHBoxLayout()
		self.check_button = QtWidgets.QPushButton('OK')
		self.check_button.setMinimumWidth(60)

		self.setup_ui()
		self.connect_ui()
		self.set_stylesheet()

	def setup_ui(self):
		self.check_layout.addStretch()
		self.check_layout.addWidget(self.check_button)
		self.check_layout.addStretch()

		self.main_layout.addLayout(self.logo_layout)
		self.main_layout.addWidget(self.about_text)
		self.main_layout.addLayout(self.check_layout)

	def connect_ui(self):
		self.check_button.clicked.connect(self.close)

	def set_stylesheet(self):
		self.setStyleSheet('''
							font: 75 9pt "Sitka Small";
							''')


class ProjectSetUI(QtWidgets.QDialog):
	def __init__(self):
		super(ProjectSetUI, self).__init__()
		self.setWindowTitle('Library_Setting')
		self.setMinimumSize(750, 500)
		self.setMaximumSize(750, 500)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
		self.main_layout = QtWidgets.QVBoxLayout(self)

		self.close_layout = QtWidgets.QHBoxLayout()
		self.close_button = QtWidgets.QPushButton('close')

		self.text_layout = QtWidgets.QHBoxLayout()
		self.main_text = QtWidgets.QLabel('Setting')
		self.main_text.setStyleSheet('''font: 20pt "Sitka Small"''')

		self.version_layout = QtWidgets.QHBoxLayout()
		self.version_label = QtWidgets.QLabel('Library Version')
		self.version_label.setMinimumHeight(120)
		self.version_label_a = QtWidgets.QLabel('1.0.0')

		self.set_project_layout = QtWidgets.QHBoxLayout()
		self.set_project_label = QtWidgets.QLabel('Local Library_Path:')
		self.set_project_label.setMinimumHeight(120)
		self.set_project_line = QtWidgets.QLineEdit()
		self.set_project_button = QtWidgets.QPushButton()

		self.check_layout = QtWidgets.QHBoxLayout()
		self.check_button = QtWidgets.QPushButton('SAVE CHANGES')
		self.check_button.setStyleSheet('''
											border: 0px solid black;
											border-radius: 6px;
										''')

		self.setup_ui()
		self.connect_ui()
		self.set_stylesheet()

	def setup_ui(self):
		self.close_layout.addStretch()
		self.close_layout.addWidget(self.close_button)

		self.text_layout.addStretch()
		self.text_layout.addWidget(self.main_text)
		self.text_layout.addStretch()

		self.version_layout.addWidget(self.version_label)
		self.version_layout.addWidget(self.version_label_a)

		self.set_project_layout.addWidget(self.set_project_label)
		self.set_project_layout.addWidget(self.set_project_line)
		self.set_project_layout.addWidget(self.set_project_button)

		self.check_layout.addStretch()
		self.check_layout.addWidget(self.check_button)

		self.main_layout.addLayout(self.close_layout)
		self.main_layout.addLayout(self.text_layout)
		self.main_layout.addLayout(self.version_layout)
		self.main_layout.addLayout(self.set_project_layout)
		self.main_layout.addLayout(self.check_layout)
		self.main_layout.addStretch()

	def connect_ui(self):
		self.close_button.clicked.connect(self.close)
		self.check_button.clicked.connect(self.check_foo)

	def check_foo(self):
		self.close()

	def set_stylesheet(self):
		self.setStyleSheet('''
							font: 75 9pt "Sitka Small";
							''')


if __name__ == '__main__':
	library = LibraryWindow()
	library.show()

