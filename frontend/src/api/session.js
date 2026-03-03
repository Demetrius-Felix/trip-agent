import apiClient from './client';

export default {
  // 根据 api.md: POST /chat/session?title=...
  async createSession(userId, title = null) {
    const params = {};
    if (title) params.title = title;
    
    const response = await apiClient.post('/session', null, {
      params
    });
    // 适配返回格式: { session_id, title } -> { id: session_id, title } 以兼容组件
    return {
      id: response.data.session_id,
      title: response.data.title,
      created_at: new Date().toISOString() // 补充缺失字段
    };
  },

  // 根据 api.md: GET /chat/session/list?page=...&page_size=...
  async getUserSessions(userId) {
    const response = await apiClient.get('/session/list', {
      params: { 
        page: 1, 
        page_size: 20 
      }
    });
    // 适配返回格式: { items: [{ session_id, title, created_at }] } -> [{ id: session_id, ... }]
    return response.data.items.map(item => ({
      id: item.session_id,
      title: item.title,
      created_at: item.created_at
    }));
  },

  // 根据 api.md: GET /chat/message/list/{session_id}?limit=...
  async getSessionMessages(sessionId, limit = 50) {
    const response = await apiClient.get(`/message/list/${sessionId}`, {
      params: { limit }
    });
    // 适配返回格式: { messages: [{ id, role, content, created_at }] } -> [...]
    return response.data.messages;
  },

  // 文档中未定义删除接口
  async deleteSession(sessionId) {
    // const response = await apiClient.delete(`/sessions/${sessionId}`);
    // return response.data;
    console.warn('Delete session not supported by API');
    return Promise.resolve();
  }
};
