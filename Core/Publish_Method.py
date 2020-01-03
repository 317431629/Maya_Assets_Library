# _*_ coding:utf-8 _*_ #
# @Time     :2019/12/31 17:22
# @Author   :Fighter
# @Software :Heater
# @E-mail    :317431629@qq.com
from Core import Publish_UI
reload(Publish_UI)
from PySide2 import QtWidgets
from PySide2 import QtGui
import shutil
import os
import pymel.core as pm
import sys


class PublishFoo(Publish_UI.PublishUI):
	def __init__(self):
		super(PublishFoo, self).__init__()
		self.image_type = ['file', 'RedshiftSprite', 'RedshiftNormalMap']
		self.library_path = "{}/Library".format(sys.path[-1])
		self.connect_ui()

	def connect_ui(self):
		self.publish_button.clicked.connect(self.publish_to_library)
		self.assets_image_button.clicked.connect(self.set_preview_image)

	def set_preview_image(self):
		image_path = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", "", "All Files (*.png);")[0]
		self.assets_image_line.setText(image_path)
		pix_map = QtGui.QPixmap(image_path)
		self.show_list_label.setPixmap(pix_map)
		self.set_preview_data()

	def get_assets_data(self):
		assets_name = self.assets_name_line.text()
		assets_type = self.assets_type_line.text()
		assets_path = os.path.join(self.library_path, assets_type, assets_name, "{}.ma".format(assets_name)).replace('\\', '/')
		assets_image = os.path.join(self.library_path, assets_type, assets_name, "{}.png".format(assets_name)).replace('\\', '/')
		return assets_name, assets_type, assets_path, assets_image

	@staticmethod
	def save_file(path):
		if os.path.exists(os.path.split(path)[0]):
			pass
		else:
			os.makedirs(os.path.split(path)[0])
		pm.saveAs(path)
		print(u'文件另存为：{}'.format(path))

	def get_maya_image(self, image_type):  # todo: 优化下这个函数
		assets_name, assets_type, assets_path, assets_image = self.get_assets_data()
		if image_type == 'file':
			image_nodes = pm.ls(type=image_type)
			for image_node in image_nodes:
				image_path = image_node.fileTextureName.get()
				image_name = os.path.split(image_path)[-1]
				source_image_path = os.path.join(self.library_path, assets_type, assets_name, 'Sourceimages')
				new_image_name = os.path.join(source_image_path, image_name)
				self.copy_source_image(image_path, new_image_name)
				image_node.fileTextureName.set(new_image_name)
		else:
			image_nodes = pm.ls(type=image_type)
			for image_node in image_nodes:
				image_path = image_node.tex0.get()
				image_name = os.path.split(image_path)[-1]
				source_image_path = os.path.join(self.library_path, assets_type, assets_name, 'Sourceimages')
				new_image_name = os.path.join(source_image_path, image_name)
				self.copy_source_image(image_path, new_image_name)
				image_node.tex0.set(new_image_name)

	@staticmethod
	def copy_source_image(image_path, new_image_path):
		source_image_path = os.path.split(new_image_path)[0]
		if os.path.exists(source_image_path):
			pass
		else:
			os.makedirs(source_image_path)
		shutil.copy2(image_path, new_image_path)
	# _________import Mod_______________________#

	def publish_to_library(self):
		assets_name, assets_type, assets_path, assets_image = self.get_assets_data()
		# # ________________copy to library____________________________________________#

		for image_type in self.image_type:
			self.get_maya_image(image_type)  # 拷贝贴图文件

		self.save_file(assets_path)  # 文件另存为

		shutil.copy2(self.assets_image_line.text(), assets_image)  # 拷贝预览图片

		QtWidgets.QMessageBox.information(self, '', 'You have successfully published your package', QtWidgets.QMessageBox.Yes)
		self.close()


if __name__ == '__main__':
	library = PublishFoo()
	library.show()
