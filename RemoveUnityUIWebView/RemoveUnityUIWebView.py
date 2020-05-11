# -*- coding:utf-8 -*-

# https://github.com/iOSCoda/PythonToolBox
# author QQ 2108336019

import os
import shutil

parPath = os.path.dirname(os.path.abspath(__file__))

kArchesList = ["armv7", "arm64", "armv7s"]

kLibName = "libiPhone-lib.a"

# 生成新的.a的名字
kNewLibName = "libiPhone-lib-new.a"


def colorPrint(string):
    print("\033[0;33;m%s\033[0m" % (str(string)))


# 获取libiPhone-lib.a路径
def get_libiPhone_libPath():
    staticLibPath = os.path.join(parPath, kLibName)
    if not os.path.exists(staticLibPath):
        print("请将需要处理的libiPhone-lib.a放入该脚本同级目录")
        os._exit(0)
    return staticLibPath


# 获取当前所有架构
def getCurArches():
    command = "lipo -info %s" % (get_libiPhone_libPath())
    output = os.popen(command)
    content = output.readline()
    output.close()
    for item in kArchesList[:]:
        if item not in content:
            kArchesList.remove(item)
    return kArchesList


# 获取URLUtility.mm路径
def getURLUtilityPath():
    URLUtilityPath = os.path.join(parPath, "URLUtility.mm")
    if not os.path.exists(URLUtilityPath):
        colorPrint(URLUtilityPath)
        colorPrint("不存在")
        os._exit(0)
    return URLUtilityPath


# 获取不同架构对应的文件夹
def getArchTmpPath(arch):
    archTmpPath = os.path.join(parPath, arch)
    if not os.path.isdir(archTmpPath):
        os.mkdir(archTmpPath)
    return archTmpPath


# 获取不同架构对应的URLUtility.o路径
def getArchURLUtilityOPath(type):
    archPath = getArchTmpPath(type)
    archOPath = os.path.join(archPath, "URLUtility.o")
    return archOPath


# 获取不同架构对应的.a路径
def getTargetLibPath(arch):
    targetArchPath = getArchTmpPath(arch)
    libName = "libiPhone-lib_" + arch + ".a"
    targetLibPath = os.path.join(targetArchPath, libName)
    return targetLibPath


# 获取不同架构对应的URLUtility.o
def createURLUtilityO(arch, URLUtilityOPath):
    colorPrint("")
    colorPrint("----------开始生成%s URLUtility.o" % (arch))
    URLUtilityPath = getURLUtilityPath()
    command = (
        "clang -c %s -arch %s -isysroot /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk -o %s"
        % (URLUtilityPath, arch, URLUtilityOPath)
    )
    os.system(command)
    colorPrint("----------结束生成%s URLUtility.o" % (arch))


# 切割框架
def splitArches(arch, archList, targetArchPath):
    libName = os.path.basename(targetArchPath)
    colorPrint("----------开始生成:%s" % (libName))
    libiPhone_libPath = get_libiPhone_libPath()
    if len(archList) > 1:
        os.system("lipo %s -thin %s -output %s" % (libiPhone_libPath, arch, targetArchPath))
    else:
        shutil.copy(libiPhone_libPath, targetArchPath)
    colorPrint("----------结束生成:%s" % (libName))


# 移除URLUtility.o 并且插入新的URLUtility.o
def deleteAndInsert(arch):
    libPath = getTargetLibPath(arch)
    oObjetPath = getArchURLUtilityOPath(arch)

    colorPrint("----------移除旧的URLUtility.o")
    os.system("ar -d %s URLUtility.o" % (libPath))

    colorPrint("----------插入新的URLUtility.o")
    command = "ar -q %s %s" % (libPath, oObjetPath)
    os.system(command)


# 合并更新后的.a
def mergeLib(archList, archPath):
    outputLibPath = os.path.join(parPath, kNewLibName)
    if len(archList) > 1:
        command = "lipo -create %s -output %s " % (archPath, outputLibPath)
        os.system(command)
    else:
        archPath = archPath.strip()
        shutil.copy(archPath, outputLibPath)
    colorPrint("")
    colorPrint("----------生成的新的libiPhone为:")
    colorPrint(outputLibPath)


if __name__ == "__main__":

    # 获取当前所有的框架
    archList = getCurArches()
    colorPrint("当前所有架构:")
    colorPrint(str(archList))

    archesString = ""
    for arch in archList:
        # 获取不同框架URLUtility.O的路径
        URLUtilityOPath = getArchURLUtilityOPath(arch)

        # 生成不同框架的URLUtility.O
        createURLUtilityO(arch, URLUtilityOPath)

        # 获取armvx.a的路径
        targetLibPath = getTargetLibPath(arch)

        # 生成对应的armvx.a
        splitArches(arch, archList, targetLibPath)

        # 删除原本的URLUtility.O,插入上面生成的URLUtility.O
        deleteAndInsert(arch)

        # 拼接需要合并的armvx.a路径
        archesString += targetLibPath + " "

    # 生成新的多框架二进制
    mergeLib(archList, archesString)

    # 清理临时文件
    for arch in archList:
        archPath = getArchTmpPath(arch)
        shutil.rmtree(archPath)
