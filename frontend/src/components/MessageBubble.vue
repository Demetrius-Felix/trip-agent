<script setup>
import { computed } from 'vue';
import { marked } from 'marked';
import { User, Bot, Loader2 } from 'lucide-vue-next';

const props = defineProps({
  message: {
    type: Object,
    required: true,
  },
  isLast: {
    type: Boolean,
    default: false,
  }
});

const parsedContent = computed(() => {
  return marked.parse(props.message.content || '');
});

const isUser = computed(() => props.message.role === 'user');
</script>

<template>
  <div class="flex w-full mb-6" :class="isUser ? 'justify-end' : 'justify-start'">
    <div 
      class="flex max-w-[85%] md:max-w-[75%]"
      :class="isUser ? 'flex-row-reverse' : 'flex-row'"
    >
      <!-- Avatar -->
      <div 
        class="flex-shrink-0 h-8 w-8 rounded-full flex items-center justify-center text-white shadow-sm"
        :class="isUser ? 'bg-gray-800 ml-3' : 'bg-emerald-600 mr-3'"
      >
        <User v-if="isUser" :size="16" />
        <Bot v-else :size="16" />
      </div>

      <!-- Content -->
      <div 
        class="relative px-4 py-3 rounded-2xl shadow-sm text-sm leading-relaxed overflow-hidden"
        :class="[
          isUser 
            ? 'bg-gray-100 text-gray-800 rounded-tr-none' 
            : 'bg-white border border-gray-100 text-gray-800 rounded-tl-none'
        ]"
      >
        <div v-if="message.role === 'assistant' && !message.content && !message.error" class="flex items-center space-x-2">
           <Loader2 class="animate-spin text-gray-400" :size="16" />
           <span class="text-gray-400 text-xs">Thinking...</span>
        </div>
        
        <div 
          v-else 
          class="prose prose-sm max-w-none break-words"
          :class="isUser ? 'prose-p:text-gray-800' : 'prose-p:text-gray-700'"
          v-html="parsedContent"
        ></div>

        <div v-if="message.error" class="text-red-500 text-xs mt-2">
            Error: {{ message.error }}
        </div>
      </div>
    </div>
  </div>
</template>

<style>
/* Custom prose styles for better markdown rendering */
.prose p {
  margin-bottom: 0.5em;
}
.prose p:last-child {
  margin-bottom: 0;
}
.prose ul {
  list-style-type: disc;
  padding-left: 1.2em;
  margin-bottom: 0.5em;
}
.prose ol {
  list-style-type: decimal;
  padding-left: 1.2em;
  margin-bottom: 0.5em;
}
.prose code {
  background-color: rgba(0,0,0,0.05);
  padding: 0.2em 0.4em;
  border-radius: 0.25em;
  font-size: 0.9em;
}
.prose pre {
  background-color: #f3f4f6;
  padding: 0.8em;
  border-radius: 0.5em;
  overflow-x: auto;
  margin-bottom: 0.8em;
}
.prose pre code {
  background-color: transparent;
  padding: 0;
}
.prose a {
  color: #059669; /* emerald-600 */
  text-decoration: underline;
}
</style>
