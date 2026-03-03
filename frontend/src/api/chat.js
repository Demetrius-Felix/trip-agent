import apiClient from './client';

export default {
  // SSE is handled directly in component using fetch/EventSource
  // but we might need helper methods here if we change to non-streaming
  
  async sendMessage(sessionId, message) {
    return apiClient.post('/chat', {
      session_id: sessionId,
      message: message
    });
  }
};
