<script setup>
import { cn } from '@/lib/utils'
const props = defineProps({ class: { type: String, default: '' } })
</script>
<template>
  <div role="none" :class="cn('shrink-0 bg-border h-[1px] w-full', props.class)"></div>
</template>
