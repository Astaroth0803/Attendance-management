<template>
  <div class="min-h-screen bg-background transition-colors duration-200">
    <div class="max-w-[1400px] mx-auto p-6 md:p-8 space-y-6">

      <!-- Back button -->
      <div v-if="activeExcursion" class="mb-4">
        <Button variant="ghost" @click="activeExcursion = null" class="text-primary hover:bg-primary/10 -ml-2">
          <ArrowLeft class="h-5 w-5 mr-1" /> Volver
        </Button>
      </div>

      <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6 mb-6">
        <h1 class="text-3xl font-bold text-foreground break-words max-w-full lg:max-w-[45%]">
          {{ activeExcursion ? `Gestión: ${activeExcursion.nombre}` : 'Eventos Especiales' }}
        </h1>
        <Button v-if="!activeExcursion" @click="showCreateModal = true">
          <Plus class="w-4 h-4 mr-1" /> Nueva Excursión
        </Button>
      </div>

      <!-- Main LIST View -->
      <div v-if="!activeExcursion" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card v-for="exc in excursions" :key="exc.id" class="flex flex-col overflow-hidden hover:shadow-md transition-shadow">
          <CardContent class="p-6 flex-grow">
            <div class="flex justify-between items-start mb-4">
              <h2 class="text-xl font-bold text-foreground line-clamp-2 leading-tight" :title="exc.nombre">{{ exc.nombre }}</h2>
              <Badge :class="stateBadgeClass(exc.estado)" class="shrink-0 ml-2 border-0">
                {{ formatState(exc.estado) }}
              </Badge>
            </div>
            <div class="space-y-3 mb-6">
              <div class="flex items-center text-muted-foreground">
                <Calendar class="h-5 w-5 mr-3 text-primary" />
                <span class="text-base font-medium">{{ exc.fecha_evento }}</span>
              </div>
              <div class="flex items-center text-muted-foreground">
                <Users class="h-5 w-5 mr-3 text-primary" />
                <span class="text-base font-medium">{{ exc.inscritos_count }} Inscritos</span>
              </div>
              <div class="flex items-center text-muted-foreground" v-if="exc.edad_min > 0 || exc.edad_max < 99">
                <Clock class="h-5 w-5 mr-3 text-primary" />
                <span class="text-sm font-medium">De {{ exc.edad_min }} a {{ exc.edad_max }} años</span>
              </div>
            </div>
            <p v-if="exc.descripcion" class="text-muted-foreground text-sm line-clamp-2 mt-4">{{ exc.descripcion }}</p>
          </CardContent>
          <div class="px-6 py-4 bg-muted/50 border-t">
            <Button @click="manageExcursion(exc)" variant="outline" class="w-full text-primary border-primary/20 hover:bg-primary/5 font-bold">
              <Settings2 class="h-5 w-5 mr-2" /> Gestionar
            </Button>
          </div>
        </Card>

        <!-- Empty State -->
        <Card v-if="excursions.length === 0" class="col-span-full">
          <CardContent class="text-center p-12">
            <Map class="h-16 w-16 mx-auto text-muted-foreground/30 mb-4" />
            <h3 class="text-xl font-medium text-foreground mb-2">No hay excursiones</h3>
            <p class="text-muted-foreground mb-6 text-base">Crea la primera excursión para empezar a administrar participantes.</p>
            <Button @click="showCreateModal = true">Crear Primera Excursión</Button>
          </CardContent>
        </Card>
      </div>

      <!-- DETAIL View -->
      <div v-if="activeExcursion" class="space-y-8">
        <!-- Header Controls & Status -->
        <Card class="overflow-hidden">
          <div class="bg-primary/5 p-6 border-b">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div>
                <p class="text-sm font-bold text-primary uppercase tracking-wider mb-1">Estado General</p>
                <Badge :class="stateBadgeClass(activeExcursion.estado)" class="px-4 py-1.5 text-sm border-0 shadow-sm">
                  {{ formatState(activeExcursion.estado) }}
                </Badge>
              </div>
              <div class="flex flex-wrap gap-3">
                <Button v-if="activeExcursion.estado === 'pendiente_registro'" @click="advanceState('registro_cerrado')" class="bg-blue-600 hover:bg-blue-700">
                  <Lock class="h-5 w-5 mr-2" /> Cerrar Registro
                </Button>
                <Button v-if="activeExcursion.estado === 'registro_cerrado'" @click="advanceState('dia_evento')" class="bg-indigo-600 hover:bg-indigo-700">
                  <Play class="h-5 w-5 mr-2" /> Iniciar Día de Evento
                </Button>
                <Button v-if="activeExcursion.estado === 'dia_evento'" @click="advanceState('finalizado')" class="bg-foreground hover:bg-foreground/90">
                  <Check class="h-5 w-5 mr-2" /> Finalizar Excursión
                </Button>
                <Button v-if="['pendiente_registro', 'registro_cerrado', 'dia_evento'].includes(activeExcursion.estado)" @click="advanceState('cancelado')" variant="outline" class="text-destructive border-destructive/30 hover:bg-destructive/10 ml-auto">
                  <XCircle class="h-5 w-5 mr-2" /> Cancelar Evento
                </Button>
              </div>
            </div>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-3 divide-y sm:divide-y-0 sm:divide-x divide-border">
            <div class="p-6 flex items-start gap-4">
              <div class="p-3 bg-blue-100 dark:bg-blue-900/30 text-blue-600 rounded-lg">
                <Calendar class="h-6 w-6" />
              </div>
              <div>
                <p class="text-sm font-medium text-muted-foreground mb-1">Fecha Programada</p>
                <p class="text-lg font-bold text-foreground">{{ activeExcursion.fecha_evento }}</p>
              </div>
            </div>
            <div class="p-6 flex items-start gap-4">
              <div class="p-3 bg-green-100 dark:bg-green-900/30 text-green-600 rounded-lg">
                <Users class="h-6 w-6" />
              </div>
              <div>
                <p class="text-sm font-medium text-muted-foreground mb-1">Personas Inscritas</p>
                <p class="text-lg font-bold text-foreground">{{ activeExcursion.inscritos_count }} participantes</p>
              </div>
            </div>
            <div class="p-6 flex items-start gap-4">
              <div class="p-3 bg-purple-100 dark:bg-purple-900/30 text-purple-600 rounded-lg">
                <Shield class="h-6 w-6" />
              </div>
              <div>
                <p class="text-sm font-medium text-muted-foreground mb-1">Requisitos</p>
                <p class="text-sm font-bold text-foreground">Edad: {{ activeExcursion.edad_min }} - {{ activeExcursion.edad_max }} años</p>
                <p class="text-sm text-muted-foreground mt-0.5">Asist. previas necesarias: {{ activeExcursion.min_asistencias }}</p>
              </div>
            </div>
          </div>
          <div class="p-6 bg-muted/30 border-t" v-if="activeExcursion.descripcion">
            <p class="text-sm font-bold text-foreground mb-2">Descripción Oficial</p>
            <p class="text-muted-foreground text-base leading-relaxed">{{ activeExcursion.descripcion }}</p>
          </div>
        </Card>

        <!-- Add Participant Section (Only in pendiente_registro) -->
        <Card v-if="activeExcursion.estado === 'pendiente_registro'" class="overflow-hidden">
          <CardHeader class="bg-muted/50 border-b">
            <CardTitle class="flex items-center text-lg"><UserPlus class="h-6 w-6 mr-2 text-indigo-500" /> Inscribir Nuevos Participantes</CardTitle>
          </CardHeader>
          <CardContent class="p-6">
            <div class="relative">
              <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
              <Input v-model="userSearchQuery" @input="searchUsers" type="text" placeholder="Escribe el nombre o número de cédula para buscar..." class="pl-11 h-12 text-lg" />
            </div>
            <!-- Found Users List -->
            <div v-if="foundUsers.length > 0" class="mt-4 border rounded-lg divide-y overflow-hidden shadow-sm">
              <div v-for="user in foundUsers" :key="user.id" class="p-4 flex flex-col sm:flex-row justify-between items-start sm:items-center hover:bg-primary/5 transition-colors gap-4">
                <div class="flex items-center gap-4">
                  <div class="bg-muted h-10 w-10 rounded-full flex items-center justify-center shrink-0">
                    <span class="text-foreground font-bold text-lg">{{ user.first_name.charAt(0) }}</span>
                  </div>
                  <div>
                    <p class="font-bold text-foreground text-lg">{{ user.first_name }} {{ user.last_name }}</p>
                    <p class="text-sm text-muted-foreground flex items-center gap-2">
                      <Badge variant="secondary" class="text-xs">CI: {{ user.ci }}</Badge>
                      <span class="truncate max-w-[200px]" v-if="user.sector">{{ user.sector }}</span>
                    </p>
                  </div>
                </div>
                <Button @click="registerParticipant(user.id)" :disabled="isRegistering" class="w-full sm:w-auto bg-emerald-600 hover:bg-emerald-700">
                  <Plus class="h-5 w-5 mr-2" /> Matricular
                </Button>
              </div>
            </div>
            <div v-else-if="userSearchQuery.length > 2" class="bg-yellow-50 dark:bg-yellow-900/20 text-yellow-800 dark:text-yellow-200 p-4 rounded-lg mt-4 flex items-center border border-yellow-200 dark:border-yellow-800">
               <AlertTriangle class="h-5 w-5 mr-3 shrink-0" />
               No se encontraron beneficiarios con esa búsqueda, o ya se encuentran matriculados.
            </div>
          </CardContent>
        </Card>

        <!-- Participants List -->
        <Card class="overflow-hidden w-full">
          <CardHeader class="bg-muted/50 border-b flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <CardTitle class="flex items-center text-xl"><Users class="h-6 w-6 mr-2 text-muted-foreground" /> Listado Final de Participantes</CardTitle>
            <div class="flex flex-col sm:flex-row gap-3 w-full sm:w-auto">
              <Button v-if="['registro_cerrado', 'dia_evento', 'finalizado'].includes(activeExcursion.estado) && activeExcursion.registros && activeExcursion.registros.length > 0" @click="exportToExcel" variant="outline" class="text-emerald-600 border-emerald-200 hover:bg-emerald-50">
                <FileSpreadsheet class="h-5 w-5 mr-2" /> Excel
              </Button>
              <Button v-if="['registro_cerrado', 'dia_evento', 'finalizado'].includes(activeExcursion.estado) && activeExcursion.registros && activeExcursion.registros.length > 0" @click="exportToPDF" variant="outline" class="text-destructive border-red-200 hover:bg-red-50">
                <FileText class="h-5 w-5 mr-2" /> PDF
              </Button>
              <Button v-if="activeExcursion.estado === 'dia_evento'" @click="saveAttendance" :disabled="isSavingAttendance" class="bg-emerald-600 hover:bg-emerald-700">
                <Save class="h-5 w-5 mr-2" /> Guardar Reporte de Asistencia
              </Button>
            </div>
          </CardHeader>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-border">
              <thead class="bg-muted/30">
                <tr>
                  <th class="px-6 py-4 text-left text-sm font-bold text-muted-foreground uppercase tracking-wider">Beneficiario</th>
                  <th class="px-6 py-4 text-left text-sm font-bold text-muted-foreground uppercase tracking-wider">Registrado el</th>
                  <th class="px-6 py-4 text-left text-sm font-bold text-muted-foreground uppercase tracking-wider">Control de Asistencia</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-border">
                <tr v-for="(reg, index) in activeExcursion.registros" :key="reg.id" class="hover:bg-muted/30 transition-colors" :class="{'bg-muted/10': index % 2 === 0}">
                  <td class="px-6 py-4">
                    <div class="flex items-center">
                      <div class="h-10 w-10 shrink-0 bg-primary/10 text-primary rounded-full flex items-center justify-center font-bold text-lg mr-4">
                        {{ reg.beneficiary_details.first_name.charAt(0) }}
                      </div>
                      <div>
                        <div class="font-bold text-foreground text-lg">{{ reg.beneficiary_details.first_name }} {{ reg.beneficiary_details.last_name }}</div>
                        <div class="text-sm font-medium text-muted-foreground mt-0.5">CI: {{ reg.beneficiary_details.ci }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 text-muted-foreground text-base">
                    {{ new Date(reg.fecha_registro).toLocaleDateString() }} a las {{ new Date(reg.fecha_registro).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) }}
                  </td>
                  <td class="px-6 py-4">
                    <!-- Day of Event Attendance Controls -->
                    <div v-if="activeExcursion.estado === 'dia_evento'" class="flex items-center gap-6 bg-muted p-2 rounded-lg inline-flex border shadow-inner">
                          <label class="flex items-center gap-2 cursor-pointer group">
                             <div class="relative flex items-center">
                               <input type="radio" :name="'att_'+reg.usuario" :value="true" v-model="attendanceForm[reg.usuario]" class="peer sr-only">
                               <div class="w-6 h-6 border-2 border-border rounded-full peer-checked:border-green-600 peer-checked:bg-green-600 transition-all flex items-center justify-center">
                                 <svg class="w-4 h-4 text-white opacity-0 peer-checked:opacity-100" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
                               </div>
                             </div>
                             <span class="text-lg font-bold text-muted-foreground group-hover:text-foreground peer-checked:text-green-700">Asistió</span>
                          </label>
                          <label class="flex items-center gap-2 cursor-pointer group">
                             <div class="relative flex items-center">
                               <input type="radio" :name="'att_'+reg.usuario" :value="false" v-model="attendanceForm[reg.usuario]" class="peer sr-only">
                               <div class="w-6 h-6 border-2 border-border rounded-full peer-checked:border-red-600 peer-checked:bg-red-600 transition-all flex items-center justify-center">
                                 <svg class="w-4 h-4 text-white opacity-0 peer-checked:opacity-100" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>
                               </div>
                             </div>
                             <span class="text-lg font-bold text-muted-foreground group-hover:text-foreground peer-checked:text-red-700">Faltó</span>
                          </label>
                    </div>
                    <!-- Finished Status Output -->
                    <div v-else class="flex">
                      <Badge v-if="reg.asistio === true" class="bg-green-100 text-green-800 border-0 text-base px-3 py-1">✓ Estuvo Presente</Badge>
                      <Badge v-else-if="reg.asistio === false" class="bg-red-100 text-red-800 border-0 text-base px-3 py-1">✗ Marcó Falta</Badge>
                      <Badge v-else variant="secondary" class="text-base px-3 py-1">⏳ Aún Pendiente</Badge>
                    </div>
                  </td>
                </tr>
                <tr v-if="!activeExcursion.registros || activeExcursion.registros.length === 0">
                  <td colspan="3" class="px-6 py-12 text-center">
                    <Users class="h-12 w-12 mx-auto text-muted-foreground/30 mb-3" />
                    <p class="text-lg font-medium text-muted-foreground">Aún no hay personas inscritas.</p>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </Card>
      </div>

      <!-- Create Modal -->
      <Dialog :open="showCreateModal" @update:open="showCreateModal = $event" class="max-w-lg">
        <DialogHeader>
          <DialogTitle class="flex items-center"><Plus class="h-6 w-6 mr-2 text-primary" /> Agendando Evento Nuevo</DialogTitle>
        </DialogHeader>
        <div class="bg-blue-50 dark:bg-blue-900/20 text-blue-800 dark:text-blue-200 p-4 rounded-lg flex items-start text-sm border border-blue-100 dark:border-blue-800 mb-4">
          <Info class="h-5 w-5 mr-3 mt-0.5 shrink-0" />
          <p>Complete los datos para generar el evento. Podrá inscribir usuarios una vez lo haya guardado.</p>
        </div>
        <form @submit.prevent="saveExcursion" class="space-y-5">
          <div>
            <Label class="mb-1">Título de la Excursión o Evento</Label>
            <Input v-model="form.nombre" type="text" placeholder="Ej: Visita al Museo Nacional" />
          </div>
          <div>
            <Label class="mb-1">Descripción General (Opcional)</Label>
            <textarea v-model="form.descripcion" rows="2" placeholder="Información útil sobre la excursión..." class="flex min-h-[60px] w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"></textarea>
          </div>
          <div>
            <Label class="mb-1">Fecha Programada</Label>
            <Input v-model="form.fecha_evento" type="date" />
          </div>
          <div class="pt-4 mt-2 border-t">
            <h4 class="font-bold text-foreground mb-4 text-lg">Reglas y Requisitos para Participar</h4>
            <div class="grid grid-cols-2 gap-6">
              <div>
                <Label class="mb-1">Edad Mínima</Label>
                <Input v-model="form.edad_min" type="number" />
              </div>
              <div>
                <Label class="mb-1">Edad Máxima</Label>
                <Input v-model="form.edad_max" type="number" />
              </div>
            </div>
            <div class="mt-5">
              <Label class="mb-1">Asistencias obligatorias previas (0 = Ninguna)</Label>
              <Input v-model="form.min_asistencias" type="number" />
            </div>
          </div>
          <div class="flex justify-end gap-3 mt-6 pt-4 border-t">
            <Button type="button" variant="outline" @click="showCreateModal = false">Cancelar</Button>
            <Button type="submit" :disabled="isSaving">
              {{ isSaving ? 'Guardando...' : 'Guardar Excursión' }}
            </Button>
          </div>
        </form>
      </Dialog>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import apiClient from '../plugins/axios'
import * as XLSX from 'xlsx'
import jsPDF from 'jspdf'
import 'jspdf-autotable'
import { ArrowLeft, Plus, Calendar, Users, Clock, Settings2, Map, Lock, Play, Check, XCircle, Shield, UserPlus, Search, AlertTriangle, FileSpreadsheet, FileText, Save, Info } from 'lucide-vue-next'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Dialog, DialogHeader, DialogTitle } from '@/components/ui/dialog'

const excursions = ref([])
const activeExcursion = ref(null)
const showCreateModal = ref(false)
const isSaving = ref(false)
const isRegistering = ref(false)
const isSavingAttendance = ref(false)

const form = ref({
    nombre: '', descripcion: '', fecha_evento: '', edad_min: 0, edad_max: 99, min_asistencias: 0
})

const userSearchQuery = ref('')
const foundUsers = ref([])
const attendanceForm = reactive({})

const fetchExcursions = async () => {
    try { const res = await apiClient.get('excursions/'); excursions.value = res.data } catch (e) { console.error(e) }
}

const saveExcursion = async () => {
    isSaving.value = true
    try {
        await apiClient.post('excursions/', form.value)
        showCreateModal.value = false
        form.value = { nombre: '', descripcion: '', fecha_evento: '', edad_min: 0, edad_max: 99, min_asistencias: 0 }
        await fetchExcursions()
    } catch (e) { alert("Error al crear la excursión."); console.error(e) } finally { isSaving.value = false }
}

const manageExcursion = async (exc) => {
    try {
        const res = await apiClient.get(`excursions/${exc.id}/`)
        activeExcursion.value = res.data
        if (res.data.estado === 'dia_evento') {
           res.data.registros.forEach(r => { if (r.asistio !== null) attendanceForm[r.usuario] = r.asistio })
        }
    } catch (e) { console.error(e) }
}

const searchTimer = ref(null)
const searchUsers = () => {
    clearTimeout(searchTimer.value)
    if (userSearchQuery.value.length < 3) { foundUsers.value = []; return }
    searchTimer.value = setTimeout(async () => {
        try {
            const res = await apiClient.get(`beneficiaries/`)
            const q = userSearchQuery.value.toLowerCase()
            const filtered = res.data.filter(u => {
                const name = `${u.first_name} ${u.last_name}`.toLowerCase()
                return name.includes(q) || (u.ci || '').toLowerCase().includes(q)
            })
            const existingIds = activeExcursion.value.registros.map(r => r.usuario)
            foundUsers.value = filtered.filter(u => !existingIds.includes(u.id)).slice(0, 10)
        } catch (e) { console.error(e) }
    }, 400)
}

const registerParticipant = async (userId) => {
    isRegistering.value = true
    try {
        await apiClient.post(`excursions/${activeExcursion.value.id}/register/`, { usuario_id: userId })
        userSearchQuery.value = ''; foundUsers.value = []
        alert("Participante registrado de forma exitosa.")
        await manageExcursion(activeExcursion.value)
    } catch (e) {
        alert(e.response?.data?.detail || "Error al registrar participante.")
    } finally { isRegistering.value = false }
}

const advanceState = async (newState) => {
    if (['registro_cerrado', 'dia_evento'].includes(newState)) {
        if (!activeExcursion.value.registros || activeExcursion.value.registros.length < 2) {
            alert("Se requieren al menos 2 participantes registrados."); return
        }
    }
    if (!confirm(`¿Actualizar estado a: ${formatState(newState)}?`)) return
    try {
        await apiClient.post(`excursions/${activeExcursion.value.id}/change-state/`, { estado: newState })
        await manageExcursion(activeExcursion.value); await fetchExcursions()
    } catch (e) { alert(e.response?.data?.detail || "Error al actualizar estado.") }
}

const saveAttendance = async () => {
    isSavingAttendance.value = true
    try {
        await apiClient.post(`excursions/${activeExcursion.value.id}/attendance/`, { attendance: attendanceForm })
        alert("Asistencia guardada con éxito.")
        await manageExcursion(activeExcursion.value)
    } catch (e) { alert(e.response?.data?.detail || "Error al guardar la asistencia.") } finally { isSavingAttendance.value = false }
}

const formatState = (state) => {
    const map = { 'pendiente_registro': 'Pendiente', 'registro_cerrado': 'Registro Cerrado', 'dia_evento': 'Día del Evento', 'finalizado': 'Finalizado', 'cancelado': 'Cancelado' }
    return map[state] || state
}

const stateBadgeClass = (state) => {
    if (state === 'pendiente_registro') return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300'
    if (state === 'registro_cerrado') return 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300'
    if (state === 'dia_evento') return 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900/30 dark:text-indigo-300'
    if (state === 'finalizado') return 'bg-muted text-muted-foreground'
    if (state === 'cancelado') return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300'
    return 'bg-muted text-muted-foreground'
}

const getExportData = () => {
    return activeExcursion.value.registros.map((r, i) => ({
        'N°': i + 1, 'Cédula de Identidad': r.beneficiary_details.ci,
        'Nombre Completo': `${r.beneficiary_details.first_name} ${r.beneficiary_details.last_name}`,
        'Fecha de Registro': new Date(r.fecha_registro).toLocaleString(),
        'Estado de Asistencia': r.asistio === true ? 'Presente' : r.asistio === false ? 'Ausente' : 'Pendiente'
    }))
}

const getReportFilename = (ext) => {
    const rawName = activeExcursion.value.nombre.replace(/[^a-z0-9]/gi, '_').toLowerCase()
    return `excursion_${rawName}_${new Date().toISOString().split('T')[0]}.${ext}`
}

const exportToExcel = () => {
    const data = getExportData()
    const ws = XLSX.utils.json_to_sheet(data)
    ws['!cols'] = [{ wch: 5 }, { wch: 15 }, { wch: 35 }, { wch: 25 }, { wch: 20 }]
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, ws, "Asistentes")
    XLSX.writeFile(wb, getReportFilename('xlsx'))
}

const exportToPDF = () => {
    const doc = new jsPDF()
    const data = getExportData()
    doc.setFontSize(18); doc.text("Listado Final de Participantes", 14, 22)
    doc.setFontSize(11); doc.setTextColor(100)
    doc.text(`Excursión: ${activeExcursion.value.nombre}`, 14, 30)
    doc.text(`Fecha del Evento: ${activeExcursion.value.fecha_evento}`, 14, 36)
    doc.text(`Estado: ${formatState(activeExcursion.value.estado)}`, 14, 42)
    doc.text(`Total Inscritos: ${activeExcursion.value.inscritos_count}`, 14, 48)
    const cols = ["N°", "Cédula", "Nombre Completo", "Fecha de Registro", "Asistencia"]
    const rows = data.map(r => [r['N°'], r['Cédula de Identidad'], r['Nombre Completo'], r['Fecha de Registro'], r['Estado de Asistencia']])
    doc.autoTable({ head: [cols], body: rows, startY: 55, theme: 'striped', headStyles: { fillColor: [234, 88, 12] } })
    doc.save(getReportFilename('pdf'))
}

onMounted(() => { fetchExcursions() })
</script>
