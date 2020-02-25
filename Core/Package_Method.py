# _*_ coding:utf-8 _*_ #
# @Time     :2020/2/19 9:18
# @Author   :Fighter
# @Software :Heater
# @E-mail    :317431629@qq.com
import pymel.core as pm
import os
import shutil
import json
import sys


class Package(object):
	def __init__(self):
		self.data_path = os.path.join(sys.path[-1], 'Data', "Shader_type.json")
		with open(self.data_path, "r") as f:
			self.image_type = json.loads(f.read())
		self.rs_proxy = pm.ls(type='RedshiftProxyMesh')
		self.ar_proxy = pm.ls(type='aiStandIn')
		self.textures = pm.ls(textures=True)

	def get_all_texture(self, target_path):
		"""
		获取贴图并设置新的贴图路径
		:param target_path:  目标路径
		"""
		texture_data = {}
		texture_target_path = os.path.join(target_path, "Sourceimage")  # todo: 后期看是否需要加上文件名
		for texture in self.textures:
			image_attr = self.image_type[str(type(texture))]
			texture_path, texture_name = os.path.split(texture.getAttr(image_attr))
			texture.setAttr(image_attr, os.path.join(texture_target_path, texture_name))

			texture_data.setdefault(texture_path.replace('//', '/'), []).append(texture_name)
		return texture_data

	def copy_texture(self, target_path):
		"""
		拷贝贴图
		:param target_path:  目标路径
		"""
		texture_target_path = os.path.join(target_path, "Sourceimage")  # todo: 后期看是否需要加上文件名
		if not os.path.exists(texture_target_path):
			os.makedirs(texture_target_path)
		texture_data = self.get_all_texture(texture_target_path)
		for texture_path in texture_data:
			for texture in os.listdir(texture_path):
				old_name = os.path.join(texture_path, texture).replace("\\", "/")
				new_name = os.path.join(texture_target_path, texture).replace("\\", "/")
				try:
					shutil.copy2(old_name, new_name)
				except IOError:
					print "检查{}是否为文件".format(os.path.join(texture_path, texture))

	def get_all_proxy(self):
		"""
		获取代理路径
		:return: redshift 代理路径 ， Arnold代理路径
		"""
		rs_proxy_paths = []
		ar_proxy_paths = []
		if self.rs_proxy:
			rs_proxy_paths = list(set([proxy.getAttr('fileName') for proxy in self.rs_proxy]))
		if self.ar_proxy:
			ar_proxy_paths = list(set([proxy.getAttr('dso') for proxy in self.ar_proxy]))
		return rs_proxy_paths + ar_proxy_paths

	@staticmethod
	def set_proxy_path(proxy, proxy_name, new_proxy_path):
		if '.ass' in proxy_name:
			proxy.setAttr('dso', new_proxy_path)
		elif '.rs' in proxy_name:
			proxy.setAttr('fileName', new_proxy_path)

	def copy_proxy(self, target_path):
		"""
		拷贝代理到指定路径 并设置新的代理路径
		"""
		proxy_paths = self.get_all_proxy()
		proxy_target_path = os.path.join(target_path, "Proxy")
		if not os.path.exists(proxy_target_path):
			os.makedirs(proxy_target_path)
		for proxy in proxy_paths:
			proxy_name = os.path.split(proxy)[-1]
			new_proxy_path = os.path.join(proxy_target_path, proxy_name)
			self.set_proxy_path(proxy, proxy_name, new_proxy_path)
			shutil.copy2(proxy, new_proxy_path)

	@staticmethod
	def save_file(target_path):
		filepath = pm.sceneName()
		filename = os.path.basename(filepath)
		pm.saveAs(os.path.join(target_path, filename))


if __name__ == '__main__':
	package = Package()
	package.copy_texture("E:/Test")
