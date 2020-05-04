# -*- coding:utf-8 -*-

import os
import shutil

parPath = os.path.dirname(os.path.abspath(__file__))

kArchesList = ["armv7","arm64","armv7s"]

kLibName = "libiPhone-lib.a"

# 生成新的.a的名字
kNewLibName = "libiPhone-lib-new.a"


def colorPrint(string):
	print("\033[0;33;m%s\033[0m" % (str(string)))



# 获取libiPhone-lib.a路径
def get_libiPhone_lib():
	staticLibPath = os.path.join(parPath,kLibName)
	if not os.path.exists(staticLibPath):
		print("请将需要处理的libiPhone-lib.a放入文件夹")
		os._exit(0)
	return staticLibPath


# 获取当前所有架构
def getCurArches():
	output = os.popen("lipo -info %s" %(get_libiPhone_lib()))
	content = output.readline()
	output.close()
	for item in kArchesList[:]:
		if item not in content:
			kArchesList.remove(item)
	return kArchesList


# 获取URLUtility.mm路径
def getURLUtilityPath():
	URLUtilityPath = os.path.join(parPath,"URLUtility.mm")
	return URLUtilityPath


# 获取不同架构对应的文件夹
def getArchPath(arch):
	tmpArchPath = os.path.join(parPath,arch)
	if not os.path.isdir(tmpArchPath):
		os.mkdir(tmpArchPath)
	return tmpArchPath


# 获取不同架构对应的URLUtility.o路径
def getArchURLUtilityOPath(type):
	archPath = getArchPath(type)
	archOPath = os.path.join(archPath,"URLUtility.o")
	return archOPath


# 获取不同架构对应的.a路径
def getTargetLibPath(arch):
	targetFolderPath  = getArchPath(arch)
	libName = "libiPhone-lib_" + arch + ".a"
	targetLibPath = os.path.join(targetFolderPath,libName)
	return targetLibPath


# 获取不同架构对应的URLUtility.o
def createURLUtility(arch,URLUtilityOPath):
	colorPrint("")
	colorPrint("----------开始生成%s URLUtility.o" %(arch))
	URLUtilityPath = getURLUtilityPath()
	command = "clang -c %s -arch %s -isysroot /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk -o %s" %(URLUtilityPath,arch,URLUtilityOPath)
	os.system(command)
	colorPrint("----------结束生成%s URLUtility.o" %(arch))


# 切割框架
def splitArches(arch,targetFolder):
	libName = os.path.basename(targetFolder)
	colorPrint("----------开始生成:%s" %(libName))
	os.system("lipo libiPhone-lib.a -thin %s -output %s" %(arch,targetFolder))
	colorPrint("----------结束生成:%s" %(libName))


# 移除URLUtility.o 并且插入新的URLUtility.o
def deleteAndInsert(arch):
	libPath = getTargetLibPath(arch)
	oObjetPath = getArchURLUtilityOPath(arch)

	colorPrint("----------移除旧的URLUtility.o")
	os.system("ar -d %s URLUtility.o" %(libPath))

	colorPrint("----------插入新的URLUtility.o")
	os.system("ar -q %s %s" %(libPath,oObjetPath))


# 合并更新后的.a
def mergeLib(archPath):
	outputLibPath = os.path.join(parPath,kNewLibName)
	command = "lipo -create %s -output %s " %(archPath,outputLibPath)
	os.system(command)
	colorPrint("")
	colorPrint("----------生成的新的libiPhone为:")
	colorPrint(outputLibPath)




if __name__ == "__main__":
	archList = getCurArches()

	colorPrint("当前所有架构:")
	colorPrint(str(archList))
	archesString = ""
	for arch in archList:
		URLUtilityOPath = getArchURLUtilityOPath(arch)
		createURLUtility(arch,URLUtilityOPath)
		targetLibPath = getTargetLibPath(arch)
		splitArches(arch,targetLibPath)
		deleteAndInsert(arch)
		archesString += targetLibPath + " "
	mergeLib(archesString)


	for arch in archList:
		archPath = getArchPath(arch)
		shutil.rmtree(archPath)