#!/bin/bash

echo "========================================"
echo "   OmniVideo - 多平台视频解析系统"
echo "========================================"
echo ""

cd "$(dirname "$0")/.."

echo "[1/4] 检查 Docker 环境..."
if ! command -v docker &> /dev/null; then
    echo "错误: Docker 未安装，请先安装 Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "错误: Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi

echo ""
echo "[2/4] 构建前端..."
cd frontend/web
npm install --silent 2>/dev/null
npm run build 2>/dev/null
cd ../..

echo ""
echo "[3/4] 启动 Docker 服务..."
docker-compose -f docker/docker-compose.yml up -d --build

echo ""
echo "[4/4] 等待服务就绪..."
sleep 15

echo ""
echo "========================================"
echo "   服务已启动！"
echo "========================================"
echo ""
echo "  Web 前端:    http://localhost"
echo "  API 文档:    http://localhost:8000/docs"
echo "  下载引擎:    http://localhost:8080"
echo "  MinIO 控制台: http://localhost:9001"
echo ""
echo "  停止服务: docker-compose -f docker/docker-compose.yml down"
echo "  查看日志: docker-compose -f docker/docker-compose.yml logs -f"
echo ""
