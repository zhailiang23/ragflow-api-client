#!/bin/bash
# 迁移到GitHub的脚本
# Migration script to GitHub

echo "🔄 RAGFlow客户端迁移到GitHub"
echo "================================"

# 提示用户输入GitHub信息
read -p "请输入您的GitHub用户名: " github_username
read -p "请输入仓库名称 (默认: ragflow-api-client): " repo_name

# 设置默认值
repo_name=${repo_name:-ragflow-api-client}

echo ""
echo "📋 迁移信息:"
echo "   GitHub用户名: $github_username"
echo "   仓库名称: $repo_name"
echo "   仓库地址: https://github.com/$github_username/$repo_name.git"
echo ""

read -p "确认迁移? (y/N): " confirm

if [[ $confirm != [yY] ]]; then
    echo "❌ 迁移已取消"
    exit 0
fi

echo ""
echo "🚀 开始迁移..."

# 添加GitHub作为新的远程仓库
echo "[1/4] 添加GitHub远程仓库..."
git remote add github https://github.com/$github_username/$repo_name.git

# 显示远程仓库配置
echo "[2/4] 当前远程仓库配置:"
git remote -v

# 推送当前分支到GitHub
current_branch=$(git branch --show-current)
echo "[3/4] 推送分支 '$current_branch' 到GitHub..."
git push github $current_branch

# 推送main分支到GitHub
echo "[4/4] 推送main分支到GitHub..."
git push github main

echo ""
echo "✅ 迁移完成！"
echo ""
echo "📋 下一步操作:"
echo "   1. 访问: https://github.com/$github_username/$repo_name"
echo "   2. 点击 Actions 标签页"
echo "   3. 点击 'Build RAGFlow Client' 工作流"
echo "   4. 点击 'Run workflow' 按钮触发构建"
echo "   5. 等待构建完成后下载 Windows 可执行文件"
echo ""
echo "🎯 设置新的默认远程仓库 (可选):"
echo "   git remote set-url origin https://github.com/$github_username/$repo_name.git"
echo "   git remote remove github"