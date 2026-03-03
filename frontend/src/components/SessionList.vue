<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import { Plus, Trash2, Map, Calendar, Settings, LogOut, MessageSquare } from 'lucide-vue-next';
import sessionApi from '../api/session';

const props = defineProps({
  activeSessionId: {
    type: [Number, String],
    default: null
  }
});

const emit = defineEmits(['select', 'create', 'delete']);

const sessions = ref([]);
const isLoading = ref(false);
const userId = 1; // Hardcoded for now

const fetchSessions = async () => {
  isLoading.value = true;
  try {
    sessions.value = await sessionApi.getUserSessions(userId);
  } catch (error) {
    console.error('Failed to fetch sessions:', error);
  } finally {
    isLoading.value = false;
  }
};

const handleCreateSession = async () => {
  try {
    const newSession = await sessionApi.createSession(userId, 'New Trip Plan');
    sessions.value.unshift(newSession);
    emit('select', newSession.id);
  } catch (error) {
    console.error('Failed to create session:', error);
  }
};

const handleDeleteSession = async (e, sessionId) => {
  e.stopPropagation(); // Prevent selecting the session when clicking delete
  if (!confirm('Are you sure you want to delete this chat?')) return;
  
  try {
    await sessionApi.deleteSession(sessionId);
    sessions.value = sessions.value.filter(s => s.id !== sessionId);
    if (props.activeSessionId === sessionId) {
      emit('select', null);
    }
  } catch (error) {
    console.error('Failed to delete session:', error);
  }
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric' }).format(date);
};

onMounted(() => {
  fetchSessions();
});

defineExpose({
  fetchSessions
});
</script>

<template>
  <div class="flex flex-col h-full bg-gray-50 border-r border-gray-200 w-64 flex-shrink-0 transition-all duration-300">
    <!-- Header -->
    <div class="p-4 flex items-center justify-between border-b border-gray-200/50">
      <div class="flex items-center space-x-2 font-semibold text-gray-800">
        <Map class="text-emerald-600" :size="20" />
        <span>Trip Agent</span>
      </div>
      <button 
        @click="handleCreateSession"
        class="p-2 hover:bg-gray-200 rounded-lg text-gray-600 transition-colors"
        title="New Chat"
      >
        <Plus :size="20" />
      </button>
    </div>

    <!-- Session List -->
    <div class="flex-1 overflow-y-auto custom-scrollbar p-2 space-y-1">
      <div v-if="isLoading" class="flex justify-center p-4">
        <div class="animate-spin rounded-full h-5 w-5 border-2 border-emerald-500 border-t-transparent"></div>
      </div>
      
      <div v-else-if="sessions.length === 0" class="text-center p-4 text-gray-400 text-sm">
        No chats yet. Start a new one!
      </div>

      <div 
        v-for="session in sessions" 
        :key="session.id"
        @click="$emit('select', session.id)"
        class="group flex items-center justify-between p-3 rounded-xl cursor-pointer transition-all duration-200 text-sm border border-transparent"
        :class="activeSessionId === session.id ? 'bg-white border-gray-200 shadow-sm text-emerald-700 font-medium' : 'hover:bg-gray-200/50 text-gray-600'"
      >
        <div class="flex items-center space-x-3 overflow-hidden">
          <MessageSquare :size="16" :class="activeSessionId === session.id ? 'text-emerald-500' : 'text-gray-400'" />
          <span class="truncate">{{ session.title || 'New Trip Plan' }}</span>
        </div>
        
        <button 
          @click="(e) => handleDeleteSession(e, session.id)"
          class="opacity-0 group-hover:opacity-100 p-1 hover:bg-red-50 hover:text-red-500 rounded transition-all duration-200"
          title="Delete Chat"
        >
          <Trash2 :size="14" />
        </button>
      </div>
    </div>

    <!-- Footer -->
    <div class="p-4 border-t border-gray-200/50 space-y-1">
      <button class="flex items-center space-x-3 w-full p-2 hover:bg-gray-200 rounded-lg text-sm text-gray-600 transition-colors">
        <Settings :size="16" />
        <span>Settings</span>
      </button>
       <button class="flex items-center space-x-3 w-full p-2 hover:bg-gray-200 rounded-lg text-sm text-gray-600 transition-colors">
        <LogOut :size="16" />
        <span>Log out</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #d1d5db;
  border-radius: 20px;
}
</style>
