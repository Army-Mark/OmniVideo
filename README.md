# OmniVideo - 多平台视频解析与下载系统

<div align="center">

![OmniVideo](https://img.shields.io/badge/OmniVideo-v1.0-blue)
![Python](https://img.shields.io/badge/Python-3.11+-green)
![Go](https://img.shields.io/badge/Go-1.21+-00ADD8)
![Vue](https://img.shields.io/badge/Vue-3-4FC08D)
![License](https://img.shields.io/badge/License-MIT-yellow)

</div>

## 📖 项目简介

OmniVideo 是一个基于**多语言微服务架构**的多平台视频解析、下载与 AI 内容分析系统。支持抖音、B站、小红书、快手、YouTube 等主流视频平台的**无水印视频解析与下载**，并提供基于 Qwen3-VL 大模型的智能视频内容分析能力。

### 设计背景

当前市面上大多数视频下载工具存在以下痛点：

- **平台支持单一**：大多数工具只支持 1-2 个平台
- **解析能力弱**：无法应对平台反爬策略更新
- **下载体验差**：缺少断点续传、多线程下载等高级功能
- **无 AI 能力**：无法对视频内容进行智能分析
- **部署复杂**：需要手动配置各种依赖环境

OmniVideo 通过**工厂模式解析器**、**Go 高性能下载引擎**、**AI 内容分析**三大核心能力，提供一站式视频解析下载解决方案。

---

## ✨ 核心特性

### 🎯 多平台解析

| 平台 | 状态 | 解析方式 | 支持功能 |
|------|------|----------|----------|
| 抖音 (Douyin) | ✅ 已完成 | 自研解析器 | 无水印视频、封面、作者信息 |
| 哔哩哔哩 (Bilibili) | ✅ 已完成 | 自研解析器 | 视频、音频、弹幕、字幕 |
| 小红书 (Xiaohongshu) | ✅ 已完成 | 自研解析器 | 图文、视频笔记 |
| 快手 (Kuaishou) | 🔜 计划中 | 第三方 API | 视频解析 |
| YouTube | 🔜 计划中 | 第三方 API | 视频/音频下载 |
| 微博 (Weibo) | � 计划中 | 第三方 API | 视频解析 |

### �🚀 高性能下载

- **Go 语言实现**：原生协程并发，资源占用低
- **多线程分块下载**：自动分块并行下载，速度提升 3-5 倍
- **断点续传**：支持暂停、继续、取消操作
- **实时进度**：WebSocket 推送下载进度、速度、剩余时间
- **智能限速**：可配置下载速度限制

### 🤖 AI 内容分析

- **视频摘要**：基于 Qwen3-VL 自动生成视频内容摘要
- **关键词提取**：智能提取视频核心关键词
- **情绪分析**：分析视频画面情绪倾向
- **场景识别**：识别视频中的主要场景

### 📱 多端支持

- **Web 端**：Vue3 + Element Plus，响应式设计
- **微信小程序**：Taro3 跨端框架，一套代码多端运行
- **RESTful API**：标准化接口设计，易于第三方集成

### 🐳 一键部署

- **Docker Compose**：一条命令启动所有服务
- **健康检查**：自动检测服务状态，异常自动重启
- **数据持久化**：MySQL、Redis、MinIO 数据持久化存储

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                         客户端层                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Web 前端    │  │  微信小程序   │  │  第三方调用   │          │
│  │  Vue3+ELPlus │  │    Taro3     │  │   REST API   │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
└─────────┼─────────────────┼─────────────────┼───────────────────┘
          │                 │                 │
          ▼                 ▼                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Nginx 反向代理                              │
│              负载均衡 / SSL 终止 / 静态资源缓存                    │
└─────────────────────────┬───────────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
┌─────────────────┐ ┌─────────────┐ ┌─────────────────┐
│   Core Service  │ │  AI Service │ │ Download Engine │
│   (Python/FastAPI) │ │  (Qwen3-VL) │ │    (Go/Gin)     │
│                 │ │             │ │                 │
│ • 视频解析       │ │ • 内容摘要   │ │ • 多线程下载     │
│ • 用户管理       │ │ • 关键词提取 │ │ • 断点续传       │
│ • 下载调度       │ │ • 情绪分析   │ │ • 进度推送       │
│ • 平台适配       │ │ • 场景识别   │ │ • 限速控制       │
└────────┬────────┘ └──────┬──────┘ └────────┬────────┘
         │                 │                 │
         ▼                 ▼                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                        数据存储层                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │    MySQL     │  │    Redis     │  │    MinIO     │          │
│  │   用户数据    │  │   缓存/会话   │  │   视频文件    │          │
│  │   下载记录    │  │   任务队列    │  │   封面图片    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 项目结构

```
OmniVideo/
├── backend/
│   ├── core-service/                     # Python FastAPI 核心服务
│   │   ├── src/
│   │   │   ├── __init__.py
│   │   │   ├── main.py                   # 应用入口，生命周期管理
│   │   │   ├── ai/                       # AI 视频分析模块
│   │   │   │   ├── __init__.py
│   │   │   │   └── qwen3vl.py            # Qwen3-VL 模型封装
│   │   │   ├── api/                      # API 路由层
│   │   │   │   ├── router.py             # 路由聚合
│   │   │   │   └── endpoints/
│   │   │   │       ├── __init__.py
│   │   │   │       ├── parse.py          # 视频解析接口
│   │   │   │       ├── download.py       # 下载管理接口
│   │   │   │       ├── ai.py             # AI 分析接口
│   │   │   │       └── user.py           # 用户认证接口
│   │   │   ├── models/                   # 数据模型层
│   │   │   │   ├── __init__.py
│   │   │   │   ├── database.py           # 数据库引擎配置
│   │   │   │   ├── entities.py           # SQLAlchemy ORM 实体
│   │   │   │   └── schemas.py            # Pydantic 请求/响应模型
│   │   │   └── parsers/                  # 视频解析器（工厂模式）
│   │   │       ├── __init__.py
│   │   │       ├── base_parser.py        # 解析器抽象基类
│   │   │       ├── parser_factory.py     # 解析器工厂
│   │   │       ├── douyin_parser.py      # 抖音解析器
│   │   │       ├── bilibili_parser.py    # B站解析器
│   │   │       └── xiaohongshu_parser.py # 小红书解析器
│   │   ├── .env.example                  # 环境变量模板
│   │   └── requirements.txt              # Python 依赖
│   │
│   └── download-engine/                  # Go 高性能下载引擎
│       ├── go.mod                        # Go 模块定义
│       ├── go.sum                        # 依赖校验
│       └── main.go                       # 下载引擎主程序
│
├── frontend/
│   ├── web/                              # Vue3 Web 前端
│   │   ├── src/
│   │   │   ├── App.vue                   # 根组件（含导航栏布局）
│   │   │   ├── main.ts                   # 应用入口
│   │   │   ├── components/
│   │   │   │   ├── VideoCard.vue         # 视频卡片组件
│   │   │   │   └── PlatformList.vue      # 平台列表组件
│   │   │   ├── views/
│   │   │   │   ├── HomeView.vue          # 首页（解析入口）
│   │   │   │   ├── DownloadView.vue      # 下载管理页
│   │   │   │   └── HistoryView.vue       # 历史记录页
│   │   │   ├── stores/
│   │   │   │   └── video.ts              # Pinia 视频状态管理
│   │   │   ├── types/
│   │   │   │   └── index.ts              # TypeScript 类型定义
│   │   │   └── utils/
│   │   │       └── request.ts            # Axios 封装（含 JWT 拦截器）
│   │   ├── index.html
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   ├── tsconfig.node.json
│   │   └── vite.config.ts
│   │
│   └── miniprogram/                      # Taro3 微信小程序
│       ├── config/
│       │   ├── index.ts                  # 全局配置
│       │   ├── dev.ts                    # 开发环境配置
│       │   └── prod.ts                   # 生产环境配置
│       ├── src/
│       │   ├── app.ts                    # 应用入口
│       │   ├── app.vue                   # 应用根组件
│       │   ├── app.scss                  # 全局样式
│       │   ├── pages/
│       │   │   ├── index/                # 首页
│       │   │   ├── download/             # 下载页
│       │   │   └── profile/              # 个人中心
│       │   └── stores/
│       │       └── video.ts              # 视频状态管理
│       ├── package.json
│       ├── tsconfig.json
│       └── project.config.json
│
├── docker/
│   ├── Dockerfile.core-service           # 核心服务镜像构建
│   ├── Dockerfile.download-engine        # 下载引擎镜像构建
│   ├── docker-compose.yml                # 一键编排所有服务
│   └── nginx.conf                        # Nginx 反向代理配置
│
├── scripts/
│   ├── start.bat                         # Windows 一键启动
│   └── start.sh                          # Linux/Mac 一键启动
│
├── .gitignore
└── README.md
```

---

## 🚀 快速开始

### 环境要求

| 组件 | 版本 | 说明 |
|------|------|------|
| Docker | 20.10+ | 容器运行时 |
| Docker Compose | 2.0+ | 服务编排 |
| Python | 3.10+ | 本地开发（可选） |
| Go | 1.21+ | 本地开发（可选） |
| Node.js | 20+ | 本地开发（可选） |

### Docker 一键部署

```bash
# 1. 克隆项目
git clone https://github.com/Army-Mark/OmniVideo.git
cd OmniVideo

# 2. 启动所有服务（首次运行会自动拉取镜像、构建）
docker-compose -f docker/docker-compose.yml up -d

# 3. 查看服务状态
docker-compose -f docker/docker-compose.yml ps

# 4. 查看日志
docker-compose -f docker/docker-compose.yml logs -f
```

### 服务访问地址

| 服务 | 地址 | 说明 |
|------|------|------|
| Web 前端 | http://localhost | Nginx 反向代理 |
| API 文档 | http://localhost:8000/docs | Swagger UI |
| 下载引擎 | http://localhost:8080 | Go 下载服务 |
| MinIO 控制台 | http://localhost:9001 | 对象存储管理 |
| MySQL | localhost:3306 | 关系型数据库 |
| Redis | localhost:6379 | 缓存/会话 |

### 本地开发

#### 后端核心服务

```bash
cd backend/core-service

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置数据库连接等信息

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

#### 后端下载引擎

```bash
cd backend/download-engine

# 下载依赖
go mod download

# 启动服务
go run main.go
```

#### 前端 Web

```bash
cd frontend/web

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

#### 微信小程序

```bash
cd frontend/miniprogram

# 安装依赖
npm install

# 开发模式
npm run dev:weapp

# 生产构建
npm run build:weapp
```

---

## 📡 API 接口文档

### 视频解析

#### 解析视频链接

```http
POST /api/parse/
Content-Type: application/json

{
  "url": "https://www.douyin.com/video/xxxxx"
}
```

**响应示例：**

```json
{
  "platform": "douyin",
  "title": "视频标题",
  "author": "作者昵称",
  "cover": "https://...",
  "duration": 60,
  "play_count": 10000,
  "like_count": 5000,
  "download_url": "https://...",
  "formats": [
    {
      "quality": "1080p",
      "size": 10240000,
      "url": "https://..."
    }
  ]
}
```

#### 获取支持的平台列表

```http
GET /api/parse/platforms
```

### 下载管理

#### 创建下载任务

```http
POST /api/download/
Content-Type: application/json

{
  "url": "https://...",
  "filename": "video.mp4",
  "quality": "1080p"
}
```

#### 获取下载列表

```http
GET /api/download/
```

#### 获取下载状态

```http
GET /api/download/{task_id}
```

#### 暂停下载

```http
POST /api/download/{task_id}/pause
```

#### 继续下载

```http
POST /api/download/{task_id}/resume
```

#### 取消下载

```http
DELETE /api/download/{task_id}
```

### AI 分析

#### 分析视频内容

```http
POST /api/ai/analyze
Content-Type: multipart/form-data

file: <视频文件>
```

#### 生成视频摘要

```http
POST /api/ai/summary
Content-Type: multipart/form-data

file: <视频文件>
```

#### 提取关键词

```http
POST /api/ai/keywords
Content-Type: multipart/form-data

file: <视频文件>
```

#### 情绪分析

```http
POST /api/ai/emotion
Content-Type: multipart/form-data

file: <视频文件>
```

### 用户认证

#### 用户注册

```http
POST /api/user/register
Content-Type: application/json

{
  "username": "testuser",
  "password": "password123",
  "email": "test@example.com"
}
```

#### 用户登录

```http
POST /api/user/login
Content-Type: application/json

{
  "username": "testuser",
  "password": "password123"
}
```

**响应示例：**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

#### 获取用户信息

```http
GET /api/user/profile
Authorization: Bearer <access_token>
```

---

## 🛠️ 技术栈

### 前端

| 技术 | 版本 | 用途 |
|------|------|------|
| Vue3 | 3.4+ | 前端框架 |
| Vite | 5.0+ | 构建工具 |
| TypeScript | 5.0+ | 类型系统 |
| Element Plus | 2.5+ | UI 组件库 |
| Pinia | 2.1+ | 状态管理 |
| Vue Router | 4.2+ | 路由管理 |
| Axios | 1.6+ | HTTP 客户端 |
| Taro3 | 3.6+ | 小程序跨端框架 |

### 后端

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.11+ | 核心服务语言 |
| FastAPI | 0.110+ | Web 框架 |
| SQLAlchemy | 2.0+ | ORM |
| aiomysql | 0.2+ | 异步 MySQL 驱动 |
| Redis | 7.x | 缓存/会话 |
| Go | 1.21+ | 下载引擎语言 |
| Gin | 1.9+ | Go Web 框架 |
| Qwen3-VL | - | AI 视频分析模型 |

### 基础设施

| 技术 | 版本 | 用途 |
|------|------|------|
| Docker | 20.10+ | 容器化 |
| Docker Compose | 2.0+ | 服务编排 |
| Nginx | 1.25+ | 反向代理 |
| MySQL | 8.0+ | 关系型数据库 |
| MinIO | - | 对象存储 |

---

## 🔧 配置说明

### 环境变量

核心服务支持以下环境变量配置（`.env` 文件）：

```env
# 数据库配置
DB_HOST=mysql
DB_PORT=3306
DB_USER=root
DB_PASSWORD=rootpassword
DB_NAME=omni_video

# Redis 配置
REDIS_HOST=redis
REDIS_PORT=6379

# JWT 配置
JWT_SECRET=your-secret-key-change-in-production
JWT_EXPIRE_HOURS=24

# 下载引擎配置
DOWNLOAD_ENGINE_URL=http://download-engine:8080

# AI 配置
AI_MODEL_PATH=/models/qwen3vl
AI_API_KEY=your-api-key

# MinIO 配置
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=omni-video

# 下载配置
DOWNLOAD_PATH=/app/downloads
CACHE_PATH=/app/cache
MAX_CONCURRENT_DOWNLOADS=3
```

---

## 📐 设计模式

### 工厂模式 - 视频解析器

```python
# 解析器工厂根据平台自动选择对应解析器
factory = ParserFactory()
parser = factory.get_parser("douyin")  # 获取抖音解析器
result = await parser.parse(url)        # 解析视频
```

每个平台的解析器继承自 `BaseParser` 抽象基类，实现统一的 `parse()` 接口：

- `DouyinParser` - 抖音解析器
- `BilibiliParser` - B站解析器
- `XiaohongshuParser` - 小红书解析器

新增平台只需：
1. 继承 `BaseParser`
2. 实现 `parse()` 方法
3. 在 `ParserFactory` 中注册

### Context 模式 - 下载控制

Go 下载引擎使用 `context.Context` 实现真正的取消和暂停：

```go
ctx, cancel := context.WithCancel(context.Background())

// 取消下载
cancel()

// 暂停：在下载循环中检查状态
for {
    if task.Status == "paused" {
        time.Sleep(time.Second)
        continue
    }
    // 下载数据...
}
```

---

## 🔒 安全特性

- **JWT 认证**：无状态 token 认证，支持过期自动失效
- **密码加密**：bcrypt 算法加密存储
- **CORS 防护**：可配置跨域白名单
- **请求限流**：Nginx 层限流防护
- **输入校验**：Pydantic 模型严格校验

---

## 📊 性能优化

### 前端

- **路由懒加载**：按需加载页面组件
- **组件缓存**：KeepAlive 缓存常用组件
- **图片懒加载**：IntersectionObserver 实现
- **请求防抖**：搜索输入防抖处理

### 后端

- **异步 I/O**：FastAPI + aiomysql 全异步
- **连接池**：数据库连接池复用
- **Redis 缓存**：热点数据缓存
- **Gzip 压缩**：Nginx 层响应压缩

### 下载引擎

- **分块下载**：多线程并行下载
- **缓冲优化**：64KB 读写缓冲区
- **限速控制**：可配置下载速度上限

---

## 🐛 常见问题

### Q: Docker 镜像拉取失败？

配置 Docker 镜像加速器：

```bash
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": [
    "https://docker.1ms.run",
    "https://docker.xuanyuan.me"
  ]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```

### Q: 前端无法连接后端 API？

检查 Nginx 配置中的代理设置，确保 `/api` 路径正确转发到核心服务。

### Q: 下载速度慢？

- 检查网络连接
- 调整 `MAX_CONCURRENT_DOWNLOADS` 配置
- 确认下载源服务器带宽

---

## 📋 开发路线图

- [x] 基础项目架构搭建
- [x] 抖音/B站/小红书解析器
- [x] Go 下载引擎（暂停/继续/取消）
- [x] JWT 用户认证
- [x] AI 视频分析接口
- [x] Web 前端（Vue3）
- [x] 微信小程序（Taro3）
- [x] Docker Compose 一键部署
- [ ] 快手/YouTube 平台支持
- [ ] WebSocket 实时进度推送
- [ ] 用户下载历史持久化
- [ ] 视频转码服务
- [ ] 分布式部署支持

---

## 🙏 参考项目

本项目参考了以下开源项目的优秀设计：

| 项目 | 说明 |
|------|------|
| [Evil0ctal/Douyin_TikTok_Download_API](https://github.com/Evil0ctal/Douyin_TikTok_Download_API) | 抖音/TikTok 无水印视频下载 API |
| [iuroc/bilidown](https://github.com/iuroc/bilidown) | B站视频下载工具 |
| [liu-ziting/xhs-parser](https://github.com/liu-ziting/xhs-parser) | 小红书内容解析 |
| [AmbitiousJun/video-downloader-go](https://github.com/AmbitiousJun/video-downloader-go) | Go 语言视频下载器 |
| [wwwzhouhui/video-parser](https://github.com/wwwzhouhui/video-parser) | 多平台视频解析 |
| [develon2015/Youtube-dl-REST](https://github.com/develon2015/Youtube-dl-REST) | YouTube 下载 REST API |
| [gitchzh/Yeguo-IDM](https://github.com/gitchzh/Yeguo-IDM) | 视频下载管理器 |

---

## 📄 许可证

本项目基于 [MIT License](https://opensource.org/licenses/MIT) 开源。

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request
