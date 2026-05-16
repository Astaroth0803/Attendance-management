<template>
  <div class="flex min-h-screen bg-[#1c202b] text-white font-sans transition-colors duration-200">
    <!-- Sidebar -->
    <aside class="w-64 bg-[#1e2330] border-r border-slate-700/50 flex flex-col shrink-0">
      
      <!-- Brand -->
      <div class="px-6 py-6 border-b border-slate-700/50 flex flex-col gap-1 items-start justify-center">
        <h1 class="text-2xl font-extrabold tracking-tight text-white flex items-center gap-1">
          <span class="text-purple-400">Ela</span> attendance
        </h1>
        <Badge variant="secondary" class="bg-slate-700 hover:bg-slate-700 text-[10px] text-slate-300">
          v1.0
        </Badge>
      </div>

      <!-- User Info -->
      <div class="px-6 py-4 flex items-center gap-3 border-b border-slate-700/50">
        <div class="w-8 h-8 rounded-full bg-purple-500 flex items-center justify-center text-sm font-bold shadow-lg">
          {{ (user?.first_name || 'A').charAt(0).toUpperCase() }}
        </div>
        <p class="text-sm font-medium text-slate-300 truncate w-full" :title="user?.email || 'admin@invupos.com'">
          {{ user?.email || 'admin@invupos.com' }}
        </p>
      </div>

      <!-- Navigation -->
      <div class="flex-1 overflow-y-auto py-6">
        <div class="px-6 mb-2">
          <p class="text-[10px] font-bold text-slate-500 uppercase tracking-widest">General</p>
        </div>
        
        <div class="px-6 mb-6">
          <p class="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2 mt-4">Operaciones</p>
          <div class="space-y-1">
            <router-link to="/super-admin" class="flex items-center gap-3 px-3 py-2.5 rounded-lg bg-slate-800 text-slate-200 font-medium text-sm border-l-2 border-orange-500">
              <span class="text-orange-500">🏢</span> Licencias
            </router-link>
          </div>
        </div>

        <div class="px-6 mb-6">
          <p class="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2">Administracion</p>
          <div class="space-y-1">
            <a href="#" class="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-slate-800/50 text-slate-400 font-medium text-sm transition-colors border-l-2 border-transparent">
              <span class="text-orange-500 opacity-60">📋</span> Visitas
            </a>
          </div>
        </div>
      </div>

      <!-- Footer Nav -->
      <div class="p-6 border-t border-slate-700/50 space-y-2 shrink-0">
        <button @click="logout" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-red-500/10 hover:text-red-400 text-slate-400 font-medium text-sm transition-colors">
          <span class="text-red-400 opacity-80">🚪</span> Cerrar sesion
        </button>
      </div>

    </aside>

    <!-- Main Content -->
    <main class="flex-1 flex flex-col min-w-0 overflow-y-auto">
      <router-view />
    </main>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../plugins/axios'
import { Badge } from '@/components/ui/badge'

const router = useRouter()
const user = ref(null)

const fetchUser = async () => {
  try {
    const token = localStorage.getItem('access_token')
    if (token) {
      const payload = JSON.parse(atob(token.split('.')[1]))
      const res = await apiClient.get(`users/${payload.user_id}/`)
      user.value = res.data
    }
  } catch (error) {
    console.error("Error fetching super admin user", error)
  }
}

onMounted(() => {
  fetchUser()
})

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  router.push('/login')
}
</script>
