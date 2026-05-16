<!-- 
  Módulo Components: AppLayout
  Componente principal de diseño que enmarca toda la aplicación.
  Redesigned with shadcn-vue components + Lucide icons.
-->
<template>
  <div class="flex min-h-screen bg-background transition-colors duration-200">

    <!-- Mobile Sidebar Backdrop -->
    <div v-show="isSidebarOpen" @click="isSidebarOpen = false" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 md:hidden transition-opacity"></div>

    <!-- Sidebar -->
    <aside :class="['fixed inset-y-0 left-0 z-50 w-64 bg-sidebar border-r border-sidebar-border shadow-xl md:shadow-none flex flex-col transition-transform duration-300 md:relative md:translate-x-0', isSidebarOpen ? 'translate-x-0' : '-translate-x-full']">

      <!-- Logo / Brand -->
      <div class="flex items-center gap-3 px-5 py-5 border-b border-sidebar-border">
        <img src="/logo.png" alt="Logo CJLM" class="h-10 w-auto object-contain shrink-0" />
        <div class="leading-tight">
          <p class="text-sm font-extrabold text-sidebar-foreground tracking-tight leading-none">{{ user?.organization_name || 'Organización' }}</p>
        </div>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 px-3 py-6 space-y-1.5 overflow-y-auto">
        <p class="text-[10px] font-bold text-muted-foreground uppercase tracking-widest px-3 mb-4">Menú Principal</p>

        <router-link to="/dashboard" class="sidebar-link" active-class="sidebar-link-active">
          <LayoutDashboard class="sidebar-icon" />
          Panel
        </router-link>

        <router-link to="/beneficiaries" class="sidebar-link" active-class="sidebar-link-active">
          <Users class="sidebar-icon" />
          Usuarios
        </router-link>

        <router-link to="/activities" class="sidebar-link" active-class="sidebar-link-active">
          <Puzzle class="sidebar-icon" />
          Actividades
        </router-link>

        <router-link to="/excursions" class="sidebar-link" active-class="sidebar-link-active">
          <Map class="sidebar-icon" />
          Excursiones
        </router-link>
        
        <router-link to="/reports" class="sidebar-link" active-class="sidebar-link-active">
          <FileBarChart class="sidebar-icon" />
          Reportes
        </router-link>

        <router-link to="/admins" class="sidebar-link" active-class="sidebar-link-active">
          <Settings class="sidebar-icon" />
          Admin
        </router-link>

        <Separator class="my-5" />

        <!-- CTA: Register Attendance -->
        <router-link :to="`/attendance?org=${user.organization_slug || 'las-mananitas'}`" class="flex items-center justify-center gap-3 px-4 py-3.5 rounded-xl bg-primary text-primary-foreground font-bold text-sm hover:bg-primary/90 transition-all shadow-md shadow-primary/25 hover:shadow-lg hover:shadow-primary/30 hover:scale-[1.02] active:scale-[0.98]">
          <ClipboardCheck class="w-5 h-5 shrink-0" />
          Registrar Asistencia
        </router-link>
      </nav>

      <!-- Bottom: Logout -->
      <div class="px-3 py-4 border-t border-sidebar-border mt-auto shrink-0">
        <Button variant="ghost" @click="logout" class="w-full justify-start gap-3 text-muted-foreground hover:text-destructive hover:bg-destructive/10">
          <LogOut class="w-5 h-5 shrink-0" />
          Salir
        </Button>
      </div>
    </aside>

    <!-- Main content area -->
    <main class="flex-1 min-w-0 overflow-y-auto flex flex-col">

      <!-- Topbar -->
      <header class="sticky top-0 z-10 bg-background/80 backdrop-blur-md border-b border-border px-6 py-3 flex items-center justify-between shrink-0 min-h-[64px] transition-colors duration-200">
        <div class="flex items-center gap-3 shrink-0">
          <!-- Mobile menu button -->
          <Button variant="ghost" size="icon" @click="isSidebarOpen = true" class="md:hidden -ml-2">
            <Menu class="w-5 h-5" />
          </Button>
          <h2 class="text-lg font-extrabold text-foreground tracking-tight whitespace-nowrap">{{ pageTitle }}</h2>
        </div>

        <!-- Middle: Subtle context (Desktop only) -->
        <div class="hidden md:flex flex-1 items-center justify-end gap-4 px-4 overflow-hidden">
          <!-- Weather Widget (toned down) -->
          <div v-if="weather" class="flex items-center gap-1.5 text-muted-foreground shrink-0" title="Clima actual en Ciudad de Panamá">
            <span class="text-base">{{ weatherIcon }}</span>
            <span class="text-xs font-medium">{{ weather.temperature }}°C</span>
          </div>
          
          <!-- Dynamic Greeting (subtler) -->
          <div class="hidden lg:flex items-center text-center truncate shrink-0">
            <span class="text-xs font-medium text-muted-foreground truncate">{{ dynamicGreeting }}, <span class="text-foreground font-semibold">{{ user.first_name || user.username }}</span> {{ greetingEmoji }}</span>
          </div>
        </div>

        <!-- Right: date + avatar + notifications -->
        <div class="flex items-center justify-end gap-3 sm:gap-4 shrink-0">
          <span class="text-sm font-medium text-muted-foreground hidden xl:block">{{ currentDate }}</span>
          
          <!-- Notifications Bell -->
          <div class="relative">
            <Button variant="ghost" size="icon" @click="toggleNotifs" title="Notificaciones" class="relative">
              <Bell class="h-5 w-5" />
              <span v-if="notifications.length > 0" class="absolute top-1.5 right-1.5 h-2.5 w-2.5 bg-destructive rounded-full border-2 border-background"></span>
            </Button>
            
            <!-- Notifications Dropdown -->
            <div v-show="isNotifOpen" @click.stop class="absolute right-0 mt-2 w-80 bg-popover text-popover-foreground rounded-xl shadow-lg border overflow-hidden z-50">
              <div class="px-4 py-3 border-b flex justify-between items-center">
                <h3 class="text-sm font-bold">Notificaciones</h3>
                <Badge class="text-[10px]">{{ notifications.length }}</Badge>
              </div>
              <div class="max-h-80 overflow-y-auto">
                <div v-if="notifications.length === 0" class="py-6 text-center text-sm text-muted-foreground">
                  No tienes notificaciones
                </div>
                <div v-for="notif in notifications" :key="notif.id" class="px-4 py-3 border-b border-border/50 hover:bg-muted/50 transition-colors flex gap-3">
                  <div class="shrink-0 mt-0.5">
                    <span v-if="notif.type === 'birthday'" class="text-xl">🎂</span>
                    <span v-else-if="notif.type === 'activity'" class="text-xl">🏃</span>
                    <span v-else class="text-xl">⚠️</span>
                  </div>
                  <div>
                    <p class="text-xs font-semibold mb-0.5">{{ notif.title }} <Badge v-if="notif.is_urgent" variant="destructive" class="ml-1 text-[10px] px-1 py-0">HOY</Badge></p>
                    <p class="text-xs text-muted-foreground leading-tight">{{ notif.message }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Theme Switcher -->
          <Button variant="ghost" size="icon" @click="toggleTheme" class="hidden sm:flex">
            <Moon v-if="!isDarkMode" class="h-5 w-5" />
            <Sun v-else class="h-5 w-5" />
          </Button>

          <!-- Profile avatar -->
          <div class="flex items-center gap-2 cursor-pointer group">
            <Avatar :fallback="(user.first_name || 'U').charAt(0)" class="h-8 w-8 bg-primary/10 text-primary border-2 border-primary/20" />
            <span class="text-sm font-semibold text-muted-foreground hidden sm:block">{{ user.first_name || user.username }}</span>
          </div>
        </div>
      </header>

      <!-- Page content -->
      <div class="flex-1 transition-colors">
        <router-view />
      </div>

      <!-- Footer -->
      <footer class="py-4 text-center text-xs text-muted-foreground mt-auto shrink-0">
        <p>Made with <span class="text-red-500">❤️</span> by AngelP</p>
      </footer>
    </main>

  </div>
</template>

<script setup>
import apiClient from '../plugins/axios'
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { LayoutDashboard, Users, Puzzle, Map, FileBarChart, Settings, ClipboardCheck, LogOut, Menu, Bell, Moon, Sun } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { Avatar } from '@/components/ui/avatar'

const router = useRouter()
const route = useRoute()
const isSidebarOpen = ref(false)
const userStore = useUserStore()
const user = computed(() => userStore.user)

watch(() => route.path, () => {
    isSidebarOpen.value = false
})

const pageTitles = {
  Dashboard: 'Panel de Control',
  Beneficiaries: 'Manejo de Usuarios',
  Activities: 'Manejo de Actividades',
  BeneficiaryProfile: 'Perfil de Usuario',
  ActivityProfile: 'Perfil de Actividad',
  Reports: 'Reportes',
  Admins: 'Administradores',
}

const pageTitle = computed(() => pageTitles[route.name] ?? route.name ?? 'Página')

const currentDate = computed(() => {
  return new Date().toLocaleDateString('es-PA', { weekday: 'long', day: 'numeric', month: 'long' })
})

const isDarkMode = ref(localStorage.getItem('theme') === 'dark')

const applyTheme = () => {
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
}

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  applyTheme()
}

// Weather Widget (Open-Meteo API for Panama City)
const weather = ref(null)
const weatherIcon = ref('⛅')

const fetchWeather = async () => {
  try {
    const lat = 8.9936
    const lon = -79.5197
    const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true`
    const res = await fetch(url)
    const data = await res.json()
    if (data && data.current_weather) {
      weather.value = {
        temperature: Math.round(data.current_weather.temperature),
        code: data.current_weather.weathercode,
        description: 'Parcialmente Nublado'
      }
      const code = weather.value.code
      if (code === 0) { weatherIcon.value = '☀️'; weather.value.description = 'Despejado' }
      else if (code >= 1 && code <= 3) { weatherIcon.value = '⛅'; weather.value.description = 'Nublado' }
      else if (code >= 51 && code <= 67) { weatherIcon.value = '🌧️'; weather.value.description = 'Lluvia' }
      else if (code >= 95) { weatherIcon.value = '⛈️'; weather.value.description = 'Tormenta' }
    }
  } catch (e) {
    console.warn("Failed to fetch weather", e)
  }
}

// Dynamic Greeting
const dynamicGreeting = ref('Hola')
const greetingEmoji = ref('👋')

const updateGreeting = () => {
  const hour = new Date().getHours()
  if (hour < 12) {
    dynamicGreeting.value = 'Buenos días'
    greetingEmoji.value = '☕'
  } else if (hour < 18) {
    dynamicGreeting.value = 'Buenas tardes'
    greetingEmoji.value = '🌤️'
  } else {
    dynamicGreeting.value = 'Buenas noches'
    greetingEmoji.value = '🌙'
  }
}

// Notifications
const isNotifOpen = ref(false)
const notifications = ref([])
const toggleNotifs = () => { isNotifOpen.value = !isNotifOpen.value }

const fetchNotifications = async () => {
  try {
    const res = await apiClient.get('notifications/')
    notifications.value = res.data
  } catch (error) {
    console.error("Error fetching notifications", error)
  }
}

const fetchUser = async () => {
  await userStore.fetchUser()
}

const handleClickOutside = (e) => {
  if (isNotifOpen.value) {
    if (!e.target.closest('.relative')) {
      isNotifOpen.value = false
    }
  }
}

onMounted(() => {
  applyTheme()
  updateGreeting()
  fetchWeather()
  fetchNotifications()
  fetchUser()
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  userStore.clearUser()
  router.push('/')
}
</script>

<style scoped>
.sidebar-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.7rem 0.85rem;
  border-radius: calc(var(--radius) + 2px);
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-muted-foreground);
  transition: background-color 0.15s, color 0.15s, border-color 0.15s;
  border-left: 3px solid transparent;
}

.sidebar-link:hover {
  background-color: var(--color-sidebar-accent);
  color: var(--color-sidebar-primary);
}

.sidebar-link-active {
  background-color: var(--color-sidebar-accent) !important;
  color: var(--color-sidebar-primary) !important;
  font-weight: 700;
  border-left-color: var(--color-sidebar-primary) !important;
}

.sidebar-icon {
  width: 1.375rem;
  height: 1.375rem;
  flex-shrink: 0;
}
</style>
