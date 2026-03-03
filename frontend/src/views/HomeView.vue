<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import SessionList from '../components/SessionList.vue';
import ChatWindow from '../components/ChatWindow.vue';
import { Menu } from 'lucide-vue-next';

const route = useRoute();
const router = useRouter();

const isSidebarOpen = ref(true);
const activeSessionId = computed(() => route.params.id ? parseInt(route.params.id) : null);
const sessionListRef = ref(null);

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
};

const refreshSessionList = () => {
  if (sessionListRef.value) {
    sessionListRef.value.fetchSessions();
  }
};

const handleSelectSession = (sessionId) => {
  if (sessionId) {
    router.push(`/session/${sessionId}`);
  } else {
    router.push('/');
  }
  // On mobile, close sidebar after selection
  if (window.innerWidth < 768) {
    isSidebarOpen.value = false;
  }
};

const handleCreateSession = (sessionId) => {
    // SessionList emits 'create' but also handles the creation logic internally 
    // and emits 'select' with the new ID.
    // So we might not need this handler if SessionList does the job.
    // Wait, SessionList emits 'select' with the new ID.
    // So handleSelectSession will be called.
};

</script>

<template>
  <div class="flex h-screen bg-gray-100 overflow-hidden font-sans">
    <!-- Sidebar -->
    <div 
      class="fixed inset-y-0 left-0 z-30 transform transition-transform duration-300 ease-in-out md:relative md:translate-x-0"
      :class="isSidebarOpen ? 'translate-x-0' : '-translate-x-full'"
    >
      <SessionList 
        ref="sessionListRef"
        :active-session-id="activeSessionId" 
        @select="handleSelectSession"
      />
    </div>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col min-w-0 relative">
      <!-- Mobile Header / Toggle -->
      <div class="md:hidden absolute top-4 left-4 z-20">
        <button @click="toggleSidebar" class="p-2 bg-white rounded-lg shadow text-gray-600 hover:text-emerald-600">
          <Menu :size="24" />
        </button>
      </div>

      <!-- Chat Area -->
      <div class="flex-1 h-full relative">
        <ChatWindow 
          v-if="activeSessionId" 
          :session-id="activeSessionId" 
          @update-title="refreshSessionList"
        />
        <div v-else class="flex flex-col items-center justify-center h-full text-gray-400 bg-white">
          <div class="text-center p-8">
            <h2 class="text-2xl font-bold text-gray-800 mb-2">Welcome to Trip Agent</h2>
            <p class="mb-6">Select a chat from the sidebar or create a new one to get started.</p>
            <button 
              @click="isSidebarOpen = true" 
              class="md:hidden px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition"
            >
              Open Menu
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Overlay for mobile sidebar -->
    <div 
      v-if="isSidebarOpen" 
      @click="isSidebarOpen = false"
      class="fixed inset-0 bg-black/20 z-20 md:hidden"
    ></div>
  </div>
</template>
