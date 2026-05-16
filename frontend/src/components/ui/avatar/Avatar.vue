<script setup>
import { cn } from '@/lib/utils'
const props = defineProps({
  class: { type: String, default: '' },
  src: { type: String, default: '' },
  alt: { type: String, default: '' },
  fallback: { type: String, default: '' },
})
</script>
<template>
  <span :class="cn('relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full', props.class)">
    <img v-if="src" :src="src" :alt="alt" class="aspect-square h-full w-full" />
    <span v-else class="flex h-full w-full items-center justify-center rounded-full bg-muted text-sm font-medium">
      {{ fallback }}
    </span>
  </span>
</template>
