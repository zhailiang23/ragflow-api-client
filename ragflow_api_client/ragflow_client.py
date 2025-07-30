#!/usr/bin/env python3
"""
RAGFlow API Client
实现RAGFlow知识库管理的完整流程：
1. 创建知识库（Create dataset）
2. 上传文档（Upload documents）
3. 解析文档（Parse documents）
4. 检索文本块（Retrieve chunks）

作者：翟亮
日期：2025-01-30
"""

import sys
import json
import logging
import requests
from pathlib import Path
from typing import List, Dict, Any


class RAGFlowClient:
    """RAGFlow API 客户端类"""
    
    def __init__(self, config_path: str = "config.json"):
        """
        初始化RAGFlow客户端
        
        参数:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.base_url = self.config['api']['base_url']
        self.api_key = self.config['api']['api_key']
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        # 设置日志
        self._setup_logging()
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"错误：找不到配置文件 {config_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"错误：解析配置文件失败 {e}")
            sys.exit(1)
            
    def _setup_logging(self):
        """设置日志配置"""
        log_config = self.config.get('logging', {})
        log_level = getattr(logging, log_config.get('level', 'INFO'))
        log_format = log_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        logging.basicConfig(
            level=log_level,
            format=log_format,
            handlers=[
                logging.FileHandler(log_config.get('file', 'ragflow_client.log')),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        发送HTTP请求的通用方法
        
        参数:
            method: HTTP方法（GET, POST, PUT, DELETE等）
            endpoint: API端点
            **kwargs: 其他请求参数
            
        返回:
            响应的JSON数据
        """
        url = f"{self.base_url}{endpoint}"
        
        # 如果kwargs中包含headers，合并而不是覆盖
        headers = kwargs.pop('headers', {})
        
        # 文件上传时，不应该设置Content-Type header
        if 'files' in kwargs:
            # 只保留Authorization header
            headers = {'Authorization': self.headers['Authorization'], **headers}
        else:
            headers = {**self.headers, **headers}
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                **kwargs
            )
            response.raise_for_status()
            
            result = response.json()
            if result.get('code') != 0:
                error_msg = result.get('message', 'Unknown error')
                self.logger.error(f"API错误: {error_msg}")
                raise Exception(f"API错误: {error_msg}")
                
            return result
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"请求失败: {e}")
            raise
            
    def create_dataset(self, name: str = None, **kwargs) -> Dict[str, Any]:
        """
        创建知识库
        
        参数:
            name: 知识库名称（如果不提供，使用配置文件中的默认值）
            **kwargs: 其他创建参数
            
        返回:
            创建的知识库信息
        """
        # 从配置文件获取参数
        dataset_config = self.config['dataset']
        
        # 构建请求体
        data = {
            "name": name or dataset_config['name'],
            "avatar": dataset_config.get('avatar'),
            "description": dataset_config.get('description'),
            "embedding_model": dataset_config.get('embedding_model', 'BAAI/bge-large-zh-v1.5@BAAI'),
            "permission": dataset_config.get('permission', 'me'),
            "chunk_method": dataset_config.get('chunk_method', 'naive'),
            "parser_config": dataset_config.get('parser_config', {
                "chunk_token_num": 128,
                "delimiter": "\\n",
                "html4excel": False,
                "layout_recognize": "DeepDOC",
                "raptor": {"use_raptor": False}
            })
        }
        
        # 更新传入的参数
        data.update(kwargs)
        
        # 移除None值
        data = {k: v for k, v in data.items() if v is not None}
        
        self.logger.info(f"创建知识库: {data['name']}")
        
        result = self._make_request('POST', '/api/v1/datasets', json=data)
        
        dataset_id = result['data']['id']
        self.logger.info(f"知识库创建成功，ID: {dataset_id}")
        
        return result['data']
        
    def upload_documents(self, dataset_id: str, file_paths: List[str]) -> List[Dict[str, Any]]:
        """
        向知识库上传文档
        
        参数:
            dataset_id: 知识库ID
            file_paths: 文件路径列表
            
        返回:
            上传的文档信息列表
        """
        # 准备文件
        files = []
        for file_path in file_paths:
            path = Path(file_path)
            if not path.exists():
                self.logger.warning(f"文件不存在: {file_path}")
                continue
                
            files.append(('file', (path.name, open(path, 'rb'), 'application/octet-stream')))
            
        if not files:
            raise ValueError("没有有效的文件可上传")
            
        self.logger.info(f"上传 {len(files)} 个文件到知识库 {dataset_id}")
        
        # 上传文件时，让requests自动设置Content-Type
        result = self._make_request(
            'POST',
            f'/api/v1/datasets/{dataset_id}/documents',
            files=files
        )
        
        # 关闭文件
        for _, (_, file_obj, _) in files:
            file_obj.close()
            
        documents = result['data']
        self.logger.info(f"成功上传 {len(documents)} 个文档")
        
        return documents
        
    def parse_documents(self, dataset_id: str, document_ids: List[str]) -> bool:
        """
        解析文档
        
        参数:
            dataset_id: 知识库ID
            document_ids: 文档ID列表
            
        返回:
            是否成功
        """
        self.logger.info(f"开始解析 {len(document_ids)} 个文档")
        
        data = {
            "document_ids": document_ids
        }
        
        self._make_request(
            'POST',
            f'/api/v1/datasets/{dataset_id}/chunks',
            json=data
        )
        
        self.logger.info("文档解析任务已提交")
        
        return True
        
    def list_datasets(self, name: str = None) -> List[Dict[str, Any]]:
        """
        列出知识库
        
        参数:
            name: 知识库名称（可选，用于筛选）
            
        返回:
            知识库列表
        """
        # 获取所有知识库
        result = self._make_request('GET', '/api/v1/datasets')
        datasets = result.get('data', [])
        
        # 如果指定了名称，在本地过滤
        if name:
            datasets = [d for d in datasets if d.get('name') == name]
            
        return datasets
        
    def run_complete_workflow(self):
        """
        运行完整的工作流程：
        1. 创建或获取知识库
        2. 上传文档
        3. 解析文档
        """
        try:
            # 1. 创建或获取知识库
            self.logger.info("=== 步骤1：创建或获取知识库 ===")
            dataset_name = self.config['dataset']['name']
            
            # 首先检查知识库是否已存在
            existing_datasets = self.list_datasets(name=dataset_name)
            
            if existing_datasets:
                # 使用现有的知识库
                dataset = existing_datasets[0]
                dataset_id = dataset['id']
                self.logger.info(f"使用现有知识库: {dataset_name} (ID: {dataset_id})")
            else:
                # 创建新知识库
                dataset = self.create_dataset()
                dataset_id = dataset['id']
            
            # 2. 上传文档
            self.logger.info("=== 步骤2：上传文档 ===")
            file_paths = self.config.get('document', {}).get('file_paths', [])
            if not file_paths:
                self.logger.warning("配置文件中没有指定要上传的文件")
                return
                
            documents = self.upload_documents(dataset_id, file_paths)
            document_ids = [doc['id'] for doc in documents]
            
            # 3. 解析文档
            self.logger.info("=== 步骤3：解析文档 ===")
            self.parse_documents(dataset_id, document_ids)
            
            self.logger.info("=== 工作流程完成 ===")
            self.logger.info(f"知识库ID: {dataset_id}")
            self.logger.info(f"已上传 {len(documents)} 个文档")
            self.logger.info("文档解析任务已提交，可以开始使用知识库进行检索")
            
        except Exception as e:
            self.logger.error(f"工作流程执行失败: {e}")
            raise


def main():
    """主函数"""
    # 检查命令行参数
    import argparse
    
    parser = argparse.ArgumentParser(description='RAGFlow API Client - 知识库管理工具')
    parser.add_argument('--config', '-c', default='config.json', 
                       help='配置文件路径 (默认: config.json)')
    parser.add_argument('--version', '-v', action='version', version='1.0.0')
    
    args = parser.parse_args()
    config_path = args.config
        
    # 创建客户端并运行工作流程
    client = RAGFlowClient(config_path)
    client.run_complete_workflow()


if __name__ == "__main__":
    main()