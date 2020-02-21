import os, sys, random
""" 
收集某路径下的所有py文件; 从这些文件中解析出所有定义的类; 构造它们的继承关系
以可视化,可交互的方式显示出这些类继承树

碰上包名,模块名的暂时都忽略掉, 只留下类名, 所以碰上同名类会有差错可能
暂时不分析[嵌套类, 同名类]. 所以碰上这些情况结果可能会有差错
"""
import pygame


class Cls:
	""" 类对象 """
	clsList = []  #所有定义的类
	clsOut = ""  #输出的内容

	def __init__(self):
		self.clsName = ""  #类名
		self.clsFile = ""  #类所在文件
		self.clsParent = []  #父类集
		self.clsChilds = []  #子类集
		self.rect = pygame.Rect(0, 0, 50, 20)

	@staticmethod
	def parse(filename):
		""" 解析文件 """
		if not os.path.exists(filename): return
		f = open(filename, "rb")
		str = f.read()
		f.close()

		def clearClsName(clsname):
			""" 剥去包名,模块名 只留下类名 """
			idx = clsname.rfind(b".")
			if idx > 0: clsname = clsname[idx + 1:]
			return clsname.strip()

		lines = str.splitlines()
		for line in lines:
			l = line.strip()
			if not l.startswith(b"class ") or not l.endswith(b":"): continue
			if l.find(b"{") > 0: continue
			l = l[6:]
			l = l.replace(b" ", b"")
			pl = l.find(b"(")

			cls = Cls()
			Cls.clsList.append(cls)
			if pl < 0:  #无(), 没有父类
				cls.clsName = clearClsName(l[0:-1])
				cls.clsFile = filename
			else:  #分析父类集
				cls.clsName = clearClsName(l[0:pl])
				cls.clsFile = filename
				ll = l[pl + 1:-2]
				if len(ll) < 1: continue  #空(), 没有父类
				plist = ll.split(b",")
				for i in plist:
					cls.clsParent.append(clearClsName(i))

	@staticmethod
	def showClsList():
		""" 显示类集 """
		for item in Cls.clsList:
			print(item.clsName, item.clsParent, "--", item.clsFile)

	@staticmethod
	def showClsTree():
		""" 显示类继承树 """
		print("all class num:", len(Cls.clsList))
		Cls._toClsTree()
		for item in Cls.clsList:
			if len(item.clsParent) > 0: continue
			Cls._showTree(item)
		f = open("cls.txt", "wt")
		f.write(Cls.clsOut)
		f.close()

	@staticmethod
	def getClsList(pathname, tabs=""):
		""" 收集文件 """
		allitem = [pathname + "/" + item for item in os.listdir(pathname)]
		for item in allitem:
			filename = os.path.basename(item)
			if os.path.isdir(item):
				# print(tabs, "[" + filename + "]")
				Cls.getClsList(item, tabs + "\t")
			elif os.path.isfile(item) and filename.endswith(".py"):
				# print(tabs, filename)
				Cls.parse(item)

	@staticmethod
	def _showTree(item, tabs=""):
		""" 显示子树 """
		# print(tabs, str(item.clsName), "\t\t", item.clsFile)
		# print("%s %s \t\t %s" % (tabs, item.clsName, item.clsFile))
		out = "{p1:50} file:///{p2}\n".format(p1=tabs + str(item.clsName), p2=item.clsFile)
		Cls.clsOut += out
		for c in item.clsChilds:
			Cls._showTree(c, tabs + "\t")

	@staticmethod
	def _toClsTree():
		""" 转换成类继承树 """
		# 收集根对象
		for item in Cls.clsList:
			for clsname in item.clsParent:
				parentCls = Cls._getClsbyName(clsname)
				if parentCls is None:
					parentCls = Cls()
					Cls.clsList.append(parentCls)
					parentCls.clsName = clsname
				parentCls.clsChilds.append(item)
		# 排序
		def getKey(item):
			return item.clsName

		Cls.clsList.sort(key=getKey)
		for item in Cls.clsList:
			item.clsChilds.sort(key=getKey)

	@staticmethod
	def _getClsbyName(clsname):
		""" 根据类名获取实例 """
		for item in Cls.clsList:
			if item.clsName == clsname: return item
		return None


if __name__ == "__main__":

	# Cls.getClsList("d:/projectcpp/testPython/battle_city")
	Cls.getClsList("d:/projectCpp/gameLib/panda3d/ursina-master/ursina")
	# Cls.getClsList("d:/projectCpp/gameLib/panda3d/panda3d-master/direct/src")

	# Cls.parse("D:/projectCpp/gameLib/panda3d/panda3d-master/direct/src/showbase/Factory.py")

	# Cls.showClsList()
	Cls.showClsTree()