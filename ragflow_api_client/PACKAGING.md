# RAGFlow Client 打包说明

本文档详细说明如何将RAGFlow客户端打包成独立的可执行文件。

## 打包准备

### 系统要求
- Python 3.8+
- 足够的磁盘空间（约100MB用于构建过程）

### 依赖包
打包过程会自动安装以下依赖：
- `requests==2.31.0` - HTTP请求库
- `pyinstaller` - Python打包工具

## 打包步骤

### Windows 系统

1. **双击运行打包脚本**
   ```cmd
   # 双击 build.bat 文件
   # 或在命令行中运行：
   build.bat
   ```

2. **打包过程**
   - 自动创建虚拟环境
   - 安装打包依赖
   - 使用PyInstaller打包应用
   - 清理临时文件

3. **打包结果**
   - 成功：`dist/ragflow-client.exe` （约15-25MB）
   - 失败：检查错误信息，通常是依赖问题

### Linux/macOS 系统

1. **运行打包脚本**
   ```bash
   chmod +x build.sh
   ./build.sh
   ```

2. **打包结果**
   - 成功：`dist/ragflow-client` 
   - 失败：检查错误信息

## 使用打包后的可执行文件

### 基本使用

```bash
# Windows
ragflow-client.exe

# Linux/macOS
./ragflow-client
```

### 指定配置文件

```bash
# Windows
ragflow-client.exe --config myconfig.json
ragflow-client.exe -c myconfig.json

# Linux/macOS
./ragflow-client --config myconfig.json
./ragflow-client -c myconfig.json
```

### 查看帮助

```bash
# Windows
ragflow-client.exe --help
ragflow-client.exe --version

# Linux/macOS
./ragflow-client --help
./ragflow-client --version
```

## 分发说明

### 必需文件
分发可执行文件时，需要包含：
1. `ragflow-client.exe` (Windows) 或 `ragflow-client` (Linux/macOS)
2. `config.json.example` - 配置文件模板
3. `README.md` - 使用说明

### 可选文件
- `test_data/` - 测试数据目录
- 其他文档文件

### 最小分发包
```
ragflow-client/
├── ragflow-client.exe    # 主程序
├── config.json.example   # 配置模板
└── README.md            # 使用说明
```

## 故障排除

### 打包失败

1. **Python版本问题**
   - 确保Python版本 >= 3.8
   - 使用 `python --version` 检查

2. **依赖安装失败**
   - 检查网络连接
   - 使用国内镜像：`pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/`

3. **磁盘空间不足**
   - 确保有足够空间（至少100MB）

4. **权限问题**
   - Windows：以管理员身份运行
   - Linux/macOS：确保脚本有执行权限

### 运行时问题

1. **配置文件找不到**
   ```bash
   # 使用绝对路径
   ragflow-client.exe --config "C:\path\to\config.json"
   ```

2. **API连接失败**
   - 检查配置文件中的API地址和密钥
   - 确保RAGFlow服务正在运行

3. **文件上传失败**
   - 检查文件路径是否正确
   - 确保文件存在且可读

## 高级配置

### 自定义打包

如需修改打包配置，编辑 `ragflow_client.spec` 文件：

```python
# 添加额外文件
datas=[
    ('config.json.example', '.'),
    ('my_custom_data', 'data'),  # 添加自定义数据
],

# 排除不需要的模块
excludes=[
    'matplotlib',
    'numpy',
    # 添加其他不需要的模块
],
```

### 优化可执行文件大小

1. **启用UPX压缩** (默认已启用)
   ```python
   upx=True,
   ```

2. **排除不必要的模块**
   在 `excludes` 列表中添加不需要的包

3. **使用虚拟环境**
   确保只安装必需的依赖包

## 技术细节

### 打包工具
- **PyInstaller**: 将Python应用打包成独立可执行文件
- **Virtual Environment**: 隔离构建环境，避免依赖冲突

### 文件结构
```
打包后的文件内部结构：
- Python解释器
- 应用代码 (ragflow_client.py)
- 依赖库 (requests等)
- 资源文件 (配置模板等)
```

### 性能考虑
- 启动时间：约1-3秒（包含Python环境初始化）
- 内存占用：约20-50MB
- 文件大小：15-25MB（压缩后）