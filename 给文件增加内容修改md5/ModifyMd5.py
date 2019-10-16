# -*- coding: UTF-8 -*-

import os
import hashlib
import sys

# 需要处理的文件类型
fileType = [".h", ".m", ".mm"]

# 需要在文件中追加的内容
appendContent = "\n"


if sys.version_info[0] < 3:
    print("请确认在python3环境运行该脚本")
    os._exit(1)


def fileMd5(file, blockSize=2**20):
    hash = hashlib.md5()
    with open(file, "rb") as f:
        while True:
            b = f.read(blockSize)
            if not b:
                break
            hash.update(b)
        return hash.hexdigest()


# 获取文件后缀(包含.,例如1.png返回.png)
def getFileSuffix(filePath):
    return os.path.splitext(filePath)[-1]


def modifyFile(filePath):
    # 判断文件后缀是否符合要求
    if getFileSuffix(filePath) not in fileType:
        return
    print(filePath)
    oldMd5 = fileMd5(filePath)
    try:
        with open(filePath, "a+") as f:
            # 写入需要追加的内容
            f.write(appendContent)
        print("md5 " + oldMd5 + " 修改为: " + fileMd5(filePath))
    except ValueError:
        pass


def modify(filePath):
    # 处理文件
    if os.path.isfile(filePath):
        print("处理文件:")
        modifyFile(filePath)
    # 处理文件夹
    elif os.path.isdir(filePath):
        print("处理文件夹:")
        for root, dirs, files in os.walk(filePath, topdown=False):
            # 过滤隐藏文件/文件夹
            files = [f for f in files if not f[0] == '.']
            for file in files:
                fullPath = os.path.join(root, file)
                modifyFile(fullPath)


# 输入需要处理的文件夹或者文件
def inputDir():
    dirPath = input("请输入需要处理的文件夹路径或者文件路径:\n")
    dirPath = dirPath.rstrip()
    while not os.path.exists(dirPath):
        dirPath = input("请输入需要处理的文件夹路径或者文件路径:\n")
        dirPath = dirPath.rstrip()
    modify(dirPath)


if __name__ == "__main__":
    inputDir()