# TradingAgents-CN Docker 部署完整指南

**文档版本**: 1.0  
**更新日期**: 2026-05-25  
**适用版本**: v1.0.1  

---

## 📋 目录

1. [系统架构](#系统架构)
2. [环境要求](#环境要求)
3. [快速部署](#快速部署)
4. [详细配置](#详细配置)
5. [服务管理](#服务管理)
6. [故障排查](#故障排查)
7. [生产环境优化](#生产环境优化)

---

## 🏗️ 系统架构

### Docker 服务组成

```
┌─────────────────────────────────────────────────────┐
│              Docker Compose 编排                      │
│                                                      │
│  ┌──────────────┐    ┌──────────────┐               │
│  │   Frontend   │───▶│   Backend    │               │
│  │  Vue 3 +     │    │   FastAPI    │               │
│  │  Nginx:80    │    │  Uvicorn:8000│               │
│  └──────────────┘    └──────┬───────┘               │
│                              │                        │
│                    ┌─────────┴─────────┐             │
│                    │                   │             │
│              ┌─────▼─────┐      ┌─────▼─────┐       │
│              │ MongoDB   │      │   Redis   │       │
│              │  mongo:4.4│      │ redis:7   │       │
│              │  :27017   │      │  :6379    │       │
│              └───────────┘      └───────────┘       │
│                                                      │
│  可选管理服务:                                         │
│  - Redis Commander (:8081)                          │
│  - Mongo Express (:8082)                            │
└─────────────────────────────────────────────────────┘
```

### 端口映射

| 服务 | 容器端口 | 宿主机端口 | 说明 |
|------|---------|-----------|------|
| **Frontend** | 80 | 3000 | Vue 3 前端 |
| **Backend** | 8000 | 8000 | FastAPI 后端 |
| **MongoDB** | 27017 | 27017 | 数据库 |
| **Redis** | 6379 | 6379 | 缓存 |
| **Redis Commander** | 8081 | 8081 | Redis 管理 (可选) |
| **Mongo Express** | 8081 | 8082 | MongoDB 管理 (可选) |

---

## 💻 环境要求

### 必需软件

```bash
# Docker (版本 >= 20.10)
docker --version
Docker version 20.10.21, build baeda1f

# Docker Compose (版本 >= 2.0)
docker-compose --version
Docker Compose version v2.10.2

# 或者使用 docker compose (新版本)
docker compose version
Docker Compose version v2.20.0
```

### 硬件要求

| 组件 | 最低配置 | 推荐配置 |
|------|---------|---------|
| **CPU** | 2 核 | 4 核+ |
| **内存** | 4 GB | 8 GB+ |
| **磁盘** | 20 GB | 50 GB+ SSD |
| **网络** | 10 Mbps | 100 Mbps+ |

### 支持的架构

- ✅ **amd64** (x86_64, Intel/AMD)
- ✅ **arm64** (Apple Silicon, AWS Graviton, 树莓派 4)

---

## 🚀 快速部署

### 步骤 1: 克隆项目

```bash
git clone https://github.com/hsliuping/TradingAgents-CN.git
cd TradingAgents-CN
```

---

### 步骤 2: 配置环境变量

```bash
# 复制环境配置模板
cp .env.example .env

# 编辑配置文件
vim .env  # 或使用你喜欢的编辑器
```

**最少配置** (仅填充必需项):

```bash
# === 必需配置 ===
MONGODB_HOST=mongodb
MONGODB_PORT=27017
MONGODB_USERNAME=admin
MONGODB_PASSWORD=tradingagents123
MONGODB_DATABASE=tradingagents

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=tradingagents123

JWT_SECRET=your-super-secret-jwt-key-change-in-production
CSRF_SECRET=your-csrf-secret-key-change-in-production

# === 至少配置一个 LLM ===
DEEPSEEK_API_KEY=sk-your-deepseek-api-key
DEEPSEEK_BASE_URL=https://api.deepseek.com

# === Docker 环境标识 ===
DOCKER_CONTAINER=true
```

**快速生成密钥**:

```bash
# 生成 JWT_SECRET
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# 生成 CSRF_SECRET
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

### 步骤 3: 启动服务

```bash
# 方式 1: 使用 docker-compose (旧版本)
docker-compose up -d

# 方式 2: 使用 docker compose (新版本推荐)
docker compose up -d

# 查看启动日志
docker compose logs -f
```

---

### 步骤 4: 验证部署

```bash
# 检查服务状态
docker compose ps

# 应该看到所有服务都是 Up 状态
NAME                         STATUS         PORTS
tradingagents-backend        Up (healthy)   0.0.0.0:8000->8000/tcp
tradingagents-frontend       Up (healthy)   0.0.0.0:3000->80/tcp
tradingagents-mongodb        Up (healthy)   0.0.0.0:27017->27017/tcp
tradingagents-redis          Up (healthy)   0.0.0.0:6379->6379/tcp
```

**访问应用**:

```
🌐 前端界面: http://localhost:3000
🔧 后端 API: http://localhost:8000/docs (Swagger UI)
📊 健康检查: http://localhost:8000/api/health
```

---

## ⚙️ 详细配置

### 1. LLM 配置

**推荐配置** (性价比高):

```bash
# DeepSeek (推荐，性价比极高)
DEEPSEEK_API_KEY=sk-your-key
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_ENABLED=true

# 通义千问 (国产稳定)
DASHSCOPE_API_KEY=sk-your-key
```

**聚合渠道** (推荐，一个 Key 访问多模型):

```bash
# AIHubMix (推荐)
AIHUBMIX_API_KEY=sk-your-key
AIHUBMIX_BASE_URL=https://aihubmix.com/v1
```

---

### 2. 数据源配置

```bash
# AKShare (免费，推荐)
DEFAULT_CHINA_DATA_SOURCE=akshare

# Tushare (专业，需要 Token)
TUSHARE_TOKEN=your-tushare-token
TUSHARE_ENABLED=true

# FinnHub (美股数据)
FINNHUB_API_KEY=your-finnhub-key
```

---

### 3. 数据库配置

**Docker 环境专用配置** (已在 docker-compose.yml 中设置):

```bash
# MongoDB
TRADINGAGENTS_MONGODB_URL=mongodb://admin:tradingagents123@mongodb:27017/tradingagents?authSource=admin

# Redis
TRADINGAGENTS_REDIS_URL=redis://:tradingagents123@redis:6379

# 缓存策略
TRADINGAGENTS_CACHE_TYPE=redis
TA_CACHE_STRATEGY=integrated
```

---

### 4. 日志配置

```bash
# 日志级别
TRADINGAGENTS_LOG_LEVEL=INFO

# 日志路径 (Docker 容器内)
TRADINGAGENTS_LOG_DIR=/app/logs
TRADINGAGENTS_LOG_FILE=/app/logs/tradingagents.log

# Docker 日志驱动 (已在 docker-compose.yml 配置)
# json-file, max-size: 100m, max-file: 3
```

---

### 5. 性能调优

```bash
# 连接池配置
MONGO_MAX_CONNECTIONS=100
MONGO_MIN_CONNECTIONS=10
REDIS_MAX_CONNECTIONS=20

# 超时配置 (毫秒)
MONGO_CONNECT_TIMEOUT_MS=30000
MONGO_SOCKET_TIMEOUT_MS=60000

# 缓存
CACHE_TTL=3600  # 1 小时
SESSION_EXPIRE_HOURS=24
```

---

## 🔧 服务管理

### 启动/停止服务

```bash
# 启动所有服务
docker compose up -d

# 停止所有服务
docker compose down

# 停止并删除数据卷 (⚠️ 会删除数据库数据)
docker compose down -v

# 重启特定服务
docker compose restart backend
docker compose restart frontend
```

---

### 查看日志

```bash
# 查看所有服务日志
docker compose logs -f

# 查看特定服务日志
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f mongodb

# 查看最近 100 行日志
docker compose logs --tail=100 backend
```

---

### 进入容器

```bash
# 进入后端容器
docker compose exec backend bash

# 进入 MongoDB 容器
docker compose exec mongodb mongosh -u admin -p tradingagents123

# 进入 Redis 容器
docker compose exec redis redis-cli -a tradingagents123
```

---

### 数据库管理

**MongoDB 操作**:

```bash
# 连接到 MongoDB
docker compose exec mongodb mongosh -u admin -p tradingagents123

# 查看数据库
show dbs

# 切换到应用数据库
use tradingagents

# 查看集合
show collections

# 查看用户信息
db.users.find().pretty()

# 查看分析结果
db.analysis_results.find().limit(10).pretty()
```

**Redis 操作**:

```bash
# 连接到 Redis
docker compose exec redis redis-cli -a tradingagents123

# 查看所有键
keys *

# 查看缓存
get cache:stock:000001

# 清除缓存
flushdb

# 查看内存使用
info memory
```

---

### 数据备份

**MongoDB 备份**:

```bash
# 备份到本地
docker compose exec mongodb mongodump \
  -u admin -p tradingagents123 \
  --out /tmp/backup

# 复制到宿主机
docker cp tradingagents-mongodb:/tmp/backup ./mongodb-backup-$(date +%Y%m%d)

# 恢复数据
docker cp ./mongodb-backup tradingagents-mongodb:/tmp/restore
docker compose exec mongodb mongorestore \
  -u admin -p tradingagents123 \
  /tmp/restore
```

**Redis 备份**:

```bash
# Redis 自动持久化 (AOF)
# 数据保存在 redis_data 卷中

# 手动备份
docker compose exec redis redis-cli -a tradingagents123 BGSAVE

# 查看持久化状态
docker compose exec redis redis-cli -a tradingagents123 INFO persistence
```

---

## 🐛 故障排查

### 1. 服务启动失败

**检查日志**:

```bash
docker compose logs backend
```

**常见问题**:

#### 问题 1: MongoDB 连接失败

```
Error: MongoDB connection failed
```

**解决方案**:
```bash
# 检查 MongoDB 是否运行
docker compose ps mongodb

# 检查网络连接
docker compose exec backend ping mongodb

# 验证凭据
docker compose exec mongodb mongosh -u admin -p tradingagents123
```

---

#### 问题 2: 端口冲突

```
Error: port is already allocated
```

**解决方案**:
```bash
# 查看端口占用
lsof -i :8000
lsof -i :3000
lsof -i :27017

# 修改 docker-compose.yml 中的端口映射
ports:
  - "8001:8000"  # 改为 8001
```

---

#### 问题 3: 内存不足

```
Error: Cannot allocate memory
```

**解决方案**:
```bash
# 查看内存使用
docker stats

# 限制容器内存 (docker-compose.yml)
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 2G
```

---

### 2. 后端健康检查失败

**检查健康状态**:

```bash
docker compose ps
```

**手动测试健康端点**:

```bash
curl http://localhost:8000/api/health
```

**可能原因**:

1. **数据库未就绪**: 等待 MongoDB/Redis 完全启动
2. **环境变量错误**: 检查 `.env` 文件
3. **依赖未安装**: 查看启动日志

---

### 3. 前端无法连接后端

**检查配置**:

```bash
# 前端环境变量
docker compose exec frontend env | grep API

# 应该看到
VITE_API_BASE_URL=http://localhost:8000
```

**测试后端连接**:

```bash
# 从前端容器测试
docker compose exec frontend wget -qO- http://backend:8000/api/health
```

**解决方案**:

修改 `docker-compose.yml`:
```yaml
frontend:
  environment:
    VITE_API_BASE_URL: "http://backend:8000"  # 使用容器名
```

---

### 4. LLM API 调用失败

**检查日志**:

```bash
docker compose logs backend | grep -i "llm\|api\|error"
```

**测试 API Key**:

```bash
# 进入后端容器
docker compose exec backend bash

# 测试 DeepSeek API
curl https://api.deepseek.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -d '{"model":"deepseek-chat","messages":[{"role":"user","content":"Hello"}]}'
```

---

### 5. 数据源获取失败

**检查数据源配置**:

```bash
docker compose exec backend python -c "
from tradingagents.dataflows.interface import get_china_stock_info_unified
print(get_china_stock_info_unified('000001'))
"
```

**切换数据源**:

```bash
# 修改 .env
DEFAULT_CHINA_DATA_SOURCE=akshare  # 或 tushare, baostock

# 重启后端
docker compose restart backend
```

---

## 🚀 生产环境优化

### 1. 安全加固

**修改默认密码**:

```bash
# .env 文件
MONGODB_PASSWORD=your-strong-password
REDIS_PASSWORD=your-strong-password
JWT_SECRET=your-random-secret
CSRF_SECRET=your-random-secret
```

**限制外部访问**:

```yaml
# docker-compose.yml
services:
  mongodb:
    ports:
      - "127.0.0.1:27017:27017"  # 仅本地访问
  
  redis:
    ports:
      - "127.0.0.1:6379:6379"
```

---

### 2. 性能优化

**增加连接池**:

```bash
MONGO_MAX_CONNECTIONS=200
REDIS_MAX_CONNECTIONS=50
```

**使用 Redis 缓存**:

```bash
TA_CACHE_STRATEGY=integrated
TRADINGAGENTS_CACHE_TYPE=redis
```

**优化 Docker 资源**:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 4G
        reservations:
          cpus: '2'
          memory: 2G
```

---

### 3. 高可用部署

**使用外部数据库**:

```bash
# .env
MONGODB_HOST=your-external-mongodb
REDIS_HOST=your-external-redis

# docker-compose.yml (移除 mongodb 和 redis 服务)
```

**多实例部署**:

```bash
# 使用 Docker Swarm 或 Kubernetes
docker swarm init
docker stack deploy -c docker-compose.yml tradingagents
```

---

### 4. 监控配置

**添加健康检查**:

```yaml
services:
  backend:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
```

**集成 Prometheus**:

```yaml
# 添加 Prometheus 服务
prometheus:
  image: prom/prometheus
  ports:
    - "9090:9090"
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml
```

---

### 5. 日志管理

**集中日志收集**:

```yaml
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "100m"
        max-file: "5"
```

**使用 ELK Stack**:

```yaml
elasticsearch:
  image: elasticsearch:8.10.0
  environment:
    - discovery.type=single-node

kibana:
  image: kibana:8.10.0
  ports:
    - "5601:5601"
```

---

## 📦 更新部署

### 方式 1: 拉取最新镜像

```bash
# 拉取最新代码
git pull origin main

# 重新构建并启动
docker compose up -d --build

# 清理无用镜像
docker image prune -f
```

### 方式 2: 使用预构建镜像

```bash
# 从 Docker Hub 拉取
docker pull tradingagents/backend:latest
docker pull tradingagents/frontend:latest

# 修改 docker-compose.yml
services:
  backend:
    image: tradingagents/backend:latest
    # build: ...  # 注释掉 build
```

---

## 🎯 常用命令速查

```bash
# === 基础操作 ===
docker compose up -d              # 启动
docker compose down               # 停止
docker compose restart            # 重启
docker compose ps                 # 状态

# === 日志 ===
docker compose logs -f            # 查看所有日志
docker compose logs -f backend    # 查看后端日志
docker compose logs --tail=100    # 最近 100 行

# === 进入容器 ===
docker compose exec backend bash  # 进入后端
docker compose exec frontend sh   # 进入前端
docker compose exec mongodb mongosh # 进入 MongoDB

# === 数据库 ===
docker compose exec mongodb mongosh -u admin -p tradingagents123
docker compose exec redis redis-cli -a tradingagents123

# === 更新 ===
docker compose up -d --build      # 重新构建
docker compose pull               # 拉取最新镜像
docker image prune -f             # 清理镜像

# === 备份 ===
docker cp tradingagents-mongodb:/tmp/backup ./backup
docker compose exec redis redis-cli -a tradingagents123 BGSAVE
```

---

## 📊 访问地址汇总

| 服务 | 地址 | 说明 |
|------|------|------|
| **前端应用** | http://localhost:3000 | 主界面 |
| **后端 API** | http://localhost:8000 | REST API |
| **API 文档** | http://localhost:8000/docs | Swagger UI |
| **健康检查** | http://localhost:8000/api/health | 健康状态 |
| **Redis 管理** | http://localhost:8081 | Redis Commander (可选) |
| **MongoDB 管理** | http://localhost:8082 | Mongo Express (可选) |

---

## 🆘 获取帮助

**遇到问题?**

1. **查看日志**: `docker compose logs -f`
2. **检查文档**: [项目文档](../docs/)
3. **提交 Issue**: [GitHub Issues](https://github.com/hsliuping/TradingAgents-CN/issues)
4. **联系社区**: 
   - QQ 群: 1091917201
   - 微信公众号: TradingAgents-CN

---

**文档生成**: BMad Docker 部署指南  
**适用版本**: v1.0.1  
**维护者**: TradingAgents-CN 团队
