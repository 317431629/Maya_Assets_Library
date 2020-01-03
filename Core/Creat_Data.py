# _*_ coding:utf-8 _*_ #
# @Time     :2019/12/23 13:49
# @Author   :Fighter
# @Software :Heater
# @E-mail    :317431629@qq.com

import sqlite3
import os
import sys


class DataBase(object):
	def __init__(self, data_path):
		super(DataBase, self).__init__()
		self.data_path = data_path
		self.library_path = "{}/Library".format(sys.path[-1])
		self.conn = sqlite3.connect(self.data_path)
		self.cursor = self.conn.cursor()
		self.cursor.execute("create table if not exists assets(assets_name,assets_type, assets_path,assets_image)")
		self.initialization_data()

	def initialization_data(self):
		for mode in os.listdir(self.library_path):
			for assets in os.listdir(os.path.join(self.library_path, mode)):
				assets_name = "{}.ma".format(assets)
				assets_type = mode
				assets_path = os.path.join(self.library_path, mode, assets, assets_name)
				assets_image = os.path.join(self.library_path, mode, assets, "{}.png".format(assets))
				self.insert_data(assets_name, assets_type, assets_path, assets_image)

	def get_sel_data(self, assets_name):
		self.cursor.execute("SELECT * FROM assets WHERE assets_name == '{}'".format(assets_name))
		return self.cursor.fetchone()

	def get_type_data(self, assets_type):
		self.cursor.execute("SELECT * FROM assets WHERE assets_type = '{}'".format(assets_type))
		return self.cursor.fetchall()

	def get_filter_data(self, assets_type, assets_filter):
		self.cursor.execute("SELECT * FROM assets WHERE assets_type = '{}' AND assets_name LIKE '{}'".format(assets_type, assets_filter))
		return self.cursor.fetchall()

	def get_all_data(self):
		self.cursor.execute("SELECT * FROM assets")
		return self.cursor.fetchall()

	def insert_data(self, assets_name, assets_type, assets_path, assets_image):
		self.cursor.execute("SELECT * FROM assets WHERE assets_name = '{}'".format(assets_name))
		if self.cursor.fetchone():
			pass
		else:
			self.cursor.execute("INSERT INTO assets (assets_name, assets_type, assets_path, assets_image) VALUES ('{}', '{}','{}','{}')".format(assets_name, assets_type, assets_path, assets_image))
		self.conn.commit()

	def delete_data(self, assets_name):
		self.cursor.execute("DELETE FROM assets WHERE assets_name = '{}'".format(assets_name))
		self.conn.commit()

	def get_type(self):
		self.cursor.execute("SELECT DISTINCT assets_type FROM assets")
		return self.cursor.fetchall()

	def remove_data(self):
		self.cursor.execute('drop table assets')
		self.conn.commit()
		self.conn.close()
		os.remove("{}/Data/data.db".format(sys.path[-1]))


if __name__ == '__main__':
	data = DataBase('F:/Project/Python_Project/Maya_Assets_Library/Data/data.db')
	print data.get_all_data()
	data.remove_data()

