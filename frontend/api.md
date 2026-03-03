# Trip Agent API 文档

Base URL

```
http://127.0.0.1:8000
```

模块前缀

```
/chat
```

---

# 1. 创建会话

## POST `/chat/session`

### Query 参数

| 参数    | 类型     | 必填 | 说明   |
| ----- | ------ | -- | ---- |
| title | string | 否  | 会话标题 |

### 请求示例

```
POST /chat/session?title=东京旅行
```

### 成功响应

```json
{
  "session_id": 1,
  "title": "东京旅行"
}
```

### 错误响应

```json
{
  "detail": "错误信息"
}
```

---

# 2. 流式聊天

## POST `/chat/stream/{session_id}`

### 路径参数

| 参数         | 类型  | 必填 | 说明   |
| ---------- | --- | -- | ---- |
| session_id | int | 是  | 会话ID |

### Query 参数

| 参数    | 类型     | 必填 | 说明   |
| ----- | ------ | -- | ---- |
| query | string | 是  | 用户输入 |

### 请求示例

```
POST /chat/stream/1?query=帮我规划东京三日游
```

### 返回类型

```
Content-Type: text/plain
Transfer-Encoding: chunked
```

### 返回示例（流式）

```
好的，
我为你规划一个
东京三日游行程...
```

### 错误响应

#### 404

```json
{
  "detail": "Session not found"
}
```

#### 500

```json
{
  "detail": "错误信息"
}
```

---

# 3. 会话列表

## GET `/chat/session/list`

### Query 参数

| 参数        | 类型  | 必填 | 默认 | 说明   |
| --------- | --- | -- | -- | ---- |
| page      | int | 否  | 1  | 页码   |
| page_size | int | 否  | 20 | 每页条数 |

### 成功响应

```json
{
  "total": 2,
  "items": [
    {
      "session_id": 2,
      "title": "东京旅行",
      "created_at": "2026-03-03T10:00:00"
    },
    {
      "session_id": 1,
      "title": "你好",
      "created_at": "2026-03-02T20:00:00"
    }
  ]
}
```

---

# 4. 消息列表

## GET `/chat/message/list/{session_id}`

### 路径参数

| 参数         | 类型  | 必填 | 说明   |
| ---------- | --- | -- | ---- |
| session_id | int | 是  | 会话ID |

### Query 参数

| 参数    | 类型  | 必填 | 默认 | 说明     |
| ----- | --- | -- | -- | ------ |
| limit | int | 否  | 50 | 返回消息数量 |

### 成功响应

```json
{
  "session_id": 1,
  "messages": [
    {
      "id": 1,
      "role": "user",
      "content": "你好",
      "created_at": "2026-03-03T10:00:00"
    },
    {
      "id": 2,
      "role": "assistant",
      "content": "你好！有什么可以帮你？",
      "created_at": "2026-03-03T10:00:02"
    }
  ]
}
```

---

# 状态码说明

| 状态码 | 说明      |
| --- | ------- |
| 200 | 请求成功    |
| 404 | 资源不存在   |
| 500 | 服务器内部错误 |