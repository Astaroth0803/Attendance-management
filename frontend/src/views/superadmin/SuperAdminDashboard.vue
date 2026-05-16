<template>
  <div class="p-6 lg:p-8 space-y-6 max-w-7xl mx-auto w-full">
    
    <!-- Resumen rápido card -->
    <div class="bg-[#1e2330] rounded-xl border border-slate-700/50 p-6 flex flex-col md:flex-row items-start justify-between shadow-sm gap-4">
      <div>
        <h2 class="text-xl font-bold text-white mb-2">Resumen rapido</h2>
        <p class="text-sm text-slate-400 mb-4">Mantenlo cerrado y abrelo solo cuando necesites contexto.</p>
        <div class="flex gap-3">
          <Badge class="bg-blue-500/10 text-blue-400 hover:bg-blue-500/20 border-blue-500/20 px-3 py-1">👥 {{ licenses.length }} resultados</Badge>
          <Badge class="bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20 border-emerald-500/20 px-3 py-1">✓ {{ activeCount }} activas</Badge>
        </div>
      </div>
    </div>

    <!-- Filtros Inteligentes -->
    <div class="bg-[#1e2330] rounded-xl border border-slate-700/50 p-6 shadow-sm">
      <h2 class="text-lg font-bold text-white mb-1">Filtros Inteligentes</h2>
      <p class="text-sm text-slate-400 mb-5">Busca por nombre y reduce rapidamente la lista por pais, distribuidor o estado.</p>
      
      <div class="flex flex-wrap gap-4 items-end mb-4">
        <div class="flex-1 min-w-[200px]">
          <div class="relative">
            <span class="absolute left-3 top-2.5 text-slate-500">🔍</span>
            <Input v-model="search" placeholder="Buscar" class="pl-10 bg-[#161a24] border-slate-700/50 focus-visible:ring-purple-500 h-10 text-slate-200" />
          </div>
        </div>
        
        <div class="w-48">
          <label class="text-xs text-slate-500 mb-1 block">Pais</label>
          <select v-model="filterCountry" class="w-full bg-[#161a24] border border-slate-700/50 rounded-md h-10 px-3 text-slate-300 focus:outline-none focus:ring-1 focus:ring-purple-500 appearance-none">
            <option value="All">🌍 All</option>
            <option value="Panamá">🇵🇦 Panamá</option>
          </select>
        </div>
        
        <div class="w-48">
          <label class="text-xs text-slate-500 mb-1 block">Distribuidor</label>
          <select disabled class="w-full bg-[#161a24] border border-slate-700/50 rounded-md h-10 px-3 text-slate-300 focus:outline-none focus:ring-1 focus:ring-purple-500 appearance-none opacity-60">
            <option value="All">📦 All</option>
          </select>
        </div>
        
        <div class="w-48">
          <label class="text-xs text-slate-500 mb-1 block">Status</label>
          <select v-model="filterStatus" class="w-full bg-[#161a24] border border-slate-700/50 rounded-md h-10 px-3 text-slate-300 focus:outline-none focus:ring-1 focus:ring-purple-500 appearance-none">
            <option value="All">🏳️ All</option>
            <option value="Active">Activas</option>
            <option value="Inactive">Inactivas</option>
          </select>
        </div>
      </div>
      
      <Badge class="bg-blue-500/10 text-blue-400 hover:bg-blue-500/10 border-blue-500/20 px-3">👁️ {{ filteredLicenses.length }} resultados</Badge>
    </div>

    <!-- List of Licenses -->
    <div class="space-y-4">
      <div v-for="(org, index) in filteredLicenses" :key="org.id" 
           @click="openActionModal(org)"
           class="bg-[#1e2330] rounded-xl border border-slate-700/50 p-4 flex items-center justify-between hover:border-purple-500/50 transition-colors cursor-pointer group shadow-sm">
        <div class="flex items-center gap-4">
          <div class="w-10 h-10 rounded bg-[#2a3042] flex items-center justify-center font-bold text-slate-300 shadow-inner">
            {{ index + 1 }}
          </div>
          <div>
            <h3 class="text-lg font-bold text-slate-200 group-hover:text-white transition-colors">{{ org.name }}</h3>
            <div class="flex gap-2 mt-2">
              <Badge v-if="org.is_active" class="bg-emerald-500/10 text-emerald-400 border-none font-medium text-xs px-2 rounded-md">✓ Activa</Badge>
              <Badge v-else class="bg-rose-500/10 text-rose-400 border-none font-medium text-xs px-2 rounded-md">✕ Inactiva</Badge>
              
              <Badge class="bg-blue-500/10 text-blue-400 border-none font-medium text-xs px-2 rounded-md">🌍 {{ org.country }}</Badge>
              <Badge class="bg-purple-500/10 text-purple-400 border-none font-medium text-xs px-2 rounded-md">🟣 Ela attendance</Badge>
              <Badge v-if="org.client_first_name" class="bg-orange-500/10 text-orange-400 border-none font-medium text-xs px-2 rounded-md">🔔 {{ org.client_first_name?.toUpperCase() }}</Badge>
            </div>
          </div>
        </div>
        <div class="text-slate-500 group-hover:text-slate-300 transition-colors">
          <span class="text-xl">↗</span>
        </div>
      </div>

      <div v-if="filteredLicenses.length === 0 && !loading" class="text-center py-12 text-slate-500">
        No se encontraron licencias con esos filtros.
      </div>
    </div>

    <!-- Floating Create Button -->
    <button @click="showCreateModal = true" class="fixed bottom-8 right-8 w-14 h-14 bg-orange-500 hover:bg-orange-600 text-white rounded-full flex items-center justify-center shadow-[0_0_20px_rgba(249,115,22,0.4)] transition-transform hover:scale-110 active:scale-95 z-40 text-2xl font-light">
      +
    </button>

    <!-- Create License Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex justify-center items-center p-4">
      <div class="bg-[#1e2330] rounded-2xl w-full max-w-md border border-slate-700/50 shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        <div class="px-6 py-5 border-b border-slate-700/50 flex justify-between items-center">
          <h2 class="text-lg font-bold text-white">Crear Licencia</h2>
          <button @click="showCreateModal = false" class="text-slate-500 hover:text-slate-300 text-xl leading-none">&times;</button>
        </div>
        <form @submit.prevent="createLicense" class="p-6 space-y-4">
          <div class="relative">
            <span class="absolute left-3 top-3 text-orange-500">👤</span>
            <input v-model="newOrg.name" required type="text" placeholder="Nombre Licencia" class="w-full bg-[#161a24] border border-slate-700/50 rounded-lg h-12 pl-10 pr-4 text-sm text-slate-200 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500" />
          </div>
          <div class="relative">
            <span class="absolute left-3 top-3 text-orange-500">👤</span>
            <input v-model="newOrg.client_first_name" required type="text" placeholder="Nombre Cliente" class="w-full bg-[#161a24] border border-slate-700/50 rounded-lg h-12 pl-10 pr-4 text-sm text-slate-200 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500" />
          </div>
          <div class="relative">
            <span class="absolute left-3 top-3 text-orange-500">👤</span>
            <input v-model="newOrg.client_last_name" required type="text" placeholder="Apellido Cliente" class="w-full bg-[#161a24] border border-slate-700/50 rounded-lg h-12 pl-10 pr-4 text-sm text-slate-200 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500" />
          </div>
          <div class="relative">
            <span class="absolute left-3 top-3 text-orange-500">📧</span>
            <input v-model="newOrg.client_email" required type="email" placeholder="Email Cliente" class="w-full bg-[#161a24] border border-slate-700/50 rounded-lg h-12 pl-10 pr-4 text-sm text-slate-200 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500" />
          </div>
          <div class="relative">
            <span class="absolute left-3 top-3 text-orange-500">📞</span>
            <input v-model="newOrg.client_phone" required type="text" placeholder="Telefono Cliente" class="w-full bg-[#161a24] border border-slate-700/50 rounded-lg h-12 pl-10 pr-4 text-sm text-slate-200 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500" />
          </div>
          
          <div class="flex justify-end gap-6 pt-4 items-center">
            <button type="button" @click="showCreateModal = false" class="text-purple-400 hover:text-purple-300 font-medium text-sm">Cerrar</button>
            <button type="submit" :disabled="creating" class="text-orange-500 hover:text-orange-400 font-medium text-sm disabled:opacity-50">
              {{ creating ? 'Creando...' : 'Crear' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Action Modal -->
    <div v-if="selectedOrg" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex justify-center items-center p-4" @click.self="selectedOrg = null">
      <div class="bg-[#1e2330] rounded-2xl w-full max-w-lg border border-slate-700/50 shadow-2xl p-6 animate-in fade-in zoom-in-95 duration-200">
        <h2 class="text-lg font-bold text-white mb-1">Cliente {{ selectedOrg.name }}</h2>
        <p class="text-xs text-rose-500 mb-6">- Central: {{ selectedOrg.name.toUpperCase() }}</p>
        
        <div class="grid grid-cols-2 gap-y-6 gap-x-4 text-sm text-purple-400 font-medium pb-8">
           <button @click="generateSupport" class="text-left hover:text-purple-300 transition-colors">🛡️ Soporte Técnico</button>
           <button @click="viewAdmins" class="text-left hover:text-purple-300 transition-colors text-blue-400">👥 Ver Usuario Admin</button>
           <button @click="toggleStatus" class="text-left" :class="selectedOrg.is_active ? 'text-rose-400 hover:text-rose-300' : 'text-emerald-400 hover:text-emerald-300'">
             {{ selectedOrg.is_active ? '🔴 Desactivar Licencia' : '🟢 Activar Licencia' }}
           </button>
        </div>
        
        <div class="border-t border-slate-700/50 pt-4 flex justify-end">
          <button @click="selectedOrg = null" class="text-purple-400 hover:text-purple-300 text-sm font-medium">Cerrar</button>
        </div>
      </div>
    </div>

    <!-- Credentials Modal -->
    <div v-if="credentials" class="fixed inset-0 bg-black/80 backdrop-blur-md z-[60] flex justify-center items-center p-4" @click.self="credentials = null">
      <div class="bg-white rounded-xl w-full max-w-sm overflow-hidden animate-in fade-in zoom-in-95 duration-200">
         <div class="bg-emerald-500 p-6 text-center text-white">
            <div class="text-4xl mb-2">🎉</div>
            <h2 class="text-xl font-bold">Credenciales Generadas</h2>
         </div>
         <div class="p-6 text-center space-y-4">
            <p class="text-slate-600 text-sm">Usa estos datos para iniciar sesión y brindar soporte técnico a esta licencia.</p>
            <div class="bg-slate-100 p-3 rounded-lg text-left">
               <p class="text-xs text-slate-500 mb-1">Usuario / Email</p>
               <p class="font-mono text-sm font-bold text-slate-800 break-all">{{ credentials.username }}</p>
            </div>
            <div class="bg-slate-100 p-3 rounded-lg text-left relative group">
               <p class="text-xs text-slate-500 mb-1">Contraseña temporal</p>
               <p class="font-mono text-sm font-bold text-slate-800 break-all">{{ credentials.password }}</p>
            </div>
            <Button @click="credentials = null" class="w-full mt-2">Aceptar y Cerrar</Button>
         </div>
      </div>
    </div>

    <!-- Admin Users Modal -->
    <div v-if="adminUsersModal" class="fixed inset-0 bg-black/80 backdrop-blur-md z-[60] flex justify-center items-center p-4" @click.self="adminUsersModal = null">
      <div class="bg-[#1e2330] rounded-2xl w-full max-w-lg border border-slate-700/50 shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200">
         <div class="px-6 py-5 border-b border-slate-700/50 flex justify-between items-center">
            <h2 class="text-lg font-bold text-white">Administradores de la Licencia</h2>
            <button @click="adminUsersModal = null" class="text-slate-500 hover:text-slate-300 text-xl leading-none">&times;</button>
         </div>
         <div class="p-6">
            <p class="text-sm text-slate-400 mb-4">Estos son los usuarios iniciales que se generaron o tienen rol de administrador en esta licencia.</p>
            <div v-if="loadingAdmins" class="text-center py-8 text-purple-400">Cargando...</div>
            <div v-else-if="adminUsers.length === 0" class="text-center py-8 text-slate-500">No se encontraron administradores primarios.</div>
            <div v-else class="space-y-3">
               <div v-for="user in adminUsers" :key="user.username" class="bg-[#161a24] p-4 rounded-xl border border-slate-700/30 flex justify-between items-center">
                  <div>
                    <h3 class="font-bold text-slate-200 text-sm">{{ user.first_name }} {{ user.last_name }}</h3>
                    <p class="text-xs text-purple-400 font-mono mt-1">{{ user.username }}</p>
                    <p class="text-[10px] text-slate-500 mt-0.5">📧 {{ user.email }}</p>
                  </div>
                  <div class="text-right">
                    <Badge v-if="user.is_active" class="bg-emerald-500/10 text-emerald-400 border-none font-medium text-[10px] px-2 py-0">Activo</Badge>
                    <Badge v-else class="bg-amber-500/10 text-amber-400 border-none font-medium text-[10px] px-2 py-0">Inactivo</Badge>
                    <p class="text-[10px] text-slate-600 mt-2">Acceso: <br/> {{ user.last_login }}</p>
                  </div>
               </div>
            </div>
         </div>
         <div class="px-6 py-4 bg-[#161a24] border-t border-slate-700/50 flex justify-end">
            <Button @click="adminUsersModal = null" variant="outline" class="bg-slate-800 text-slate-200 hover:bg-slate-700 hover:text-white border-none text-sm h-9">Cerrar</Button>
         </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import apiClient from '../../plugins/axios'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'

const licenses = ref([])
const loading = ref(false)
const search = ref('')
const filterCountry = ref('All')
const filterStatus = ref('All')

const showCreateModal = ref(false)
const selectedOrg = ref(null)
const creating = ref(false)
const credentials = ref(null)

const adminUsersModal = ref(null)
const adminUsers = ref([])
const loadingAdmins = ref(false)

const newOrg = ref({
  name: '', client_first_name: '', client_last_name: '', client_email: '', client_phone: '', country: 'Panamá'
})

const fetchLicenses = async () => {
  loading.value = true
  try {
    const res = await apiClient.get('superadmin/organizations/')
    licenses.value = res.data
  } catch (error) {
    console.error("Error fetching licenses", error)
  } finally {
    loading.value = false
  }
}

const activeCount = computed(() => licenses.value.filter(l => l.is_active).length)

const filteredLicenses = computed(() => {
  return licenses.value.filter(org => {
    const matchSearch = org.name.toLowerCase().includes(search.value.toLowerCase()) || 
                       (org.client_first_name && org.client_first_name.toLowerCase().includes(search.value.toLowerCase()))
    const matchCountry = filterCountry.value === 'All' || org.country === filterCountry.value
    const matchStatus = filterStatus.value === 'All' || 
                        (filterStatus.value === 'Active' && org.is_active) || 
                        (filterStatus.value === 'Inactive' && !org.is_active)
    return matchSearch && matchCountry && matchStatus
  })
})

const createLicense = async () => {
  creating.value = true
  try {
    const res = await apiClient.post('superadmin/organizations/', newOrg.value)
    licenses.value.unshift(res.data)
    showCreateModal.value = false
    newOrg.value = { name: '', client_first_name: '', client_last_name: '', client_email: '', client_phone: '', country: 'Panamá' }
    
    // Automatically show the generated admin credentials
    if (res.data.admin_credentials) {
      credentials.value = res.data.admin_credentials
    }
  } catch (error) {
    alert("Error al crear la licencia. Verifica que el nombre no exista.")
    console.error(error)
  } finally {
    creating.value = false
  }
}

const openActionModal = (org) => {
  selectedOrg.value = org
}

const toggleStatus = async () => {
  if (!selectedOrg.value) return
  if (!confirm(`¿Estás seguro que deseas ${selectedOrg.value.is_active ? 'desactivar' : 'activar'} esta licencia?`)) return
  try {
    const res = await apiClient.post(`superadmin/organizations/${selectedOrg.value.id}/toggle_status/`)
    const index = licenses.value.findIndex(l => l.id === selectedOrg.value.id)
    if (index !== -1) {
      licenses.value[index].is_active = res.data.is_active
    }
    selectedOrg.value = null
  } catch (e) {
    alert("Ha ocurrido un error al cambiar el estado.")
  }
}

const generateSupport = async () => {
  if (!selectedOrg.value) return
  if (!confirm("Esto regenerará las credenciales temporales de soporte técnico para esta organización. ¿Continuar?")) return
  try {
    const res = await apiClient.post(`superadmin/organizations/${selectedOrg.value.id}/generate_support_user/`)
    credentials.value = res.data.credentials
    selectedOrg.value = null
  } catch (e) {
    alert("Hubo un error al generar las credenciales de soporte.")
  }
}

const viewAdmins = async () => {
  if (!selectedOrg.value) return
  adminUsersModal.value = selectedOrg.value
  loadingAdmins.value = true
  try {
    const res = await apiClient.get(`superadmin/organizations/${selectedOrg.value.id}/admin_users/`)
    adminUsers.value = res.data
  } catch (error) {
    alert("Error al obtener los administradores.")
  } finally {
    loadingAdmins.value = false
  }
}

onMounted(() => {
  fetchLicenses()
})
</script>
