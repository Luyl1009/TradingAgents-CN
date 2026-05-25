# TradingAgents-CN 项目文档索引

**最后更新**: 2026-05-25  
**项目版本**: v1.0.1  

---

## 📚 文档概览

本文档索引整理了 TradingAgents-CN 项目的所有关键文档，帮助你快速找到所需信息。

---

## 🎯 快速开始

### 新用户入门
1. [快速入门指南](../docs/QUICK_START.md) - 5 分钟快速开始
2. [v1.0.0 快速入门视频](https://www.bilibili.com/video/BV1i2CeBwEP7/) - B 站视频教程
3. [数据库设置指南](../docs/database_setup.md) - 数据库配置

### 部署文档
1. [Docker 部署指南](https://mp.weixin.qq.com/s/JkA0cOu8xJnoY_3LC5oXNw) - 推荐部署方式
2. [本地安装指南](https://mp.weixin.qq.com/s/cqUGf-sAzcBV19gdI4sYfA) - 源码安装
3. [绿色版安装指南](https://mp.weixin.qq.com/s/eoo_HeIGxaQZVT76LBbRJQ) - Windows 绿色版
4. [Docker 更新指南](https://mp.weixin.qq.com/s/WKYhW8J80Watpg8K6E_dSQ) - 镜像更新

### 使用手册
1. [v1.0.1 使用手册](../docs/guides/v1.0.1-user-manual.md)
2. [v1.0.1 发布说明](../docs/releases/v1.0.1-release-notes.md)
3. [升级指南](../docs/releases/upgrade-guide.md)

---

## 🏗️ 架构文档

### 系统架构
- [项目分析报告](./project-analysis.md) - **BMad 生成的完整分析**
- [架构文档目录](../docs/architecture/) - 架构设计文档
- [数据库版本隔离](../docs/deployment/database/DB_VERSION_ISOLATION_AND_PROVIDER_NORMALIZATION.md)

### 核心模块
- [多智能体系统](../docs/agents/) - 智能体架构
- [数据流设计](../docs/data/) - 数据处理流程
- [LLM 集成](../docs/llm/) - 大模型集成

---

## ⚙️ 配置文档

### 配置指南
- [配置指南目录](../docs/configuration/) - 所有配置文档
- [环境变量配置](../.env.example) - 环境变量示例
- [配置管理优化](../docs/releases/v1.0.1-release-notes.md) - v1.0.1 配置增强

### LLM 配置
- [LLM 配置指南](../docs/configuration/llm/) - 大模型配置
- [SiliconFlow 设置](../docs/SILICONFLOW_SETUP_GUIDE.md) - SiliconFlow 配置
- [LLM 适配器模板](../docs/LLM_ADAPTER_TEMPLATE.py) - 自定义适配器

---

## 🚀 开发与部署

### 开发文档
- [开发文档目录](../docs/development/) - 开发指南
- [构建指南](../docs/BUILD_GUIDE.md) - 项目构建
- [测试环境设置](../docs/test_environment_setup.md) - 测试配置

### 部署文档
- [部署文档目录](../docs/deployment/) - 部署指南
- [Docker 多架构构建](../docs/docker-multiarch-build.md)
- [Docker 报告导出](../docs/docker-report-export.md)
- [Nginx 配置](../docker/nginx.conf)

### CI/CD
- [GitHub Actions 工作流](../.github/workflows/) - 自动化构建

---

## 📖 功能文档

### 核心功能
- [功能文档目录](../docs/features/) - 功能说明
- [分析功能](../docs/analysis/) - 股票分析
- [前端功能](../docs/frontend/) - 前端特性

### 企业功能
- [用户管理](../scripts/USER_MANAGEMENT.md)
- [配置管理](../docs/configuration/)
- [缓存管理](../docs/deployment/)
- [通知系统](../docs/features/)

---

## 🔧 运维与维护

### 运维文档
- [维护文档目录](../docs/maintenance/) - 运维指南
- [上游同步策略](../docs/maintenance/upstream-sync.md)
- [上游吸收清单](../docs/maintenance/manual-upstream-absorption-checklist.md)

### 数据库运维
- [数据库版本隔离](../docs/deployment/database/DB_VERSION_ISOLATION_AND_PROVIDER_NORMALIZATION.md)

### 脚本工具
- [脚本目录](../scripts/) - 371 个运维脚本
  - 部署脚本 (`deployment/`)
  - 开发脚本 (`development/`)
  - Docker 脚本 (`docker/`)
  - 维护脚本 (`maintenance/`)
  - 安装脚本 (`setup/`)
  - 启动脚本 (`startup/`)
  - 验证脚本 (`validation/`)

---

## 🐛 故障排除

### 常见问题
- [FAQ 目录](../docs/faq/) - 常见问题解答
- [故障排除目录](../docs/troubleshooting/) - 问题排查
- [Bug 修复目录](../docs/bugfix/) - 已知 Bug 修复

### 特定问题
- [MongoDB Docker 问题](../docs/troubleshooting-mongodb-docker.md)
- [配置验证修复](../docs/CONFIG_VALIDATION_FIX_SUMMARY.md)
- [错误处理改进](../docs/error-handling-improvement.md)

---

## 📝 发布说明

### 版本历史
- [发布说明目录](../docs/releases/) - 所有版本发布
- [更新日志](../docs/releases/CHANGELOG.md) - 完整更新历史
- [v1.0.1 发布说明](../docs/releases/v1.0.1-release-notes.md) - 最新版本

### 版本对比
- [技术栈升级对比](../README.md#技术栈升级) - v0.1.x vs v1.0.1

---

## 🎓 学习与教程

### 学习中心
- [学习文档目录](../docs/learning/) - 学习教程
- [实战教程](../examples/) - 示例代码
- [技术分析原理](../docs/analysis/) - 分析原理

### 最佳实践
- [配置最佳实践](../docs/configuration/)
- [部署最佳实践](../docs/deployment/)
- [开发最佳实践](../docs/development/)

---

## 🌐 本地化

### 中文增强
- [本地化文档](../docs/localization/) - 本地化说明
- [A 股数据支持](../docs/data/) - A 股数据配置
- [国产 LLM 支持](../docs/llm/) - 国产大模型

---

## 🤝 贡献指南

### 贡献文档
- [贡献者名单](../CONTRIBUTORS.md)
- [贡献指南](../README.md#贡献指南)
- [GitHub 分支保护](../docs/GITHUB_BRANCH_PROTECTION.md)

---

## 📋 许可证与合规

### 许可证文档
- [主许可证](../LICENSE) - Apache 2.0
- [版权声明](../COPYRIGHT.md) - 版权声明
- [商业许可证](../COMMERCIAL_LICENSE_TEMPLATE.md) - 商业授权
- [后端许可证](../app/LICENSE) - 后端专有许可证
- [前端许可证](../frontend/LICENSE) - 前端专有许可证

---

## 🔍 项目分析

### BMad 分析文档
- [项目分析报告](./project-analysis.md) - **完整的项目分析**
- [项目结构](./project-structure.txt) - 目录结构

### 技术分析
- [API 密钥管理分析](../docs/API_KEY_MANAGEMENT_ANALYSIS.md)
- [API 密钥测试指南](../docs/API_KEY_TESTING_GUIDE.md)

---

## 📊 项目统计

| 类别 | 数量 | 说明 |
|------|------|------|
| 后端服务 | 37 个文件 | `app/services/` |
| API 路由 | 37 个文件 | `app/routers/` |
| 前端 API | 22 个文件 | `frontend/src/api/` |
| 前端视图 | 15 个文件 | `frontend/src/views/` |
| 智能体模块 | 7 个目录 | `tradingagents/agents/` |
| 图计算 | 7 个文件 | `tradingagents/graph/` |
| 数据流 | 15 个文件 | `tradingagents/dataflows/` |
| LLM 客户端 | 9 个文件 | `tradingagents/llm_clients/` |
| 运维脚本 | 371 个文件 | `scripts/` |
| 测试文件 | 292 个文件 | `tests/` |
| 文档文件 | 71+ 个 | `docs/` |
| 示例代码 | 25 个文件 | `examples/` |

---

## 🎯 下一步

### 推荐阅读顺序

**新用户**:
1. [快速入门](../docs/QUICK_START.md)
2. [使用手册](../docs/guides/v1.0.1-user-manual.md)
3. [配置指南](../docs/configuration/)

**开发者**:
1. [项目分析报告](./project-analysis.md)
2. [架构文档](../docs/architecture/)
3. [开发指南](../docs/development/)

**运维人员**:
1. [部署指南](../docs/deployment/)
2. [数据库设置](../docs/database_setup.md)
3. [维护文档](../docs/maintenance/)

---

## 📞 获取帮助

- **GitHub Issues**: [提交问题](https://github.com/hsliuping/TradingAgents-CN/issues)
- **邮箱**: hsliup@163.com
- **QQ 群**: 1091917201
- **微信公众号**: TradingAgents-CN

---

**文档生成**: BMad Document Project Workflow  
**最后更新**: 2026-05-25
