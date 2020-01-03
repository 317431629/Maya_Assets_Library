# _*_ coding:utf-8 _*_ #
# @Time     :2019/12/31 17:22
# @Author   :Fighter
# @Software :Heater
# @E-mail    :317431629@qq.com
from PySide2 import QtWidgets
from PySide2 import QtGui
import shutil
import os
import pymel.core as pm
import sys
import json
from Core import Publish_UI
reload(Publish_UI)


class PublishFoo(Publish_UI.PublishUI):
	def __init__(self):
		super(PublishFoo, self).__init__()
		self.data_path = os.path.join(sys.path[-1], 'Data', "Shader_type.json")
		with open(self.data_path, "r") as f:
			self.image_type = json.loads(f.read())
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
		assets_path = os.path.join(
									self.library_path, assets_type, assets_name,
									"{}.ma".format(assets_name)
									).replace('\\', '/')
		assets_image = os.path.join(
									self.library_path, assets_type, assets_name,
									"{}.png".format(assets_name)
									).replace('\\', '/')
		return assets_name, assets_type, assets_path, assets_image

	@staticmethod
	def save_file(path):
		if os.path.exists(os.path.split(path)[0]):
			pass
		else:
			os.makedirs(os.path.split(path)[0])
		pm.saveAs(path)
		print(u'文件另存为：{}'.format(path))

	def get_maya_image(self):
		assets_name, assets_type, assets_path, assets_image = self.get_assets_data()
		texture = pm.ls(textures=True)
		for i in texture:
			image_attr = pm.PyNode("{}.{}".format(i, self.image_type[str(type(i))]))
			image_path, image_name = os.path.split(image_attr.get())
			source_image_path = os.path.join(self.library_path, assets_type, assets_name, 'Sourceimages')
			image_attr.set(os.path.join(source_image_path, image_name))
			self.copy_source_image(image_name, image_path, source_image_path)

	@staticmethod
	def copy_source_image(image_name, image_path, source_image_path):
		if os.path.exists(source_image_path):
			pass
		else:
			os.makedirs(source_image_path)
		udim_images = [
						udim_name for udim_name in os.listdir(image_path)
						if image_name.split("<UDIM>")[0] in udim_name and "<UDIM>" in image_name
					]
		if udim_images:
			for i in udim_images:
				shutil.copy2(os.path.join(image_path, i), os.path.join(source_image_path, i))
		else:
			shutil.copy2(os.path.join(image_path, image_name), os.path.join(source_image_path, image_name))

	# _________import Mod_______________________#

	def publish_to_library(self):
		assets_name, assets_type, assets_path, assets_image = self.get_assets_data()
		# # ________________copy to library____________________________________________#

		self.get_maya_image()  # 拷贝贴图文件

		self.save_file(assets_path)  # 文件另存为

		shutil.copy2(self.assets_image_line.text(), assets_image)  # 拷贝预览图片

		QtWidgets.QMessageBox.information(self, '', 'You have successfully published your package', QtWidgets.QMessageBox.Yes)
		self.close()


if __name__ == '__main__':
	library = PublishFoo()
	library.show()
