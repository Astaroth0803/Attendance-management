<script setup>
import { TabsRoot, useForwardPropsEmits } from 'radix-vue'

const props = defineProps({
  defaultValue: { type: String, required: false },
  orientation: { type: String, required: false, default: 'horizontal' },
  dir: { type: String, required: false, default: 'ltr' },
  activationMode: { type: String, required: false, default: 'automatic' },
  modelValue: { type: String, required: false },
  asChild: { type: Boolean, required: false },
  as: { type: null, required: false }
})

const emits = defineEmits(['update:modelValue'])

const forwarded = useForwardPropsEmits(props, emits)
</script>

<template>
  <TabsRoot v-bind="forwarded">
    <slot />
  </TabsRoot>
</template>
