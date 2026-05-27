# Harness 环境配置

> 锁定依赖版本,确保开发环境一致性。

---

## 🐍 Python 依赖

### 核心依赖 (必须锁定版本)
```
fastapi==0.115.6
uvicorn==0.34.0
pydantic==2.10.4
pymongo==4.10.1
redis==5.2.1
langchain==0.3.14
langchain-openai==0.3.1
langchain-anthropic==0.3.3
nest-asyncio==1.6.0
```

### 数据源依赖
```
akshare==1.15.73
baostock==0.8.9
tushare==1.4.21
```

### 完整依赖清单
见 `requirements-lock.txt` (已锁定所有依赖及子依赖版本)

### Python 版本
- **开发环境**: 3.10+
- **Docker 镜像**: python:3.10-slim-bookworm
- **锁定文件**: `.python-version`

---

## 🟢 Node.js 依赖

### 前端依赖
- **Node 版本**: 18+ (见 `frontend/.nvmrc` 或 `frontend/package.json`)
- **包管理器**: Yarn
- **锁定文件**: `frontend/yarn.lock`

### 核心依赖
```json
{
  "vue": "^3.5.0",
  "typescript": "^5.6.0",
  "vite": "^6.0.0",
  "axios": "^1.7.0",
  "pinia": "^2.3.0",
  "vue-router": "^4.5.0"
}
```

---

## 🐳 Docker 环境

### 基础镜像
```dockerfile
# Backend
FROM python:3.10-slim-bookworm

# Frontend (构建阶段)
FROM node:18-alpine

# Frontend (运行阶段)
FROM nginx:alpine
```

### Docker Compose 版本
- **文件格式**: Compose Specification (已移除 `version` 字段)
- **服务**:
  - backend: v1.0.0-preview
  - frontend: v1.0.0-preview
  - mongodb: mongo:4.4
  - redis: redis:7-alpine

### 端口映射
```
Frontend: 3000:80
Backend:  8000:8000 (内部,不对外)
MongoDB:  27017:27017
Redis:    6379:6379
```

---

## 🔧 开发工具版本

### 必需工具
```
Docker:         24.0+
Docker Compose: 2.20+
Python:         3.10+
Node.js:        18+
Git:            2.40+
MongoDB Shell:  4.4 (mongo 命令,不是 mongosh)
```

### 推荐工具
```
VS Code:        1.85+
  扩展:
  - Python
  - Pylance
  - Vue Language Features (Volar)
  - Docker
  - MongoDB for VS Code

Postman/Insomnia: API 测试
```

---

## 📦 环境初始化

### 1. 克隆项目
```bash
git clone <repository-url>
cd TradingAgents-CN
```

### 2. 配置环境
```bash
# 复制环境配置
cp .env.docker .env

# 编辑 .env,填入 API Keys
vim .env
```

### 3. 启动服务
```bash
# 首次启动 (构建镜像)
docker compose up -d --build

# 后续启动
docker compose up -d
```

### 4. 验证环境
```bash
# 检查服务状态
docker compose ps

# 检查后端健康
curl http://localhost:3000/api/health

# 检查前端
curl http://localhost:3000
```

### 5. 初始化数据库
```bash
# 数据库会自动初始化,无需手动操作
# 默认会创建:
# - admin 用户 (admin/admin123)
# - LLM 配置 (阿里云百炼 + DeepSeek)
```

---

## 🔒 版本锁定策略

### Python 依赖
```bash
# 锁定所有依赖
pip freeze > requirements-lock.txt

# 使用 uv (推荐)
uv pip compile pyproject.toml -o requirements-lock.txt
```

### Node 依赖
```bash
# Yarn 自动锁定
yarn install
# 生成 yarn.lock
```

### Docker 镜像
```bash
# 锁定镜像版本
docker pull python:3.10-slim-bookworm
docker pull nginx:alpine
docker pull mongo:4.4
docker pull redis:7-alpine
```

---

## ⚠️ 版本升级流程

### 原则
1. **小版本升级**: 测试后直接升级
2. **大版本升级**: 先在开发环境验证,再升级到生产
3. **破坏性升级**: 必须有回滚方案

### Python 依赖升级
```bash
# 1. 更新 pyproject.toml 中的版本
vim pyproject.toml

# 2. 重新锁定依赖
uv pip compile pyproject.toml -o requirements-lock.txt

# 3. 重新构建镜像
docker compose up -d --build backend

# 4. 运行测试
docker compose exec backend pytest tests/

# 5. 验证服务
curl http://localhost:3000/api/health
```

### Node 依赖升级
```bash
# 1. 更新 package.json
cd frontend
vim package.json

# 2. 更新依赖
yarn upgrade

# 3. 重新构建
cd ..
docker compose up -d --build frontend

# 4. 验证
curl http://localhost:3000
```

---

## 🐛 环境故障排查

### Python 依赖冲突
```bash
# 检查已安装的包
docker compose exec backend pip list

# 检查特定包版本
docker compose exec backend pip show fastapi

# 重新安装依赖
docker compose exec backend pip install -r requirements.txt
```

### Node 依赖问题
```bash
# 清理缓存
cd frontend
rm -rf node_modules
yarn cache clean
yarn install

# 检查依赖
yarn list --depth=0
```

### Docker 环境问题
```bash
# 清理所有容器
docker compose down -v

# 清理镜像
docker compose down --rmi local

# 完全重建
docker compose up -d --build --force-recreate
```

---

## 📊 环境检查清单

每次开发前检查:

- [ ] Python 版本 >= 3.10
- [ ] Node 版本 >= 18
- [ ] Docker 版本 >= 24.0
- [ ] Docker Compose 版本 >= 2.20
- [ ] `.env` 文件存在
- [ ] 所有服务正常运行
- [ ] 数据库连接正常
- [ ] Redis 连接正常
- [ ] API Key 已配置

---

**最后更新**: 2026-05-25
**维护者**: AI 助手 + 项目管理员
