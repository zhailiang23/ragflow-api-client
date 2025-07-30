# RAGFlow API 客户端

这是一个用于与RAGFlow API交互的Python客户端，实现了完整的知识库管理流程。

## 功能特性

- ✅ 创建知识库（Create dataset）
- ✅ 上传文档（Upload documents）
- ✅ 解析文档（Parse documents）
- ✅ 检索文本块（Retrieve chunks）
- ✅ 完整的配置文件支持
- ✅ 详细的日志记录
- ✅ 错误处理和重试机制

## 安装

1. 克隆或下载此项目：
```bash
git clone <repository-url>
cd ragflow_api_client
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

或者直接安装核心依赖：
```bash
pip install requests
```

**注意：现在只需要一个外部依赖（requests），所有配置都使用Python内置的JSON格式。**

## 配置

1. 复制配置文件模板：
```bash
cp config.json config.json.example
```

2. 编辑 `config.json` 文件，填入您的配置信息：

```json
{
  "api": {
    "base_url": "http://localhost:9380",
    "api_key": "YOUR_API_KEY_HERE"
  },
  "dataset": {
    "name": "my_knowledge_base"
  }
}
```

**注意：JSON配置文件不支持注释，但我们在配置文件中使用了 `_comment` 字段来提供说明。**

### 主要配置项说明

#### API配置
- `base_url`: RAGFlow API的基础URL
- `api_key`: 您的API密钥（从RAGFlow管理界面获取）

#### 知识库配置
- `name`: 知识库名称（必须唯一）
- `embedding_model`: 嵌入模型（默认：BAAI/bge-large-zh-v1.5@BAAI）
- `chunk_method`: 分块方法（naive/qa/table/paper等）
- `parser_config`: 解析器配置（根据chunk_method不同而不同）

#### 文档配置
- `file_paths`: 要上传的文件路径列表
- `wait_for_parsing`: 是否等待文档解析完成
- `parsing_wait`: 解析等待相关配置

#### 检索配置
- `similarity_threshold`: 相似度阈值（0-1）
- `vector_similarity_weight`: 向量相似度权重
- `test_questions`: 测试查询问题列表

## 打包为可执行文件

项目提供了打包脚本，可以将Python脚本打包成独立的可执行文件，无需安装Python环境即可运行。

### Windows 打包

```bash
# 双击运行或在命令行执行
build.bat
```

### Linux/macOS 打包

```bash
# 在终端执行
./build.sh
```

### 打包产物

打包完成后，会在 `dist/` 目录生成可执行文件：
- Windows: `ragflow-client.exe`
- Linux/macOS: `ragflow-client`

### 可执行文件使用

```bash
# Windows
ragflow-client.exe --config config.json

# Linux/macOS  
./ragflow-client --config config.json

# 使用默认配置文件
ragflow-client.exe
```

## 使用方法

### 1. 运行完整工作流程

最简单的使用方式是运行完整的工作流程：

```bash
python ragflow_client.py
```

或指定配置文件：

```bash
python ragflow_client.py --config /path/to/config.json
# 或使用短参数
python ragflow_client.py -c /path/to/config.json
```

查看帮助信息：

```bash
python ragflow_client.py --help
```

这将自动执行以下步骤：
1. 创建知识库
2. 上传配置文件中指定的文档
3. 解析上传的文档
4. 使用测试问题进行检索

### 2. 作为Python库使用

您也可以在自己的Python代码中使用此客户端：

```python
from ragflow_client import RAGFlowClient

# 创建客户端实例
client = RAGFlowClient('config.json')

# 创建知识库
dataset = client.create_dataset(name="my_dataset")
dataset_id = dataset['id']

# 上传文档
documents = client.upload_documents(dataset_id, ['file1.txt', 'file2.pdf'])
document_ids = [doc['id'] for doc in documents]

# 解析文档
client.parse_documents(dataset_id, document_ids)

# 检索文本块
results = client.retrieve_chunks(
    question="你的问题",
    dataset_ids=[dataset_id]
)

# 处理结果
for chunk in results['chunks']:
    print(f"内容: {chunk['content']}")
    print(f"相似度: {chunk['similarity']}")
```

## 文件结构

```
ragflow_api_client/
├── ragflow_client.py      # 主客户端代码
├── config.json           # 配置文件
├── config.json.example   # 配置文件示例
├── requirements.txt      # Python依赖（仅requests）
├── README.md            # 本文档
└── test_data/           # 测试数据目录（可选）
    └── document1.txt
```

## 日志

程序会生成详细的日志文件（默认：`ragflow_client.log`），包含：
- API调用记录
- 错误信息
- 执行进度
- 调试信息（如果启用DEBUG级别）

## 错误处理

客户端包含了完善的错误处理机制：
- API错误会被捕获并记录
- 文件不存在会给出警告
- 网络错误会触发重试
- 所有错误都会记录到日志文件

## 注意事项

1. **极简依赖**：现在只依赖一个外部库（requests），大大降低了部署复杂度
2. **API密钥安全**：请不要将包含真实API密钥的配置文件提交到版本控制系统
3. **JSON配置**：配置文件使用标准JSON格式，易于解析和维护
4. **文件大小限制**：上传文件可能有大小限制，请查看RAGFlow文档
5. **并发限制**：避免同时发起过多请求，可能会触发速率限制
6. **文档解析时间**：大文档可能需要较长时间解析，请耐心等待

## 故障排除

### 常见问题

1. **"找不到配置文件"错误**
   - 确保config.json文件存在
   - 检查文件路径是否正确
   - 确保JSON格式正确，可以使用在线JSON验证工具检查

2. **"API错误：未授权"**
   - 检查API密钥是否正确
   - 确认API密钥有相应的权限

3. **"连接错误"**
   - 检查base_url是否正确
   - 确认RAGFlow服务正在运行
   - 检查网络连接

4. **"文档解析超时"**
   - 增加配置文件中的max_wait_time
   - 检查文档格式是否支持

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

[根据您的需要添加许可证信息]

## 联系方式

[添加您的联系方式]