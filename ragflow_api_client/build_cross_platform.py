#!/usr/bin/env python3
"""
跨平台构建脚本
Cross-platform build script for RAGFlow Client
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(cmd, check=True):
    """运行命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, check=check)
    return result.returncode == 0

def build_executable():
    """构建可执行文件"""
    system = platform.system().lower()
    print(f"当前系统: {system}")
    
    # 创建虚拟环境
    if system == "windows":
        venv_activate = "build_env\\Scripts\\activate.bat"
        exe_name = "ragflow-client.exe"
    else:
        venv_activate = "source build_env/bin/activate"
        exe_name = "ragflow-client"
    
    print("\n[1/4] 创建虚拟环境...")
    if Path("build_env").exists():
        if system == "windows":
            run_command("rmdir /s /q build_env")
        else:
            run_command("rm -rf build_env")
    
    run_command(f"{sys.executable} -m venv build_env")
    
    print("\n[2/4] 安装依赖...")
    if system == "windows":
        run_command(f"{venv_activate} && pip install --upgrade pip")
        run_command(f"{venv_activate} && pip install requests==2.31.0 pyinstaller")
    else:
        run_command(f"{venv_activate} && pip install --upgrade pip")
        run_command(f"{venv_activate} && pip install requests==2.31.0 pyinstaller")
    
    print("\n[3/4] 打包应用...")
    if system == "windows":
        success = run_command(f"{venv_activate} && pyinstaller --clean ragflow_client.spec")
    else:
        success = run_command(f"{venv_activate} && pyinstaller --clean ragflow_client.spec")
    
    print("\n[4/4] 检查结果...")
    exe_path = Path("dist") / exe_name
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"✅ 打包成功！")
        print(f"📁 文件位置: {exe_path}")
        print(f"📏 文件大小: {size_mb:.1f}MB")
        
        print(f"\n🚀 使用方法:")
        if system == "windows":
            print(f"   {exe_path} --config config.json")
        else:
            print(f"   ./{exe_path} --config config.json")
    else:
        print("❌ 打包失败！请检查错误信息。")
        return False
    
    # 清理
    print("\n🧹 清理构建文件...")
    if system == "windows":
        run_command("rmdir /s /q build_env", check=False)
        run_command("rmdir /s /q build", check=False)
        run_command("rmdir /s /q __pycache__", check=False)
    else:
        run_command("rm -rf build_env", check=False)
        run_command("rm -rf build", check=False)
        run_command("rm -rf __pycache__", check=False)
    
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("RAGFlow Client 跨平台构建工具")
    print("=" * 50)
    
    success = build_executable()
    
    if success:
        print("\n🎉 构建完成！")
    else:
        print("\n💥 构建失败！")
        sys.exit(1)