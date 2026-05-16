<script setup>
import { cn } from '@/lib/utils'

const props = defineProps({
  open: { type: Boolean, required: true },
  class: { type: String, default: '' },
})
const emit = defineEmits(['update:open'])

const close = () => emit('update:open', false)
</script>

<template>
  <Teleport to="body">
    <Transition name="dialog-fade">
      <div v-if="open" class="fixed inset-0 z-50 flex items-center justify-center">
        <!-- Overlay -->
        <div class="fixed inset-0 bg-black/60 backdrop-blur-sm" @click="close"></div>
        <!-- Content -->
        <div :class="cn('relative z-50 w-full max-w-lg mx-4 bg-background rounded-xl border shadow-2xl animate-in fade-in-0 zoom-in-95 p-6', props.class)">
          <slot />
          <!-- Close button -->
          <button @click="close" class="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
          </button>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.dialog-fade-enter-active,
.dialog-fade-leave-active {
  transition: all 0.2s ease;
}
.dialog-fade-enter-from,
.dialog-fade-leave-to {
  opacity: 0;
}
.dialog-fade-enter-from > div:last-child,
.dialog-fade-leave-to > div:last-child {
  transform: scale(0.95);
}
</style>
