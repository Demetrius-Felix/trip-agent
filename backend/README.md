# 🧠 Trip Agent — 智能旅行规划系统

基于 **LangChain + FastAPI + SQLAlchemy + aiomysql + Chroma** 构建的智能旅行规划 Agent 系统。

该系统采用 **Agent 驱动架构**，支持：

* 🔎 RAG 向量检索
* 🧰 Tool 自动决策调用
* 🧠 会话记忆（多轮对话）
* 💾 会话持久化存储
* ⚡ 异步数据库操作

---

# 🚀 技术栈

| 模块       | 技术             |
| -------- | -------------- |
| Web 框架   | FastAPI        |
| Agent 框架 | LangChain      |
| 向量数据库    | Chroma         |
| ORM      | SQLAlchemy 2.0 |
| MySQL 驱动 | aiomysql       |
| 数据库      | MySQL 8+       |
| 数据校验     | Pydantic v2    |

---

# 🏗 系统架构

```
trip_agent/
│
├── app/                 # FastAPI 入口层（外壳）
│   ├── main.py
│   └── api/
│
├── agent/               # Agent 核心逻辑
│   ├── agent.py
│   ├── planner.py
│   └── prompt.py
│
├── tools/               # 工具层（插件式扩展）
│   ├── base.py
│   └── rag_tool.py
│
├── rag/                 # RAG 模块
│   ├── embedding.py
│   ├── retriever.py
│   └── vector_store.py
│
├── memory/              # 会话记忆管理
│   └── memory_manager.py
│
├── models/              # SQLAlchemy ORM
│   ├── base.py
│   ├── sessions.py
│   └── messages.py
│
├── core/                # 基础设施层
│   ├── config.py
│   ├── database.py
│   └── logger.py
│
└── tests/
```

---

# 🧠 系统设计理念

## 1️⃣ Agent 为核心

FastAPI 只是接口层，真正的业务逻辑全部在 Agent 内部完成：

* 自动规划
* Tool 决策
* 上下文拼接
* 推理执行

---

## 2️⃣ Tool 插件化设计

所有能力都通过 Tool 注册：

```python
tools = [
    RagTool(),
    WeatherTool(),
    MapTool(),
]
```

Agent 根据模型输出自动决定是否调用 Tool。

---

## 3️⃣ RAG 作为知识层

* 向量存储使用 Chroma
* 支持语义检索
* 可扩展为多知识库架构

---

## 4️⃣ 会话记忆机制

支持：

* 多轮对话
* 历史消息持久化
* Token 控制
* 滑动窗口
* 摘要压缩（可扩展）

---

# 📦 功能特性

* ✅ 多轮对话支持
* ✅ 会话持久化
* ✅ RAG 检索增强
* ✅ Agent 自动工具调用
* ✅ 异步数据库操作
* ✅ 可扩展 Tool 架构

---

# 💾 数据存储设计

当前持久化内容：

* sessions（会话）
* messages（对话记录）

向量数据存储于：

* Chroma 本地持久化目录

---

# 🔄 请求流程

```
用户请求
   ↓
FastAPI
   ↓
Chat Service
   ↓
Memory 加载历史
   ↓
Agent 推理
   ↓
Tool 调用（可选）
   ↓
返回结果
   ↓
持久化消息
```

---

# 🛠 本地运行

## 1️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

## 2️⃣ 启动 MySQL

创建数据库：

```sql
CREATE DATABASE trip_db;
```

## 3️⃣ 启动服务

```bash
uvicorn app.main:app --reload
```

访问：

```
http://127.0.0.1:8000/docs
```

---

# 🔮 未来扩展方向

* 🔹 多 Agent 协作
* 🔹 Tool 执行可观测
* 🔹 任务分解（Planner / Executor 分离）
* 🔹 LangGraph 重构
* 🔹 WebSocket 流式响应
* 🔹 多用户权限系统
* 🔹 机票/酒店 API 接入

---

# 🧠 项目目标

打造一个：

> 具备自主规划能力的旅行智能体系统
> 而不是简单的问答机器人

---

# 📌 当前阶段定位

* 单实例 Agent
* 单用户或轻量多用户
* 本地 RAG
* 会话持久化

适合：

* 架构学习
* Agent 实验
* 工程能力提升

---

# 📄 License

MIT

