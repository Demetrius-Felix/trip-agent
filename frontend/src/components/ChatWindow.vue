<script setup>
import { ref, watch, nextTick, onMounted, onUnmounted } from 'vue';
import { Send, MapPin, Loader2 } from 'lucide-vue-next';
import MessageBubble from './MessageBubble.vue';
import InputArea from './InputArea.vue';
import sessionApi from '../api/session';

const props = defineProps({
  sessionId: {
    type: [Number, String],
    required: true
  }
});

const emit = defineEmits(['update-title']);

const messages = ref([]);
const isLoading = ref(false);
const isGenerating = ref(false);
const messagesEndRef = ref(null);
const currentEventSource = ref(null);

const scrollToBottom = async () => {
  await nextTick();
  if (messagesEndRef.value) {
    messagesEndRef.value.scrollIntoView({ behavior: 'smooth' });
  }
};

const fetchMessages = async () => {
  if (!props.sessionId) return;
  isLoading.value = true;
  try {
    const data = await sessionApi.getSessionMessages(props.sessionId);
    // Transform backend message format to frontend format if needed
    // Backend: { role: 'user'|'assistant', content: '...', ... }
    messages.value = data;
    scrollToBottom();
  } catch (error) {
    console.error('Failed to fetch messages:', error);
  } finally {
    isLoading.value = false;
  }
};

const handleSendMessage = async (text) => {
  if (!text.trim() || isGenerating.value) return;

  // Optimistic update
  const userMessage = {
    role: 'user',
    content: text,
    created_at: new Date().toISOString()
  };
  messages.value.push(userMessage);
  scrollToBottom();

  isGenerating.value = true;
  
  // Create placeholder for assistant message
  const assistantMessage = {
    role: 'assistant',
    content: '',
    created_at: new Date().toISOString()
  };
  messages.value.push(assistantMessage);

  try {
    const url = `http://127.0.0.1:8000/chat/stream/${props.sessionId}?query=${encodeURIComponent(text)}`;
    console.log('Initiating EventSource connection to:', url);
    
    // 使用 EventSource (GET) 连接后端流式接口
    const eventSource = new EventSource(url);

    eventSource.onopen = () => {
      console.log('EventSource connection opened');
    };

    eventSource.onmessage = (event) => {
      console.log('Received SSE data:', event.data);
      const data = event.data;
      
      if (data === '[DONE]') {
        console.log('Stream finished [DONE]');
        eventSource.close();
        isGenerating.value = false;
        // 触发标题更新事件
        emit('update-title');
      } else if (data.startsWith('[ERROR]')) {
        console.error('Stream error:', data);
        assistantMessage.error = data.slice(7);
        eventSource.close();
        isGenerating.value = false;
      } else {
        assistantMessage.content += data;
        scrollToBottom();
      }
    };

    eventSource.onerror = (error) => {
      console.error('EventSource failed:', error);
      eventSource.close();
      isGenerating.value = false;
      if (!assistantMessage.content && !assistantMessage.error) {
        assistantMessage.error = 'Connection failed or stream ended unexpectedly.';
      }
    };

    // Store eventSource reference to close it if component unmounts or user navigates away
    // (This part requires adding a ref to store the current eventSource)
    currentEventSource.value = eventSource;

  } catch (error) {
    console.error('Error initiating EventSource:', error);
    assistantMessage.error = 'Failed to start conversation.';
    isGenerating.value = false;
  }
};

watch(() => props.sessionId, (newId) => {
  if (newId) {
    if (currentEventSource.value) {
      currentEventSource.value.close();
      currentEventSource.value = null;
      isGenerating.value = false;
    }
    fetchMessages();
  } else {
    messages.value = [];
  }
}, { immediate: true });

onUnmounted(() => {
  if (currentEventSource.value) {
    currentEventSource.value.close();
  }
});
</script>

<template>
  <div class="flex flex-col h-full bg-white relative">
    <!-- Messages Area -->
    <div class="flex-1 overflow-y-auto custom-scrollbar p-4 md:p-8 space-y-6">
      <div v-if="isLoading" class="flex justify-center items-center h-full text-gray-400">
        <Loader2 class="animate-spin mr-2" /> Loading chat...
      </div>
      
      <div v-else-if="messages.length === 0" class="flex flex-col items-center justify-center h-full text-center space-y-4 opacity-50">
        <div class="bg-emerald-100 p-4 rounded-full">
            <MapPin class="text-emerald-600 h-8 w-8" />
        </div>
        <h3 class="text-xl font-medium text-gray-700">Where do you want to go?</h3>
        <p class="text-sm text-gray-500 max-w-md">I can help you plan your perfect trip. Just tell me your destination, dates, and interests.</p>
      </div>

      <template v-else>
        <MessageBubble 
          v-for="(msg, index) in messages" 
          :key="index" 
          :message="msg" 
          :is-last="index === messages.length - 1"
        />
        <div ref="messagesEndRef" class="h-4"></div>
      </template>
    </div>

    <!-- Input Area -->
    <div class="p-4 bg-white/80 backdrop-blur-sm border-t border-gray-100 z-10">
      <InputArea 
        @send="handleSendMessage" 
        :disabled="isGenerating || isLoading" 
        placeholder="Plan a 3-day trip to Kyoto..."
      />
    </div>
  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #e5e7eb;
  border-radius: 20px;
}
</style>
