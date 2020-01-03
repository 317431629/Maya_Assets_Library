# _*_ coding:utf-8 _*_ #
# @Time     :2019/12/26 13:33
# @Author   :Fighter
# @Software :Maya
# @E-mail    :317431629@qq.com
import pymel.core as pm
from Core import Library_UI
from Core import Library_Method
import os
import sys
from shutil import rmtree

reload(Library_UI)
reload(Library_Method)


class LibraryTool(Library_UI.LibraryWindow):
	def __init__(self, method):
		super(LibraryTool, self).__init__()
		self.method = method
		self.library_path = "{}/Library".format(sys.path[-1])

	def connect_ui(self):
		super(LibraryTool, self).connect_ui()
		self.refresh_button.clicked.connect(self.refresh_list)
		self.remove_button.clicked.connect(self.remove_assets)
		self.import_button.clicked.connect(self.import_file)

	# ____________Refresh list__________________#
	def refresh_list(self):
		self.database.initialization_data()
		self.type_combobox.clear()
		for assets_type in self.database.get_type():
			self.type_combobox.addItem(assets_type[0])

	# ____________Remove Mod____________________#
	def remove_assets(self):
		assets_name = self.assets_data[0]
		assets_path = self.assets_data[2]
		self.database.delete_data(assets_name)
		print(u'已移出数据库')

		self.remove_form_list()
		self.del_assets_from_lib(assets_path)
		print(u"已移除出库！")

	def remove_form_list(self):
		index = self.list_view.currentIndex().row()
		item_model = self.list_view.model()
		item_model.removeRow(index)

	@staticmethod
	def del_assets_from_lib(path):
		dir_path = os.path.split(path)[0]
		rmtree(dir_path)
		type_path = os.path.dirname(dir_path)
		if not os.listdir(type_path):
			os.removedirs(type_path)

	# _________________Copy Maya Source images_____________________#
	def import_file(self):
		assets_path = self.assets_data[2]
		pm.importFile(assets_path)

	def closeEvent(self, event):
		self.database.remove_data()
		self.close()


if __name__ == '__main__':
	library = LibraryTool(Library_Method.LibraryFoo())
	library.show()
