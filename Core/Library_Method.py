# _*_ coding:utf-8 _*_ #
# @Time     :2019/12/25 16:31
# @Author   :Fighter
# @Software :Heater
# @E-mail    :317431629@qq.com

import pymel.core as pm


class LibraryFoo(object):
	def __init__(self):
		super(LibraryFoo, self).__init__()
		print u'加载方法'

	@staticmethod
	def import_file(path):
		pm.importFile(path)
		print(u'导入成功')

	def publish_to_library(self):
		pass


