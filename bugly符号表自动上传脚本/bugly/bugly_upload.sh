# 需要Java版本 jdk-8u341-macosx-x64.dmg

# 组装参数
# BUGLY_APP_ID
# BUGLY_APP_KEY
# BUNDLE_IDENTIFIER
# App Version
# platform IOS
# inputSymbol

if [ $ACTION != install ]; then
    echo "Xcode build"
    exit 0
fi

if [ "${CONFIGURATION}" == "Debug" ]; then
    echo "Debug模式不继续执行脚本"
    exit 0
fi

# 默认是Release的参数
BUGLY_APP_ID="BUGLY_APP_ID"
BUGLY_APP_KEY="BUGLY_APP_KEY"
if [ "${CONFIGURATION}" != "Release" ]; then
    BUGLY_APP_ID="debug_BUGLY_APP_ID"
    BUGLY_APP_KEY="debug_BUGLY_APP_KEY"
fi

echo "当前编译模式: ${CONFIGURATION}"

echo "--------------Product Name: ${PRODUCT_NAME}"
echo "--------------Bundle Identifier: ${PRODUCT_BUNDLE_IDENTIFIER}"
echo "--------------版本号Version: ${MARKETING_VERSION}"
echo "--------------构建Build: ${CURRENT_PROJECT_VERSION}"

echo "--------------Bugly App ID: ${BUGLY_APP_ID}"
echo "--------------Bugly App key: ${BUGLY_APP_KEY}"
BUGLY_APP_VERSION="${MARKETING_VERSION}(${CURRENT_PROJECT_VERSION})"
echo "--------------Bugly App Version: ${BUGLY_APP_VERSION}"


exitWithMessage() {
    echo "--------------------------------"
    echo -e "${1}"
    echo "--------------------------------"
    echo "No upload and exit."
    echo "----------------------------------------------------------------"
    exit 0
}


function uploadDSYM {

    DSYM_SRC="$1"
    echo "--------------开始上传"
    echo "--------------上传命令: java -jar ${BUGLY_SYMBOL_JAR_PATH} -appid ${BUGLY_APP_ID} -appkey ${BUGLY_APP_KEY} -bundleid ${PRODUCT_BUNDLE_IDENTIFIER} -version ${MARKETING_VERSION} -appBuildNo ${CURRENT_PROJECT_VERSION} -platform IOS -inputSymbol ${DSYM_SRC}"
    
    (java -jar ${BUGLY_SYMBOL_JAR_PATH} -appid ${BUGLY_APP_ID} -appkey ${BUGLY_APP_KEY} -bundleid ${PRODUCT_BUNDLE_IDENTIFIER} -version ${MARKETING_VERSION} -appBuildNo ${CURRENT_PROJECT_VERSION} -platform IOS -inputSymbol ${DSYM_SRC}) || exitWithMessage "上传符号表失败." 0
}


# .dSYM生成的文件夹
echo "--------------dSYM所在的文件路径: ${DWARF_DSYM_FOLDER_PATH}"

BUGLY_SYMBOL_JAR_PATH="${SRCROOT}/script/bugly/buglyqq-upload-symbol.jar"

for dsymFile in $(find "${DWARF_DSYM_FOLDER_PATH}" -name '你app的名字.*.dSYM'); do
    echo "--------------找到 dSYM file: $dsymFile"
    uploadDSYM ${dsymFile}
done
