# 1.安装Java环境

## 需要特定版本:
- jdk-8u341-macosx-x64.dmg

## 查看Java安装位置:

如果本机存在多个版本，需要干掉其他版本的Java

```
/usr/libexec/java_home -V
```

# 将bugly文件夹复制到项目文件夹:
- script/

## 例如: 

```
/Users/ios/project/XcodeProject/script/bugly
```

## 打开Xcode项目 添加 Run Script配置:

```
${SRCROOT}/script/bugly/bugly_upload.sh
```



