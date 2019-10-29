# -*- coding:utf-8 -*-

import os
import sys

toolPath = os.path.join(os.getcwd(), "lib")
sys.path.append(toolPath)

try:
    import xcodeproj
except Exception as exception:
	print(exception)

if __name__ == "__main__":
    xcodeproj.inputPath()

