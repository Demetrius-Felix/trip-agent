<script setup>
import { ref, watch, onMounted } from 'vue';
import { Send, ArrowUp } from 'lucide-vue-next';

const props = defineProps({
  disabled: {
    type: Boolean,
    default: false
  },
  placeholder: {
    type: String,
    default: 'Ask me anything about your trip...'
  }
});

const emit = defineEmits(['send']);
const inputRef = ref(null);
const message = ref('');

const adjustHeight = () => {
  const el = inputRef.value;
  if (!el) return;
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 150) + 'px';
};

const handleSend = () => {
  if (props.disabled || !message.value.trim()) return;
  emit('send', message.value);
  message.value = '';
  adjustHeight();
};

const handleKeydown = (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    handleSend();
  }
};

watch(message, () => {
  adjustHeight();
});

onMounted(() => {
  adjustHeight();
});
</script>

<template>
  <div class="relative w-full max-w-4xl mx-auto p-4">
    <div class="relative flex items-end bg-white border border-gray-200 shadow-sm rounded-2xl focus-within:ring-2 focus-within:ring-emerald-500/20 focus-within:border-emerald-500 transition-all duration-200">
      <textarea
        ref="inputRef"
        v-model="message"
        :placeholder="placeholder"
        :disabled="disabled"
        rows="1"
        class="w-full py-3 pl-4 pr-12 bg-transparent resize-none outline-none text-gray-700 placeholder-gray-400 min-h-[52px] max-h-[150px] overflow-y-auto custom-scrollbar"
        @keydown="handleKeydown"
        @input="adjustHeight"
      ></textarea>
      
      <button 
        @click="handleSend"
        :disabled="!message.trim() || disabled"
        class="absolute right-2 bottom-2 p-2 rounded-xl transition-all duration-200 disabled:opacity-30 disabled:cursor-not-allowed hover:bg-emerald-50 text-emerald-600"
      >
        <ArrowUp v-if="!disabled" :size="20" />
        <span v-else class="block w-5 h-5 rounded-full border-2 border-emerald-600 border-t-transparent animate-spin"></span>
      </button>
    </div>
    
    <div class="mt-2 text-center text-xs text-gray-400">
      Trip Agent can make mistakes. Consider checking important information.
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
  background-color: #e5e7eb;
  border-radius: 20px;
}
</style>
