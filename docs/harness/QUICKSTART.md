# Harness 快速入门

> 5 分钟了解如何使用 Harness 系统

---

## 🎯 Harness 是什么?

Harness 是给 AI 助手的"缰绳",确保开发过程:
- ✅ 不犯错 (有规则约束)
- ✅ 不遗忘 (有状态记录)  
- ✅ 不敷衍 (有验证检查)

---

## 📁 文件结构

```
TradingAgents-CN/
├── AGENTS.md                      ← AI 助手规则 (必读!)
├── PROGRESS.md                    ← 项目进度 (每次更新!)
├── docs/harness/
│   ├── README.md                  ← Harness 总文档
│   ├── TOOLS.md                   ← 工具使用规范
│   └── ENVIRONMENT.md             ← 环境配置
└── scripts/harness/
    └── validate_changes.py        ← 验证脚本
```

---

## 🚀 快速开始

### 1. 开始新会话

```bash
# 第一步: 阅读规则
cat AGENTS.md

# 第二步: 查看当前进度
cat PROGRESS.md

# 第三步: 验证环境
python3 scripts/harness/validate_changes.py
```

### 2. 开发过程中

遵循 AGENTS.md 中的规则:
- ❌ 不做禁止的操作
- ✅ 做必须做的事情
- 📝 记录重要决策

### 3. 完成任务后

```bash
# 运行验证
python3 scripts/harness/validate_changes.py

# 必须看到:
# 🎉 所有检查通过! 代码可以提交。
```

### 4. 更新进度

在 PROGRESS.md 中添加:

```markdown
## [日期] 会话进度

### 已完成
- [x] 完成了 XXX

### 已知问题
- 问题 YYY (临时方案: ZZZ)
```

---

## 💡 核心规则 (Top 5)

### 🚫 绝对禁止

1. **不要删除文档** - `.md` 文件都不能删
2. **不要跳过测试** - 修改后必须验证
3. **不要掩盖错误** - 必须修复根本原因

### ✅ 必须做到

4. **记录进度** - 每次会话更新 PROGRESS.md
5. **验证通过才能宣布完成** - 退出码必须是 0

---

## 🔧 常用命令

### 验证环境
```bash
python3 scripts/harness/validate_changes.py
```

### 检查服务状态
```bash
docker compose ps
```

### 查看日志
```bash
docker compose logs --tail=50 backend
```

### 测试 API
```bash
curl http://localhost:3000/api/health
```

---

## ⚠️ 常见错误

### 错误 1: 过早宣布完成
```
❌ "代码改好了!" (但没测试)
✅ "代码改好了,验证通过: [输出]"
```

### 错误 2: 忽略错误
```
❌ "有点小问题,但不影响"
✅ "发现问题 XXX,正在修复"
```

### 错误 3: 忘记更新进度
```
❌ 任务完成了,但 PROGRESS.md 没更新
✅ 任务完成,立即更新 PROGRESS.md
```

---

## 📊 检查清单

每次开发前:

- [ ] 阅读了 AGENTS.md
- [ ] 查看了 PROGRESS.md
- [ ] 运行了 validate_changes.py
- [ ] 确认所有检查通过

每次开发后:

- [ ] 运行了验证脚本
- [ ] 更新了 PROGRESS.md
- [ ] 记录了重要决策
- [ ] 确认退出码为 0

---

## 🎓 学习路径

### Day 1: 了解规则
- 阅读 AGENTS.md
- 理解禁止操作和必须操作

### Day 2: 使用工具
- 阅读 TOOLS.md
- 了解允许和禁止的命令

### Day 3: 环境管理
- 阅读 ENVIRONMENT.md
- 学习版本锁定和升级

### Day 4: 状态跟踪
- 学习更新 PROGRESS.md
- 记录决策和问题

### Day 5: 自动化验证
- 运行 validate_changes.py
- 理解所有检查项

---

## 🤝 需要帮助?

1. **查看文档**: `docs/harness/README.md`
2. **检查规则**: `AGENTS.md`
3. **查看进度**: `PROGRESS.md`
4. **运行验证**: `python3 scripts/harness/validate_changes.py`

---

## 📝 示例: 完整的工作流程

### 场景: 修复一个 Bug

```bash
# 1. 开始前
cat AGENTS.md              # 了解规则
cat PROGRESS.md            # 查看当前进度
python3 scripts/harness/validate_changes.py  # 验证环境

# 2. 修复 Bug
# (遵循 AGENTS.md 规则)

# 3. 验证修复
python3 scripts/harness/validate_changes.py  # 必须通过!

# 4. 更新进度
vim PROGRESS.md            # 记录修复情况

# 5. 提交
git add .
git commit -m "fix: 修复 XXX bug"
```

---

**创建日期**: 2026-05-25
**版本**: 1.0.0
