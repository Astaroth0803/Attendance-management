<!-- 
  Módulo Components: AppLayout
  Componente principal de diseño que enmarca toda la aplicación.
  Incluye el Sidebar (navegación lateral), el Header (barra superior con clima, saludo dinámico y notificaciones)
  y proporciona el espacio <router-view> para el contenido de la página.
-->
<template>
  <div class="flex min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">

    <!-- Mobile Sidebar Backdrop -->
    <div v-show="isSidebarOpen" @click="isSidebarOpen = false" class="fixed inset-0 bg-gray-900/50 z-40 md:hidden transition-opacity"></div>

    <!-- Sidebar -->
    <aside :class="['fixed inset-y-0 left-0 z-50 w-64 bg-white dark:bg-gray-800 border-r border-gray-100 dark:border-gray-700 shadow-xl md:shadow-sm flex flex-col transition-transform duration-300 md:relative md:translate-x-0', isSidebarOpen ? 'translate-x-0' : '-translate-x-full']">

      <!-- Logo / Brand -->
      <div class="flex items-center gap-3 px-5 py-5 border-b border-gray-100 dark:border-gray-700">
        <img src="/logo.png" alt="Logo CJLM" class="h-10 w-auto object-contain shrink-0" />
        <div class="leading-tight">
          <p class="text-sm font-extrabold text-gray-800 dark:text-gray-100 tracking-tight leading-none">Centro Juvenil</p>
          <p class="text-sm font-extrabold text-orange-600 dark:text-orange-400 tracking-tight leading-none">Y Biblioteca</p>
        </div>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 px-3 py-5 space-y-1 overflow-y-auto">

        <!-- Main nav label -->
        <p class="text-[10px] font-bold text-gray-400 dark:text-gray-500 uppercase tracking-widest px-3 mb-3">Menú Principal</p>

        <router-link to="/dashboard" class="sidebar-link" active-class="sidebar-link-active">
          <!-- Dashboard icon -->
          <svg xmlns="http://www.w3.org/2000/svg" class="sidebar-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
          Panel
        </router-link>

        <router-link to="/beneficiaries" class="sidebar-link" active-class="sidebar-link-active">
          <!-- Users icon -->
          <svg xmlns="http://www.w3.org/2000/svg" class="sidebar-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
          Usuarios
        </router-link>

        <router-link to="/activities" class="sidebar-link" active-class="sidebar-link-active">
          <!-- Activities icon -->
          <svg xmlns="http://www.w3.org/2000/svg" class="sidebar-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 4a2 2 0 114 0v1a1 1 0 001 1h3a1 1 0 011 1v3a1 1 0 01-1 1h-1a2 2 0 100 4h1a1 1 0 011 1v3a1 1 0 01-1 1h-3a1 1 0 01-1-1v-1a2 2 0 10-4 0v1a1 1 0 01-1 1H7a1 1 0 01-1-1v-3a1 1 0 00-1-1H4a2 2 0 110-4h1a1 1 0 001-1V7a1 1 0 011-1h3a1 1 0 001-1V4z" />
          </svg>
          Actividades
        </router-link>

        <router-link to="/excursions" class="sidebar-link" active-class="sidebar-link-active">
          <!-- Excursions icon -->
          <svg xmlns="http://www.w3.org/2000/svg" class="sidebar-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 4a2 2 0 114 0v1a1 1 0 001 1h3a1 1 0 011 1v3a1 1 0 01-1 1h-1a2 2 0 100 4h1a1 1 0 011 1v3a1 1 0 01-1 1h-3a1 1 0 01-1-1v-1a2 2 0 10-4 0v1a1 1 0 01-1 1H7a1 1 0 01-1-1v-3a1 1 0 00-1-1H4a2 2 0 110-4h1a1 1 0 001-1V7a1 1 0 011-1h3a1 1 0 001-1V4z" />
          </svg>
          Excursiones
        </router-link>
        
        <router-link to="/reports" class="sidebar-link" active-class="sidebar-link-active">
          <!-- Reports icon -->
          <svg xmlns="http://www.w3.org/2000/svg" class="sidebar-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Reportes
        </router-link>

        <router-link to="/admins" class="sidebar-link" active-class="sidebar-link-active">
          <!-- Admin icon -->
          <svg xmlns="http://www.w3.org/2000/svg" class="sidebar-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          Admin
        </router-link>

        <!-- Divider -->
        <div class="pt-4 pb-2">
          <div class="border-t border-gray-100 dark:border-gray-700"></div>
        </div>

        <!-- CTA: Register Attendance -->
        <router-link to="/attendance" class="flex items-center gap-3 px-3 py-2.5 rounded-xl bg-orange-600 text-white font-semibold text-sm hover:bg-orange-700 transition-all shadow-sm">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
          </svg>
          Registrar Asistencia
        </router-link>
      </nav>

      <!-- Bottom: Logout -->
      <div class="px-3 py-4 border-t border-gray-100 dark:border-gray-700 mt-auto shrink-0 bg-white dark:bg-gray-800 transition-colors">
        <button @click="logout" class="flex items-center gap-3 w-full px-3 py-2.5 rounded-xl text-gray-500 dark:text-gray-400 hover:bg-red-50 dark:hover:bg-red-900/20 hover:text-red-600 dark:hover:text-red-400 font-semibold text-sm transition-all focus:outline-none focus:ring-2 focus:ring-red-200">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          Salir
        </button>
      </div>
    </aside>

    <!-- Main content area -->
    <main class="flex-1 min-w-0 overflow-y-auto flex flex-col">

      <!-- Topbar -->
      <header class="sticky top-0 z-10 bg-white dark:bg-gray-800 border-b border-gray-100 dark:border-gray-700 shadow-sm px-6 py-3 flex items-center justify-between shrink-0 min-h-[64px] transition-colors duration-200">
        <div class="flex items-center gap-3 shrink-0">
          <!-- Mobile menu button -->
          <button @click="isSidebarOpen = true" class="md:hidden p-2 -ml-2 text-gray-500 dark:text-gray-400 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          <!-- Page title -->
          <h2 class="text-base font-bold text-gray-700 dark:text-gray-200 tracking-tight whitespace-nowrap transition-colors">{{ pageTitle }}</h2>
        </div>

        <!-- Middle: Dynamic Greeting & Weather (Desktop only) -->
        <div class="hidden md:flex flex-1 items-center justify-center gap-4 lg:gap-6 px-4 overflow-hidden">
          <!-- Weather Widget -->
          <div v-if="weather" class="flex items-center gap-2 bg-blue-50/50 dark:bg-blue-900/30 px-3 py-1.5 rounded-full border border-blue-100 dark:border-blue-800 shrink-0 transition-colors" title="Clima actual en Ciudad de Panamá">
            <span class="text-lg">{{ weatherIcon }}</span>
            <div class="flex flex-col">
              <span class="text-xs font-bold text-gray-700 dark:text-gray-300 leading-none">{{ weather.temperature }}°C</span>
              <span class="text-[10px] text-gray-500 dark:text-gray-400 font-medium leading-none capitalize mt-0.5">{{ weather.description }}</span>
            </div>
          </div>
          
          <!-- Dynamic Greeting -->
          <div class="hidden lg:flex items-center text-center truncate shrink-0">
            <span class="text-sm font-bold text-gray-800 dark:text-gray-200 truncate transition-colors">{{ dynamicGreeting }}, <span class="text-orange-600 dark:text-orange-400">{{ user.first_name || user.username }} {{ user.last_name }}</span>! {{ greetingEmoji }}</span>
          </div>
        </div>

        <!-- Right: date + avatar + notifications -->
        <div class="flex items-center justify-end gap-3 sm:gap-4 shrink-0">
          <span class="text-sm font-medium text-gray-500 dark:text-gray-400 hidden xl:block transition-colors">{{ currentDate }}</span>
          
          <!-- Notifications Bell -->
          <div class="relative">
            <button @click="toggleNotifs" class="relative p-2 text-gray-400 dark:text-gray-500 hover:text-orange-500 dark:hover:text-orange-400 transition-colors focus:outline-none shrink-0" title="Notificaciones">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
              <span v-if="notifications.length > 0" class="absolute top-1.5 right-1.5 h-2.5 w-2.5 bg-red-500 rounded-full border-2 border-white dark:border-gray-800"></span>
            </button>
            
            <!-- Notifications Dropdown -->
            <div v-show="isNotifOpen" @click.stop class="absolute right-0 mt-2 w-80 bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-100 dark:border-gray-700 overflow-hidden z-50">
              <div class="px-4 py-3 border-b border-gray-100 dark:border-gray-700 flex justify-between items-center">
                <h3 class="text-sm font-bold text-gray-700 dark:text-gray-200">Notificaciones</h3>
                <span class="text-xs font-semibold bg-orange-100 dark:bg-orange-900/30 text-orange-600 dark:text-orange-400 px-2 py-0.5 rounded-full">{{ notifications.length }}</span>
              </div>
              <div class="max-h-80 overflow-y-auto">
                <div v-if="notifications.length === 0" class="py-6 text-center text-sm text-gray-500 dark:text-gray-400">
                  No tienes notificaciones
                </div>
                <!-- Notif Items -->
                <div v-for="notif in notifications" :key="notif.id" class="px-4 py-3 border-b border-gray-50 dark:border-gray-700/50 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors flex gap-3">
                  <!-- Icon by type -->
                  <div class="shrink-0 mt-0.5">
                    <span v-if="notif.type === 'birthday'" class="text-xl">🎂</span>
                    <span v-else-if="notif.type === 'activity'" class="text-xl">🏃</span>
                    <span v-else class="text-xl">⚠️</span>
                  </div>
                  <div>
                    <p class="text-xs font-semibold text-gray-800 dark:text-gray-200 mb-0.5">{{ notif.title }} <span v-if="notif.is_urgent" class="ml-1 text-[10px] bg-red-100 text-red-600 px-1 py-0.5 rounded">HOY</span></p>
                    <p class="text-xs text-gray-600 dark:text-gray-400 leading-tight">{{ notif.message }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Theme Switcher (Placeholder for now) -->
          <button @click="toggleTheme" class="p-2 text-gray-400 hover:text-gray-600 transition-colors focus:outline-none hidden sm:block">
            <svg v-if="!isDarkMode" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
          </button>
          <!-- Profile avatar -->
          <div class="flex items-center gap-2 cursor-pointer group">
            <div class="w-8 h-8 rounded-full bg-orange-100 border-2 border-orange-200 flex items-center justify-center shrink-0">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-orange-600" viewBox="0 0 24 24" fill="currentColor">
                <path fill-rule="evenodd" d="M7.5 6a4.5 4.5 0 1 1 9 0 4.5 4.5 0 0 1-9 0ZM3.751 20.105a8.25 8.25 0 0 1 16.498 0 .75.75 0 0 1-.437.695A18.683 18.683 0 0 1 12 22.5c-2.786 0-5.433-.608-7.812-1.7a.75.75 0 0 1-.437-.695Z" clip-rule="evenodd" />
              </svg>
            </div>
            <span class="text-sm font-semibold text-gray-600 hidden sm:block">{{ user.first_name || user.username }}</span>
          </div>
        </div>
      </header>

      <!-- Page content -->
      <div class="flex-1 dark:bg-gray-900 transition-colors">
        <router-view />
      </div>

      <!-- Footer -->
      <footer class="py-4 text-center text-xs text-gray-400 dark:text-gray-500 mt-auto shrink-0 transition-colors">
        <p>Made with <span class="text-red-500">❤️</span> by AngelP</p>
      </footer>
    </main>

  </div>
</template>

<script setup>
import apiClient from '../plugins/axios'
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const isSidebarOpen = ref(false)
const user = ref({ first_name: 'Cargando...', last_name: '' })

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

const pageTitle = computed(() => pageTitles[route.name] ?? 'Excursiones ')

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
    // Coordinates for Panama City
    const lat = 8.9936
    const lon = -79.5197
    const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true`
    const res = await fetch(url)
    const data = await res.json()
    if (data && data.current_weather) {
      weather.value = {
        temperature: Math.round(data.current_weather.temperature),
        code: data.current_weather.weathercode,
        description: 'Parcialmente Nublado' // simplified for now
      }
      // Simple icon logic based on WMO code
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

// Dynamic Greeting Lifecycle
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

// Notifications Logic
const isNotifOpen = ref(false)
const notifications = ref([])

const toggleNotifs = () => {
  isNotifOpen.value = !isNotifOpen.value
}

const fetchNotifications = async () => {
  try {
    const res = await apiClient.get('notifications/')
    notifications.value = res.data
  } catch (error) {
    console.error("Error fetching notifications", error)
  }
}

// Fetch User Profile Data
const fetchUser = async () => {
  try {
    const token = localStorage.getItem('access_token')
    if (token) {
      const payload = JSON.parse(atob(token.split('.')[1]))
      if (payload.user_id) {
        const res = await apiClient.get(`users/${payload.user_id}/`)
        user.value = res.data
      }
    }
  } catch (error) {
    console.error("Error fetching user", error)
  }
}

// Click outside to close notifications Dropdown
const handleClickOutside = (e) => {
  if (isNotifOpen.value) {
    // Basic check assuming button click opens it
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
  router.push('/')
}
</script>

<style scoped>
.sidebar-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.625rem 0.75rem;
  border-radius: 0.75rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #4b5563; /* gray-600 */
  transition: background-color 0.15s, color 0.15s;
}

:where(.dark, .dark *) .sidebar-link {
  color: #d1d5db; /* gray-300 */
}

.sidebar-link:hover {
  background-color: #fff7ed; /* orange-50 */
  color: #ea580c; /* orange-600 */
}

:where(.dark, .dark *) .sidebar-link:hover {
  background-color: rgba(234, 88, 12, 0.15);
  color: #fb923c; /* orange-400 */
}

.sidebar-link-active {
  background-color: #fff7ed !important;
  color: #ea580c !important;
  font-weight: 700;
}

:where(.dark, .dark *) .sidebar-link-active {
  background-color: rgba(234, 88, 12, 0.2) !important;
  color: #fb923c !important;
}

.sidebar-icon {
  width: 1.25rem;
  height: 1.25rem;
  flex-shrink: 0;
}
</style>
