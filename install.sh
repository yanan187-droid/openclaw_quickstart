#!/bin/bash
# OpenClaw 10分钟极速上手技能 - 快速安装脚本

set -e

SKILL_NAME="openclaw-quickstart"
SKILL_DIR="$HOME/.openclaw/skills/$SKILL_NAME"
DATA_DIR="$HOME/.openclaw/skills/quickstart/data"

echo "🦞 OpenClaw 10分钟极速上手技能安装脚本"
echo "=========================================="

# 检查OpenClaw目录
if [ ! -d "$HOME/.openclaw" ]; then
    echo "❌ 未找到OpenClaw目录，请先安装OpenClaw"
    exit 1
fi

# 创建目录
echo "📁 创建技能目录..."
mkdir -p "$SKILL_DIR"
mkdir -p "$DATA_DIR"

# 复制文件
echo "📦 复制技能文件..."
cp manifest.json "$SKILL_DIR/"
cp main.py "$SKILL_DIR/"
cp tasks.json "$SKILL_DIR/"
cp README.md "$SKILL_DIR/"

# 设置权限
chmod +x "$SKILL_DIR/main.py"
chmod 755 "$SKILL_DIR"
chmod 755 "$DATA_DIR"

echo ""
echo "✅ 安装成功！"
echo ""
echo "📍 安装位置: $SKILL_DIR"
echo "💾 数据位置: $DATA_DIR"
echo ""
echo "🚀 使用方法:"
echo "   1. 重启OpenClaw 或发送 /reload"
echo "   2. 发送: 开始"
echo ""
echo "📖 查看帮助: 发送「帮助」"
echo ""
