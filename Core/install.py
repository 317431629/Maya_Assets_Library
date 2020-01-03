# _*_ coding:utf-8 _*_ #
# @Time     :2019/12/30 11:14
# @Author   :Fighter
# @Software :Maya
# @E-mail    :317431629@qq.com
import pymel.core as pm
import os
import json
import sys


class Install(object):
	def __init__(self, library_path):
		super(Install, self).__init__()
		self.project_path = library_path
		self.core_path = "{}/Core".format(self.project_path)
		self.icon_path = "{}/Icon".format(self.project_path)
		self.library_path = "{}/Library".format(self.project_path)
		self.script_path = "{}/Script".format(self.project_path)
		self.data_path = "{}/Data".format(self.project_path)
		# self.write_data()
		if not pm.shelfLayout('Assets_Library', exists=True):
			print u'创建', self.project_path, self.core_path
			self.shelf_name = self.creat_shelf()
			self.command_A, self.command_B = self.creat_command()
			print self.command_A, self.command_B
			self.creat_shelf_button('Logo', self.command_A, self.shelf_name)
			self.creat_shelf_button('Publish', self.command_B, self.shelf_name)
		else:
			print u'已存在'

	def write_data(self):
		data_path = {
						"project_path": self.project_path, "core_path": self.core_path,
						"icon_path": self.icon_path, "library_path": self.library_path,
						"script_path": self.script_path, "data_path": self.data_path
					}
		with open(os.path.join(self.data_path, 'Project_Setting.json'), 'w') as f:
			json.dump(data_path, f)

	def creat_shelf(self):
		self.shelf = pm.mel.eval('''addNewShelfTab "Assets_Library";''')
		shelf_name = pm.shelfLayout('Assets_Library', q=True, fullPathName=True)
		return shelf_name

	def creat_shelf_button(self, image, command, parent):
		pm.shelfButton(annotation='', image="{}/Icon/{}.png".format(self.project_path, image), command=command, parent=parent)

	def creat_command(self):
		command_import = "import sys\nif '{}' not in sys.path:\n\tsys.path.append('{}')".format(self.project_path, self.project_path)
		command_A = command_import + "\nexecfile('{}/Maya_Assets_Library_Tool.py')".format(self.core_path)
		command_B = command_import + "\nexecfile('{}/Publish_Method.py')".format(self.core_path)
		return command_A, command_B

