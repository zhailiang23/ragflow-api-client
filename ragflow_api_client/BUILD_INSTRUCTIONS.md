# 如何获取Windows可执行文件

本项目使用GitHub Actions自动构建多平台可执行文件，包括Windows、Linux和macOS版本。

## 方法1：下载预构建版本（推荐）

### 步骤1：访问GitHub仓库
1. 将项目上传到GitHub仓库
2. 访问仓库主页

### 步骤2：触发构建
有三种方式触发自动构建：

**方式A：手动触发**
1. 点击 `Actions` 标签页
2. 选择 `Build RAGFlow Client` 工作流
3. 点击 `Run workflow` 按钮
4. 点击绿色的 `Run workflow` 确认

**方式B：推送代码**
```bash
git add .
git commit -m "触发构建"
git push origin main
```

**方式C：创建Release**
1. 点击 `Releases` 标签页  
2. 点击 `Create a new release`
3. 填写版本号和说明
4. 点击 `Publish release`

### 步骤3：下载构建产物
构建完成后（通常需要5-10分钟）：

1. 点击 `Actions` 标签页
2. 点击最新的成功构建
3. 在 `Artifacts` 部分下载文件：
   - `ragflow-client-windows` - Windows版本
   - `ragflow-client-linux` - Linux版本  
   - `ragflow-client-macos` - macOS版本
   - `ragflow-client-all-platforms` - 所有平台打包版本

## 方法2：本地构建

如果您有相应的系统环境，也可以本地构建：

### Windows系统
```cmd
build.bat
```

### Linux/macOS系统
```bash
./build.sh
```

### 跨平台构建脚本
```bash
python build_cross_platform.py
```

## 使用构建的可执行文件

下载并解压后，您将得到：

```
ragflow-client-windows/
├── ragflow-client.exe    # Windows可执行文件
├── config.json.example   # 配置文件模板
├── README.md             # 使用说明
├── PACKAGING.md          # 打包说明
└── test_data/            # 测试数据（可选）
```

### 使用方法

1. **准备配置文件**
   ```cmd
   copy config.json.example config.json
   # 编辑config.json，填入您的API信息
   ```

2. **运行程序**
   ```cmd
   # 使用默认配置文件
   ragflow-client.exe
   
   # 指定配置文件
   ragflow-client.exe --config myconfig.json
   
   # 查看帮助
   ragflow-client.exe --help
   ```

## 构建状态

构建状态可以通过以下方式查看：
- GitHub仓库的Actions标签页
- README.md中的构建徽章（如果添加）
- Release页面的资产列表

## 故障排除

### 构建失败
1. 检查Actions日志中的错误信息
2. 确保所有必需文件都已提交到仓库
3. 检查Python代码语法是否正确

### 下载问题
1. 确保构建已完成（状态为绿色✅）
2. Artifacts有30天的保留期限
3. 如果过期，可以重新触发构建

### 运行问题
1. 确保从正确的平台下载（Windows用户下载windows版本）
2. 检查配置文件格式是否正确
3. 查看程序日志文件获取详细错误信息

## 注意事项

1. **GitHub账户**: 需要GitHub账户来访问和下载构建产物
2. **网络要求**: 构建过程需要网络连接下载依赖
3. **系统兼容性**: 
   - Windows: 支持Windows 10/11
   - Linux: 支持主流发行版
   - macOS: 支持macOS 10.15+
4. **文件大小**: 可执行文件约10-25MB，包含完整的Python运行时

## 自动化优势

使用GitHub Actions构建的优势：
- ✅ 多平台支持（Windows/Linux/macOS）
- ✅ 自动化构建，无需本地环境
- ✅ 版本管理和发布
- ✅ 构建历史和日志
- ✅ 免费使用（GitHub免费账户包含使用时间）