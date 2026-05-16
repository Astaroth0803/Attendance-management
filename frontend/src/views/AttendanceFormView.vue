<template>
  <div class="min-h-screen bg-background flex flex-col">
    
      <!-- Form Header -->
      <div class="bg-gradient-to-r from-primary to-primary/80 px-6 py-12 md:py-16 text-primary-foreground relative shrink-0">
        <Button variant="ghost" @click="$router.push('/')" class="absolute top-6 left-6 md:top-8 md:left-8 text-primary-foreground/70 hover:text-primary-foreground hover:bg-white/10">
          <ArrowLeft class="w-5 h-5 mr-2" />
          Volver
        </Button>
        <h2 class="text-3xl md:text-5xl font-extrabold text-center tracking-tight">Registro de Asistencia</h2>
        <p class="text-primary-foreground/70 text-center mt-4 md:text-lg">Selecciona al usuario y la actividad correspondiente</p>
      </div>

      <!-- Form Body -->
      <div class="flex-1 w-full max-w-4xl mx-auto p-6 md:p-12 lg:p-16">
        <form @submit.prevent="submitAttendance" class="space-y-10 md:space-y-12">
        
        <!-- Step 1 -->
        <div class="space-y-4">
          <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center border-b border-border pb-2 gap-4">
            <div>
              <h3 class="text-xl font-semibold text-foreground">1. Buscar Usuario</h3>
              <p class="text-sm text-muted-foreground">Ingresa la cédula, número de ID o Nombre para buscar al asistente.</p>
            </div>
            <Button type="button" variant="outline" @click="showRegisterForm = true" class="text-primary border-primary/30 hover:bg-primary/5">
              <Plus class="w-4 h-4 mr-1" /> Primer Registro
            </Button>
          </div>
          
          <div class="relative">
            <Input v-model="searchQuery" type="text" placeholder="Ej: 8-000-0000 o 'Juan Pérez'" class="pr-20 h-12" />
            <Button type="button" @click="searchBeneficiaries" size="sm" class="absolute right-1.5 top-1.5">
              Buscar
            </Button>
          </div>

          <ul v-if="beneficiaries.length > 0" class="mt-2 divide-y divide-border border rounded-lg max-h-48 overflow-y-auto">
             <li v-for="b in beneficiaries" :key="b.id" 
                 @click="selectBeneficiary(b)"
                 class="p-3 hover:bg-muted/50 cursor-pointer flex justify-between items-center transition-colors"
                 :class="{ 'bg-primary/5 border-l-4 border-l-primary': selectedBeneficiary?.id === b.id }">
               <div>
                 <p class="font-medium text-foreground">{{ b.first_name }} {{ b.last_name }}</p>
                 <p class="text-xs text-muted-foreground">
                    <span v-if="b.ci">Cédula: {{ b.ci }} | </span>
                    Edad: {{ calculateAge(b.dob) }}
                 </p>
               </div>
               <Badge v-if="selectedBeneficiary?.id === b.id">✓ Seleccionado</Badge>
             </li>
          </ul>
        </div>

        <!-- Step 2 -->
        <div class="space-y-4" :class="{'opacity-50 pointer-events-none': !selectedBeneficiary}">
          <h3 class="text-xl font-semibold text-foreground border-b border-border pb-2">2. Seleccionar Actividad y Evento</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <Label class="mb-1">Actividad</Label>
              <select v-model="selectedActivity" @change="updateEvents"
                class="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring">
                <option :value="null" disabled>Selecciona una opción...</option>
                <option v-for="act in activities" :key="act.id" :value="act">{{ act.name }}</option>
              </select>
            </div>
            <div>
              <Label class="mb-1">Evento</Label>
              <select v-model="selectedEvent" :disabled="!selectedActivity"
                class="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:bg-muted disabled:text-muted-foreground">
                <option :value="null" disabled>Selecciona un evento...</option>
                <option v-for="ev in availableEvents" :key="ev.id" :value="ev">{{ ev.name }}</option>
              </select>
            </div>
          </div>
        </div>

        <div v-if="submissionSuccess" class="p-4 bg-emerald-50 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-400 rounded-lg border border-emerald-200 dark:border-emerald-800">
           ✅ ¡Asistencia registrada exitosamente!
        </div>

        <div v-if="submissionError" class="p-4 bg-destructive/10 text-destructive rounded-lg border border-destructive/20 flex items-start gap-3">
            <AlertTriangle class="w-6 h-6 shrink-0 mt-0.5" />
            <div>
               <p class="font-bold">Error de Registro</p>
               <p class="text-sm mt-1">{{ submissionError }}</p>
            </div>
        </div>

        <div class="pt-4">
          <Button type="submit" :disabled="!selectedBeneficiary || !selectedEvent || loading" class="w-full h-12 text-lg font-bold">
            {{ loading ? 'Guardando...' : 'Registrar Asistencia' }}
          </Button>
        </div>

        </form>
      </div>

    <!-- Public Register Modal -->
    <Dialog :open="showRegisterForm" @update:open="showRegisterForm = $event">
      <DialogHeader>
        <DialogTitle>Primer Registro</DialogTitle>
      </DialogHeader>
      <p class="text-sm text-muted-foreground mb-6">Completa tus datos para crear tu perfil en la plataforma.</p>
      
      <form @submit.prevent="submitRegistration" class="space-y-5">
          <div class="grid grid-cols-2 gap-4">
              <div>
                  <Label class="mb-1">Nombre *</Label>
                  <Input v-model="regForm.first_name" required type="text" />
              </div>
              <div>
                  <Label class="mb-1">Apellido *</Label>
                  <Input v-model="regForm.last_name" required type="text" />
              </div>
          </div>
          <div>
             <Label class="mb-1">Cédula o ID (Opcional)</Label>
             <Input v-model="regForm.ci" type="text" />
          </div>
          <div class="grid grid-cols-2 gap-4">
              <div>
                  <Label class="mb-1">Fecha de Nac. *</Label>
                  <Input v-model="regForm.dob" required type="date" />
              </div>
              <div>
                  <Label class="mb-1">Sexo *</Label>
                  <select v-model="regForm.sex" required class="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring">
                      <option value="M">Masculino</option>
                      <option value="F">Femenino</option>
                      <option value="O">Otro</option>
                  </select>
              </div>
          </div>
          <div>
             <Label class="mb-1">Sector / Ubicación *</Label>
             <Input v-model="regForm.sector" required type="text" />
          </div>
          <div v-if="regError" class="text-sm text-destructive bg-destructive/10 p-3 rounded-lg border border-destructive/20">
              {{ regError }}
          </div>
          <div class="flex justify-end gap-3 mt-8 pt-4 border-t">
              <Button type="button" variant="outline" @click="showRegisterForm = false">Cancelar</Button>
              <Button type="submit" :disabled="regLoading">
                  {{ regLoading ? 'Creando Perfil...' : 'Crear Perfil' }}
              </Button>
          </div>
      </form>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import apiClient from '../plugins/axios'
import { ArrowLeft, Plus, AlertTriangle } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Badge } from '@/components/ui/badge'
import { Dialog, DialogHeader, DialogTitle } from '@/components/ui/dialog'

const calculateAge = (dobString) => {
    if (!dobString) return '?';
    const dob = new Date(dobString);
    const diff_ms = Date.now() - dob.getTime();
    const age_dt = new Date(diff_ms); 
    return Math.abs(age_dt.getUTCFullYear() - 1970);
}

const searchQuery = ref('')
const beneficiaries = ref([])
const selectedBeneficiary = ref(null)
const activities = ref([])
const selectedActivity = ref(null)
const availableEvents = ref([])
const selectedEvent = ref(null)
const loading = ref(false)
const submissionSuccess = ref(false)
const submissionError = ref('')
const showRegisterForm = ref(false)
const regLoading = ref(false)
const regError = ref('')
const regForm = ref({ ci: '', first_name: '', last_name: '', dob: '', sex: 'M', sector: '' })

import { useRoute } from 'vue-router'
const route = useRoute()
const orgSlug = computed(() => route.query.org || 'las-mananitas')

const fetchActivities = async () => {
    try {
        const res = await apiClient.get(`public/activities/?org=${orgSlug.value}`)
        activities.value = res.data
    } catch (e) { console.error("Error fetching activities", e) }
}

const searchBeneficiaries = async () => {
    if (!searchQuery.value) return;
    try {
        const res = await apiClient.get(`public/beneficiaries/?search=${searchQuery.value}&org=${orgSlug.value}`)
        beneficiaries.value = res.data
        if (res.data.length === 0) alert("No se encontró ningún usuario con ese criterio.")
    } catch (e) { console.error("Error searching", e) }
}

const selectBeneficiary = (b) => { selectedBeneficiary.value = b }

const updateEvents = () => {
    selectedEvent.value = null
    availableEvents.value = selectedActivity.value?.events || []
}

const submitAttendance = async () => {
    loading.value = true
    submissionSuccess.value = false
    submissionError.value = ''
    try {
        await apiClient.post(`public/attendance/?org=${orgSlug.value}`, {
            beneficiary: selectedBeneficiary.value.id,
            event: selectedEvent.value.id
        })
        submissionSuccess.value = true
        setTimeout(() => {
            selectedBeneficiary.value = null
            searchQuery.value = ''
            beneficiaries.value = []
            submissionSuccess.value = false
        }, 3000)
    } catch (e) {
        console.error("Error saving attendance", e)
        submissionError.value = "Lo sentimos, no puedes marcar asistencia 2 veces para la misma actividad y evento."
        setTimeout(() => { submissionError.value = '' }, 5000)
    } finally { loading.value = false }
}

const submitRegistration = async () => {
    regLoading.value = true
    regError.value = ''
    try {
        const res = await apiClient.post(`public/beneficiaries/?org=${orgSlug.value}`, regForm.value)
        selectedBeneficiary.value = res.data
        searchQuery.value = res.data.first_name + ' ' + res.data.last_name
        beneficiaries.value = [res.data]
        showRegisterForm.value = false
        regForm.value = { ci: '', first_name: '', last_name: '', dob: '', sex: 'M', sector: '' }
        alert("Perfil creado existosamente! Ahora solo selecciona tu actividad.")
    } catch (e) {
        console.error("Error creating profile", e)
        regError.value = e.response?.data?.ci ? "Ya existe un usuario con esta Cédula / ID." : "Hubo un error al crear el perfil. Revisa tus datos."
    } finally { regLoading.value = false }
}

onMounted(() => { fetchActivities() })
</script>
