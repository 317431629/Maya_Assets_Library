# _*_ coding:utf-8 _*_ #
# @Time     :2020/1/2 9:41
# @Author   :Fighter
# @Software :Heater
# @E-mail    :317431629@qq.com
import pymel.core as pm


class CheckUp(object):
	def __init__(self):
		super(CheckUp, self).__init__()
		pass

	def check_outline(self):
		ifRight = 0
		self.theCountOfParentDag = 0
        for one in pm.ls(dag=True,type='transform',l=True):
            if not 'persp' in one and not 'top' in one and not 'front' in one and not 'side' in one:
                if len([oneStr for oneStr in one if '|' in oneStr])==1:
					self.theCountOfParentDag+=1
        if self.theCountOfParentDag > 10:
            self.theValueUP(1, 10, u'大纲顶层分组超过10个，可能有些凌乱\n')
            ifRight = 1
        if ifRight == 0:
            self.theValueUP(1, 0, self.No)

	def check_texture(self):
		'''
		检查贴图是否有丢失
		:return:
		'''
		pass

	def check_plugin(self):
		'''
		检查时候有不识别的插件
		:return:
		'''
		pass

	def check_history(self):
		'''
		检查是否存在历史
		:return:
		'''
		pass

	def checkFaceMaterial(self):
		ifRight = 0
		self.theAllObj = []
		for one in pm.ls(type='shadingEngine', l=True):
			if 'initialShadingGroup' not in one and 'initialParticleSE' not in one:
				getTheMesh = pm.listConnections(one +'.memberWireframeColor')
				if getTheMesh != None:
					for oneMesh in getTheMesh:
						if not oneMesh in self.theAllObj:
							print (1, 29, u'以面给材质的物体：【'+oneMesh+u'】\n')
							ifRight = 1
		if ifRight == 0:
			self.theValueUP(1, 0, self.No)


if __name__ == '__main__':
	checkup = CheckUp()
	checkup.checkFaceMaterial()