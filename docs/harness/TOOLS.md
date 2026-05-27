# Harness 工具使用规范

> 定义 AI 助手可以调用的工具和命令,以及使用限制。

---

## ✅ 允许的工具和命令

### 1. 文件读取工具

#### 允许的操作
```
✅ read_file - 读取任何项目文件
✅ list_dir - 列出目录内容
✅ search_file - 搜索文件
✅ grep_code - 搜索代码内容
✅ lsp - 符号查找、引用查找
```

#### 使用规则
```
✅ 优先使用 read_file 读取完整文件
✅ 大文件使用 start_line/end_line 限制范围
✅ 使用 grep_code 进行精确搜索
✅ 使用 lsp 进行代码导航
```

---

### 2. 代码编辑工具

#### 允许的操作
```
✅ search_replace - 精确替换代码 (首选)
✅ create_file - 创建新文件或完全覆盖
```

#### 使用规则
```
✅ search_replace 必须提供唯一的 original_text
✅ original_text 必须包含足够的上下文
✅ 修改后必须验证语法正确性
✅ 禁止使用 edit_file (除非明确要求)
```

#### 禁止的操作
```
❌ 不修改已存在文件时使用 create_file
❌ 使用 search_replace 时 original_text 不唯一
❌ 创建文档文件 (.md) 除非明确要求
```

---

### 3. 终端命令工具

#### 允许的命令类别

**Docker 相关**
```bash
✅ docker compose up -d
✅ docker compose down
✅ docker compose restart <service>
✅ docker compose build <service>
✅ docker compose ps
✅ docker compose logs --tail=100 <service>
✅ docker compose logs --since="5m" <service>
✅ docker compose exec <service> <command>
✅ docker compose config  # 验证配置
```

**Git 相关**
```bash
✅ git status
✅ git log --oneline -10
✅ git diff --stat
✅ git diff <file>
✅ git add <file>
✅ git commit -m "<message>"
✅ git branch -a
✅ git checkout <branch>
✅ git pull
```

**Python 相关**
```bash
✅ python3 -m py_compile <file>  # 语法检查
✅ pytest tests/<test_file>.py -v  # 运行测试
✅ python3 -c "<code>"  # 快速执行 Python 代码
✅ pip list | grep <package>  # 检查包版本
✅ pip show <package>  # 查看包详情
```

**Node 相关**
```bash
✅ cd frontend && yarn install
✅ cd frontend && yarn build
✅ cd frontend && yarn lint
✅ cd frontend && yarn type-check
```

**文件操作**
```bash
✅ cat <file>  # 查看文件内容
✅ ls -la <directory>  # 列出文件
✅ find . -name "*.py" -type f  # 查找文件
✅ grep -n "pattern" <file>  # 搜索内容
✅ wc -l <file>  # 统计行数
```

**网络测试**
```bash
✅ curl http://localhost:3000/api/health  # 测试 API
✅ curl -X POST http://localhost:3000/api/... -d '{}'  # POST 请求
✅ wget -q -O- <url>  # 下载测试
```

---

### 4. 数据库工具

#### MongoDB 操作
```bash
✅ docker compose exec mongodb mongo -u admin -p tradingagents123 --authenticationDatabase admin --eval "<js>"

# 允许的操作:
✅ 查询数据: db.collection.find()
✅ 更新数据: db.collection.updateOne()
✅ 插入数据: db.collection.insertOne()
✅ 统计: db.collection.count()
✅ 创建索引: db.collection.createIndex()
```

#### Redis 操作
```bash
✅ docker compose exec redis redis-cli
✅ GET <key>
✅ SET <key> <value>
✅ KEYS <pattern>
✅ DEL <key>
```

---

## 🚫 禁止的命令

### 危险操作
```bash
❌ rm -rf <directory>  # 递归删除
❌ docker system prune -a  # 清理所有镜像
❌ docker volume prune -f  # 删除所有卷
❌ git push --force  # 强制推送
❌ sudo <command>  # 提权操作
❌ chmod 777 <file>  # 开放所有权限
❌ pip install --break-system-packages  # 破坏系统包
```

### 数据库危险操作
```bash
❌ db.collection.drop()  # 删除集合
❌ db.dropDatabase()  # 删除数据库
❌ db.collection.remove({})  # 删除所有文档
❌ 批量更新无确认: db.collection.updateMany({}, {$set: ...})
```

### Git 危险操作
```bash
❌ git reset --hard  # 强制重置
❌ git clean -fd  # 清理未跟踪文件
❌ git push --force  # 强制推送
❌ git rebase -i  # 交互式变基 (可能改写历史)
```

---

## 🔧 工具使用最佳实践

### 1. 代码搜索
```python
# ❌ 错误: 搜索过于宽泛
grep_code(regex="def ")

# ✅ 正确: 精确搜索
grep_code(regex="def get_stock_data\(", path="tradingagents/dataflows/")
```

### 2. 代码替换
```python
# ❌ 错误: original_text 不唯一
search_replace(
    original_text="return result",  # 文件中有多个这样的语句
    new_text="return result.strip()"
)

# ✅ 正确: 提供足够的上下文
search_replace(
    original_text="""
    logger.info(f"获取数据成功: {symbol}")
    return result
    """,
    new_text="""
    logger.info(f"获取数据成功: {symbol}, 共 {len(result)} 条")
    return result.strip()
    """
)
```

### 3. 文件读取
```python
# ❌ 错误: 读取整个大文件
read_file(file_path="large_file.py")  # 5000 行

# ✅ 正确: 只读取需要的部分
read_file(file_path="large_file.py", start_line=100, end_line=150)
```

### 4. 命令执行
```python
# ❌ 错误: 后台运行需要交互的命令
run_in_terminal(command="vim config.py", is_background=True)

# ✅ 正确: 使用非交互方式
run_in_terminal(command="echo 'config' > config.py", is_background=False)

# ✅ 正确: 长时间运行的服务使用后台
run_in_terminal(command="docker compose up -d", is_background=False)
run_in_terminal(command="tail -f logs/app.log", is_background=True)
```

---

## 📊 工具调用反馈

### 必须记录的信息

#### 成功操作
```
✅ 操作类型: 修改文件 / 执行命令 / 数据库操作
✅ 影响范围: 哪些文件/服务受影响
✅ 验证结果: 如何确认操作成功
```

#### 失败操作
```
❌ 错误信息: 完整的错误输出
❌ 可能原因: 分析失败原因
❌ 解决方案: 提供修复建议
❌ 回滚方案: 如何撤销操作
```

---

## 🔐 安全限制

### 环境变量保护
```
❌ 禁止在日志中输出完整的 API Key
❌ 禁止在代码中硬编码 API Key
✅ 可以显示 API Key 的前 15 个字符 + "..."
✅ 可以显示 API Key 的长度
```

### 文件权限
```
❌ 禁止修改 .gitignore 规则
❌ 禁止删除 .env 文件
❌ 禁止修改 Dockerfile 的基础镜像
✅ 可以添加新的忽略规则 (需说明原因)
```

### 数据保护
```
❌ 禁止导出包含用户数据的文件
❌ 禁止在日志中输出用户密码
✅ 可以统计用户数量
✅ 可以检查数据完整性
```

---

## 📝 工具使用日志

### 每次会话必须记录

```markdown
## 工具调用日志

### 文件修改
1. 文件: tradingagents/llm_clients/openai_client.py
   操作: search_replace
   原因: 修复 DeepSeek thinking 模式
   验证: Python 语法检查通过

### 命令执行
1. 命令: docker compose restart backend
   原因: 应用代码更改
   结果: 服务正常启动

### 数据库操作
1. 集合: llm_configs
   操作: updateOne
   原因: 添加 tool_calling 特性
   验证: 查询确认更新成功
```

---

## ⚠️ 常见陷阱

### 1. 工具调用失败
```
❌ 错误: 忽略失败,继续下一步
✅ 正确: 分析失败原因,提供解决方案
```

### 2. 命令超时
```
❌ 错误: 使用默认超时时间,导致长时间等待
✅ 正确: 设置合理的 timeout 参数
```

### 3. 后台命令混淆
```
❌ 错误: 前台命令设置为后台,无法获取输出
✅ 正确: 需要输出的命令使用 is_background=false
```

---

## 🎯 工具使用检查清单

每次调用工具前检查:

- [ ] 这个操作是否必要?
- [ ] 是否有更安全的方式?
- [ ] 是否会影响其他服务?
- [ ] 是否有回滚方案?
- [ ] 是否记录了操作日志?

---

**最后更新**: 2026-05-25
**维护者**: AI 助手 + 项目管理员
