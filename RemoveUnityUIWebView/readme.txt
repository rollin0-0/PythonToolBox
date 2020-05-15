使用前请确认本机Xcode SDKs所在路径,确认包含以下路径:
/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk

如果不是这个路径:
请将RemoveUnityUIWebView.py中的83行中以上路径改成本机Xcode SDKs所在路径(出现这个问题一般因为本机安装了多个Xcode)


1. 将需要移除UIWebView的libiPhone-lib.a放入该文件夹,名字一定要是libiPhone-lib.a
2. 执行RemoveUnityUIWebView.py脚本
	打开终端
	输入 python 空格 将RemoveUnityUIWebView.py拖入到空格后面 回车
3. 执行完成后,脚本会打印生成的libiPhone-lib.a