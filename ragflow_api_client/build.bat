@echo off
REM RAGFlow Client 打包脚本
REM 用于将Python脚本打包成Windows可执行文件

echo ================================
echo RAGFlow Client 打包工具
echo ================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo [1/4] 检查Python环境...
python --version

REM 创建虚拟环境
echo.
echo [2/4] 创建虚拟环境...
if exist "build_env" (
    echo 删除现有虚拟环境...
    rmdir /s /q build_env
)
python -m venv build_env
call build_env\Scripts\activate.bat

REM 安装依赖
echo.
echo [3/4] 安装依赖包...
pip install --upgrade pip
pip install requests==2.31.0
pip install pyinstaller

REM 打包应用
echo.
echo [4/4] 打包应用程序...
pyinstaller --clean ragflow_client.spec

REM 检查打包结果
if exist "dist\ragflow-client.exe" (
    echo.
    echo ================================
    echo 打包成功！
    echo ================================
    echo 可执行文件位置: dist\ragflow-client.exe
    echo 文件大小:
    dir "dist\ragflow-client.exe" | findstr ragflow-client
    echo.
    echo 使用方法:
    echo   1. 复制 config.json.example 为 config.json 并配置
    echo   2. 运行: ragflow-client.exe
    echo   3. 或指定配置文件: ragflow-client.exe --config myconfig.json
    echo.
) else (
    echo.
    echo ================================
    echo 打包失败！
    echo ================================
    echo 请检查错误信息并重试
)

REM 清理
echo 清理构建文件...
rmdir /s /q build_env
if exist "__pycache__" rmdir /s /q __pycache__
if exist "build" rmdir /s /q build

echo.
echo 按任意键退出...
pause >nul