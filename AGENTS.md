# AGENTS.md - AI 助手开发约定

> 本文档定义 AI 助手在本项目中必须遵循的开发规则和约定。
> **违反这些规则将导致代码质量问题和项目风险。**

---

## 📋 项目基本信息

- **项目名称**: TradingAgents-CN
- **技术栈**: FastAPI + Vue 3 + MongoDB + Redis + LangChain
- **架构**: 前后端分离,Docker Compose 编排
- **Python 版本**: 3.10+
- **Node 版本**: 18+

---

## 🚫 禁止操作 (MUST NOT)

### 1. 文件系统禁止
```
❌ 禁止删除任何 .md 文档(除非明确要求)
❌ 禁止修改 .env 文件中的 API Key(除非用户明确要求)
❌ 禁止删除 tests/ 目录下的任何测试文件
❌ 禁止修改 docker-compose.yml 的端口映射(除非用户要求)
```

### 2. 数据库操作禁止
```
❌ 禁止直接 drop 任何 MongoDB 集合
❌ 禁止修改已存在的数据库字段类型
❌ 禁止在没有备份的情况下批量更新数据
```

### 3. 代码修改禁止
```
❌ 禁止修改 tradingagents/llm_clients/ 的核心逻辑(除非修复 bug)
❌ 禁止删除任何现有的 API 路由
❌ 禁止修改已配置的 LLM 模型名称
❌ 禁止修改 Dockerfile 的基础镜像版本
```

### 4. 命令执行禁止
```
❌ 禁止执行 rm -rf 命令
❌ 禁止执行 docker system prune -a
❌ 禁止执行 git push --force
❌ 禁止执行任何需要 sudo 的命令
```

---

## ✅ 必须遵守 (MUST)

### 1. 代码修改规则
```
✅ 修改任何代码前,必须先说明修改原因和影响范围
✅ 修改后必须验证代码可以正常运行(至少语法检查)
✅ 新增功能必须添加对应的测试用例
✅ 修改配置文件必须提供回滚方案
```

### 2. 测试规则
```
✅ 任何功能修改后,必须运行相关测试
✅ 测试失败时,禁止宣布"任务完成"
✅ 新增 API 端点必须提供 curl 测试示例
✅ 数据库变更必须先创建备份
```

### 3. 文档规则
```
✅ 新增功能必须更新对应的文档
✅ 修改配置必须记录在 docs/ 目录
✅ Bug 修复必须记录在 docs/bugfix/ 目录
✅ 重要决策必须记录决策原因和备选方案
```

### 4. Docker 规则
```
✅ 修改 docker-compose.yml 后必须执行 docker compose config 验证
✅ 修改 Dockerfile 后必须重新构建镜像
✅ 新增服务必须在 .env.example 中添加环境变量示例
✅ 端口冲突时必须说明解决方案
```

---

## 🔧 工具调用限制

### 允许的命令
```bash
# Docker 相关
docker compose up -d
docker compose logs --tail=100
docker compose restart
docker compose build
docker compose ps

# Git 相关
git status
git log --oneline -10
git diff --stat
git add <file>
git commit -m "<message>"

# Python 相关
python3 -m py_compile <file>
pytest tests/<specific_test>.py -v
pip list | grep <package>

# 文件操作
cat <file>
grep -n "pattern" <file>
find . -name "*.py" -type f
ls -la <directory>
```

### 禁止的命令
```bash
rm -rf /
docker system prune -a
git push --force
sudo chmod 777
pip install --break-system-packages
```

---

## 📊 任务完成标准

### 必须满足以下条件才能宣布"完成"

1. **代码验证**
   ```
   ✅ Python 文件通过 py_compile 检查
   ✅ TypeScript 文件通过 tsc --noEmit 检查
   ✅ Docker Compose 配置通过 docker compose config 验证
   ```

2. **测试验证**
   ```
   ✅ 相关单元测试通过 (pytest)
   ✅ API 端点可以通过 curl 测试
   ✅ 数据库查询返回预期结果
   ```

3. **功能验证**
   ```
   ✅ 服务正常启动 (docker compose ps)
   ✅ API 返回 200 状态码
   ✅ 前端页面无报错
   ```

4. **文档更新**
   ```
   ✅ 修改记录已添加到对应文档
   ✅ 配置变更已记录
   ✅ 已知问题已说明
   ```

---

## 🐛 错误处理规则

### 遇到错误时的处理流程

1. **不要忽略错误**
   ```
   ❌ 错误: 直接宣布任务完成,忽略报错
   ✅ 正确: 分析错误原因,提供解决方案
   ```

2. **不要掩盖问题**
   ```
   ❌ 错误: 用 try-except 包裹所有代码,不处理异常
   ✅ 正确: 修复根本原因,添加适当的错误处理
   ```

3. **不要跳过验证**
   ```
   ❌ 错误: 说"应该可以了",但不实际测试
   ✅ 正确: 运行验证命令,确认问题解决
   ```

---

## 💾 状态持久化

### PROGRESS.md 更新规则

每次会话结束前,必须更新 `PROGRESS.md`:

```markdown
## [日期] 会话进度

### 已完成
- [x] 任务 1: 描述
- [x] 任务 2: 描述

### 进行中
- [ ] 任务 3: 描述 (进度 50%)

### 待办
- [ ] 任务 4: 描述

### 已知问题
- 问题 1: 描述 + 临时解决方案

### 重要决策
- 决策 1: 选择了方案 A,原因是 XXX
```

---

## 🎯 项目特定规则

### 1. LLM 配置
```
✅ 新增模型必须同时更新:
   - llm_providers 集合
   - llm_configs 集合
   - model_catalog 集合(可选)
   
✅ 修改模型配置后必须重启后端服务
✅ 测试 API Key 必须使用实际的 API 调用,不仅检查长度
```

### 2. 数据源管理
```
✅ 修改数据源优先级必须更新:
   - data_source_manager.py
   - 对应的数据库配置
   
✅ 新增数据源必须实现降级机制
✅ 异步数据源调用必须处理事件循环冲突(nest_asyncio)
```

### 3. API 开发
```
✅ 新增 API 必须在 app/routers/ 下创建路由文件
✅ 必须在 app/services/ 下实现业务逻辑
✅ 必须在 app/schemas/ 下定义请求/响应模型
✅ 必须添加操作日志记录
```

---

## ⚠️ 常见陷阱

### 1. 过早宣布胜利
```
❌ "代码已修改,任务完成" (但没测试)
✅ "代码已修改,测试通过,服务正常运行"
```

### 2. 上下文焦虑
```
❌ 长任务中赶进度,跳过验证步骤
✅ 即使任务很长,也要逐步验证每个步骤
```

### 3. 跨会话失忆
```
❌ 新会话中忘记之前的决策和约定
✅ 每次会话开始前阅读 PROGRESS.md 和 AGENTS.md
```

---

## 📞 紧急处理

### 如果发生严重错误

1. **立即停止操作**
2. **记录当前状态** (更新 PROGRESS.md)
3. **提供回滚方案**
4. **等待用户确认后再继续**

---

## 📝 版本历史

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| 1.0.0 | 2026-05-25 | 初始版本,定义基础规则 |

---

**最后更新**: 2026-05-25
**维护者**: AI 助手 + 项目管理员
