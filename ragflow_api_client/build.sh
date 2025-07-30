#!/bin/bash
# RAGFlow Client 打包脚本
# 用于将Python脚本打包成可执行文件

set -e

echo "================================"
echo "RAGFlow Client 打包工具"
echo "================================"
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误：未找到Python3，请先安装Python 3.8+"
    exit 1
fi

echo "[1/4] 检查Python环境..."
python3 --version

# 创建虚拟环境
echo
echo "[2/4] 创建虚拟环境..."
if [ -d "build_env" ]; then
    echo "删除现有虚拟环境..."
    rm -rf build_env
fi
python3 -m venv build_env
source build_env/bin/activate

# 安装依赖
echo
echo "[3/4] 安装依赖包..."
pip install --upgrade pip
pip install requests==2.31.0
pip install pyinstaller

# 打包应用
echo
echo "[4/4] 打包应用程序..."
pyinstaller --clean ragflow_client.spec

# 检查打包结果
if [ -f "dist/ragflow-client" ]; then
    echo
    echo "================================"
    echo "打包成功！"
    echo "================================"
    echo "可执行文件位置: dist/ragflow-client"
    echo "文件大小: $(du -h dist/ragflow-client | cut -f1)"
    echo
    echo "使用方法:"
    echo "  1. 复制 config.json.example 为 config.json 并配置"
    echo "  2. 运行: ./dist/ragflow-client"
    echo "  3. 或指定配置文件: ./dist/ragflow-client --config myconfig.json"
    echo
else
    echo
    echo "================================"
    echo "打包失败！"
    echo "================================"
    echo "请检查错误信息并重试"
    exit 1
fi

# 清理
echo "清理构建文件..."
rm -rf build_env
rm -rf __pycache__
rm -rf build

echo
echo "打包完成！"