
def getReplaceString(aStr):
    aList = list(aStr)
    newString = ""
    for index, item in enumerate(aList):
        if index == 0:
            newString += "[@["
        # 替换的时候需要引号
        newString += "@\"" + item + "\","
        if index == len(aList) - 1:
            newString = newString.rstrip(",")
            newString += "] componentsJoinedByString:@\"\"]"
    print(newString)



def inputString():
    while(True):
        str = input("\n请输入需要拆分的字符串:\n")
        getReplaceString(str)

inputString()