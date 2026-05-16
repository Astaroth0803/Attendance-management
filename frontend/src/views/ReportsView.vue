<template>
  <div class="min-h-screen bg-background transition-colors duration-200">
    <div class="max-w-[1400px] mx-auto p-6 md:p-8 flex flex-col md:flex-row gap-8">
      
      <!-- STEP 1: Select Report Type -->
      <div v-if="!selectedReport" class="w-full">
        <h1 class="text-3xl font-extrabold text-foreground mb-2">Centro de Reportes</h1>
        <p class="text-muted-foreground mb-8 text-lg">Selecciona el tipo de informe que deseas generar y exportar.</p>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card @click="selectedReport = 'attendance'" class="p-6 cursor-pointer hover:shadow-md hover:border-primary/30 transition-all text-left group flex flex-col h-full hover:-translate-y-1 duration-200">
            <div class="w-12 h-12 bg-primary/10 text-primary rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <Star class="w-6 h-6" />
            </div>
            <h3 class="text-lg font-bold text-foreground mb-1">Asistencias por Día</h3>
            <p class="text-muted-foreground text-sm leading-relaxed">Listado cronológico de ingresos a fecha y hora determinada.</p>
          </Card>

          <Card @click="selectedReport = 'activities'" class="p-6 cursor-pointer hover:shadow-md hover:border-primary/30 transition-all text-left group flex flex-col h-full hover:-translate-y-1 duration-200">
            <div class="w-12 h-12 bg-emerald-100 dark:bg-emerald-900/20 text-emerald-600 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <BarChart3 class="w-6 h-6" />
            </div>
            <h3 class="text-lg font-bold text-foreground mb-1">Actividades más visitadas</h3>
            <p class="text-muted-foreground text-sm leading-relaxed">Actividades con más asistencias únicas en un rango.</p>
          </Card>

          <Card @click="selectedReport = 'events'" class="p-6 cursor-pointer hover:shadow-md hover:border-primary/30 transition-all text-left group flex flex-col h-full hover:-translate-y-1 duration-200">
            <div class="w-12 h-12 bg-blue-100 dark:bg-blue-900/20 text-blue-600 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <CalendarRange class="w-6 h-6" />
            </div>
            <h3 class="text-lg font-bold text-foreground mb-1">Por Evento</h3>
            <p class="text-muted-foreground text-sm leading-relaxed">Cuántas personas únicas asistieron a los eventos específicos.</p>
          </Card>

          <Card @click="selectedReport = 'risk'; fetchRiskReport()" class="p-6 cursor-pointer hover:shadow-md hover:border-destructive/50 transition-all text-left group flex flex-col h-full hover:-translate-y-1 duration-200 border-destructive/20 bg-destructive/5">
            <div class="w-12 h-12 bg-destructive/10 text-destructive rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform group-hover:bg-destructive group-hover:text-white">
              <AlertTriangle class="w-6 h-6" />
            </div>
            <h3 class="text-lg font-bold text-destructive mb-1">Riesgo de Abandono</h3>
            <p class="text-muted-foreground text-sm leading-relaxed">Identifica a los usuarios que dejaron de asistir recientemente para seguimiento.</p>
          </Card>
        </div>
      </div>
      
      <!-- STEP 2: Report View -->
      <div v-else class="flex-1 space-y-6 w-full">
        <Button variant="ghost" @click="selectedReport = null; hasSearched = false" class="text-primary -ml-2 mb-4">
          <ArrowLeft class="h-5 w-5 mr-1" /> Volver a opciones
        </Button>

        <div class="flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
            <div>
                <h2 class="text-3xl font-bold text-foreground tracking-tight">
                    {{ selectedReport === 'attendance' ? 'Reporte de Asistencia' : selectedReport === 'activities' ? 'Actividades con más asistencias' : selectedReport === 'events' ? 'Reporte por Evento' : 'Riesgo de Abandono (Churn)' }}
                </h2>
                <p class="text-muted-foreground mt-2 text-lg">Filtra y exporta el historial.</p>
            </div>
            <div class="flex gap-3 mt-4 md:mt-0 w-full md:w-auto">
                <Button @click="exportToPDF" :disabled="!currentRecords.length" variant="outline" class="flex-1 md:flex-none text-destructive border-red-200 hover:bg-red-50">
                    <FileText class="w-5 h-5 mr-2" /> PDF
                </Button>
                <Button @click="exportToExcel" :disabled="!currentRecords.length" variant="outline" class="flex-1 md:flex-none text-emerald-600 border-emerald-200 hover:bg-emerald-50">
                    <FileSpreadsheet class="w-5 h-5 mr-2" /> Excel
                </Button>
            </div>
        </div>

        <!-- Filters -->
        <Card class="p-8">
            <div class="flex flex-wrap items-end gap-6 mb-6">
                <div class="flex-1 min-w-[160px]">
                    <Label class="mb-2">Fecha de Inicio</Label>
                    <Input type="date" v-model="filters.start_date" />
                </div>
                <div class="flex-1 min-w-[160px]">
                    <Label class="mb-2">Fecha Final</Label>
                    <Input type="date" v-model="filters.end_date" />
                </div>
                <template v-if="selectedReport === 'attendance'">
                    <div class="flex-1 min-w-[130px]">
                        <Label class="mb-2">Hora de Inicio</Label>
                        <Input type="time" v-model="filters.start_time" />
                    </div>
                    <div class="flex-1 min-w-[130px]">
                        <Label class="mb-2">Hora Final</Label>
                        <Input type="time" v-model="filters.end_time" />
                    </div>
                </template>
                <Button @click="fetchReport" class="uppercase text-sm tracking-widest mt-4 md:mt-0 w-full md:w-auto">
                    BUSCAR
                </Button>
            </div>

            <!-- Quick Actions -->
            <div class="flex flex-wrap gap-4 mt-8 justify-start">
                <button v-for="q in quickFilters" :key="q.key" @click="setQuickFilter(q.key)" class="w-16 h-16 rounded-full bg-primary text-primary-foreground font-bold text-xs shadow-md hover:bg-primary/90 hover:-translate-y-1 flex items-center justify-center transition-all duration-200 text-center leading-tight">
                    <span v-html="q.label"></span>
                </button>
            </div>
        </Card>

        <!-- Tables area -->
        <Card class="overflow-hidden">
          <div v-if="!hasSearched && !loading" class="flex flex-col items-center justify-center py-20 text-muted-foreground gap-3">
            <SearchIcon class="w-12 h-12 text-primary/20" />
            <p class="text-sm font-medium">Selecciona un rango de fechas y presiona <strong class="text-primary">BUSCAR</strong></p>
          </div>

          <div v-else-if="loading" class="flex items-center justify-center py-20 text-muted-foreground">
            Cargando datos...
          </div>

          <template v-else>
            <!-- Table: Attendance History -->
            <table v-if="selectedReport === 'attendance'" class="min-w-full divide-y divide-border">
                <thead class="bg-muted/50">
                    <tr>
                        <th class="px-6 py-4 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Fecha</th>
                        <th class="px-6 py-4 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Hora</th>
                        <th class="px-6 py-4 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Usuario</th>
                        <th class="px-6 py-4 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Cédula</th>
                        <th class="px-6 py-4 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Actividad</th>
                        <th class="px-6 py-4 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Evento / Detalles</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-border">
                    <tr v-for="record in attendanceRecords" :key="record.id" class="hover:bg-muted/30 transition-colors">
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-foreground">{{ record.date }}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground font-mono">{{ record.time }}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-base text-foreground">{{ record.beneficiary_name }}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">{{ record.beneficiary_ci }}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-foreground">{{ record.activity_name }}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">{{ record.event_name }}</td>
                    </tr>
                    <tr v-if="attendanceRecords.length === 0">
                        <td colspan="6" class="px-6 py-12 text-center text-muted-foreground text-lg">Sin resultados para el rango seleccionado.</td>
                    </tr>
                </tbody>
            </table>

            <!-- Table: Top Activities -->
            <table v-if="selectedReport === 'activities'" class="min-w-full divide-y divide-border">
                <thead class="bg-muted/50">
                    <tr>
                        <th class="px-6 py-4 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Actividad</th>
                        <th class="px-6 py-4 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Evento / Detalles</th>
                        <th class="px-6 py-4 text-center text-xs font-bold text-muted-foreground uppercase tracking-wider">Nº de Asistentes Únicos</th>
                        <th class="px-6 py-4 text-center text-xs font-bold text-muted-foreground uppercase tracking-wider w-16">Detalle</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-border">
                    <tr v-for="(record, idx) in activityRecords" :key="idx" class="hover:bg-muted/30 transition-colors">
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-foreground">{{ record.activity_name }}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-foreground">{{ record.event_name }}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-center text-primary bg-primary/5">{{ record.attendees }}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-center">
                            <Button @click="openAttendeesModal(record)" variant="ghost" size="icon" class="h-8 w-8 rounded-full bg-primary/10 text-primary hover:bg-primary hover:text-primary-foreground">
                              <Plus class="w-4 h-4" />
                            </Button>
                        </td>
                    </tr>
                    <tr v-if="activityRecords.length === 0">
                        <td colspan="4" class="px-6 py-12 text-center text-muted-foreground text-lg">Sin resultados para el rango seleccionado.</td>
                    </tr>
                </tbody>
            </table>

            <!-- Table: Por Evento -->
            <table v-if="selectedReport === 'events'" class="min-w-full divide-y divide-border">
                <thead class="bg-muted/50">
                    <tr>
                        <th class="px-6 py-4 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Evento</th>
                        <th class="px-6 py-4 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Actividad</th>
                        <th class="px-6 py-4 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Fecha Evento</th>
                        <th class="px-6 py-4 text-center text-xs font-bold text-muted-foreground uppercase tracking-wider">Asistentes Únicos</th>
                        <th class="px-6 py-4 text-center text-xs font-bold text-muted-foreground uppercase tracking-wider w-16">Detalle</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-border">
                    <tr v-for="(record, idx) in eventRecords" :key="idx" class="hover:bg-muted/30 transition-colors">
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-foreground">{{ record.event_name }}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-foreground">{{ record.activity_name }}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">{{ record.event_date }}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-center text-primary bg-primary/5">{{ record.attendees }}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-center">
                            <Button @click="openAttendeesModal(record)" variant="ghost" size="icon" class="h-8 w-8 rounded-full bg-primary/10 text-primary hover:bg-primary hover:text-primary-foreground">
                              <Plus class="w-4 h-4" />
                            </Button>
                        </td>
                    </tr>
                    <tr v-if="eventRecords.length === 0">
                        <td colspan="5" class="px-6 py-12 text-center text-muted-foreground text-lg">Sin resultados para el rango seleccionado.</td>
                    </tr>
                </tbody>
            </table>
            <!-- Table: Riesgo Abandono -->
            <table v-if="selectedReport === 'risk'" class="min-w-full divide-y divide-border">
                <thead class="bg-muted/50">
                    <tr>
                        <th class="px-6 py-4 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Nombre</th>
                        <th class="px-6 py-4 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Cédula</th>
                        <th class="px-6 py-4 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Teléfono / Sector</th>
                        <th class="px-6 py-4 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Última Asistencia</th>
                        <th class="px-6 py-4 text-center text-xs font-bold text-muted-foreground uppercase tracking-wider">Días de Ausencia</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-border">
                    <tr v-for="(record, idx) in riskRecords" :key="idx" class="hover:bg-muted/30 transition-colors">
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-foreground">{{ record.name }}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-foreground">{{ record.ci }}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">{{ record.phone }} / {{ record.sector }}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">{{ record.last_attendance }}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-center">
                            <Badge variant="destructive" class="bg-destructive/10 text-destructive shadow-none">{{ record.days_since }} días</Badge>
                        </td>
                    </tr>
                    <tr v-if="riskRecords.length === 0">
                        <td colspan="5" class="px-6 py-12 text-center border-emerald-500/20 bg-emerald-500/5 transition-colors">
                          <div class="flex flex-col items-center gap-2">
                             <CheckCircle2 class="text-emerald-500 w-10 h-10" />
                             <p class="text-emerald-700 dark:text-emerald-400 font-medium">No hay usuarios en riesgo de abandono actualmente. ¡Excelente retención!</p>
                          </div>
                        </td>
                    </tr>
                </tbody>
            </table>
          </template>
        </Card>
      </div>
    </div>
  </div>

  <!-- ===== Attendees Detail Modal ===== -->
  <Dialog :open="showAttendeesModal" @update:open="showAttendeesModal = $event" class="max-w-3xl">
    <DialogHeader>
      <DialogTitle>Asistentes: {{ modalRecord?.activity_name }}</DialogTitle>
      <p class="text-sm text-muted-foreground mt-0.5">{{ modalRecord?.event_name }} · {{ filters.start_date }} – {{ filters.end_date }}</p>
    </DialogHeader>
    <!-- Export buttons -->
    <div class="flex items-center gap-3 py-3 border-b bg-muted/30 -mx-6 px-6 mb-4">
      <Button @click="exportAttendeesExcel" :disabled="!attendeesList.length" variant="outline" size="sm" class="text-emerald-600 border-emerald-200 hover:bg-emerald-50">
        <FileSpreadsheet class="w-4 h-4 mr-1" /> Excel
      </Button>
      <Button @click="exportAttendeesPDF" :disabled="!attendeesList.length" variant="outline" size="sm" class="text-destructive border-red-200 hover:bg-red-50">
        <FileText class="w-4 h-4 mr-1" /> PDF
      </Button>
      <span class="ml-auto text-sm font-medium text-muted-foreground">{{ attendeesList.length }} asistente{{ attendeesList.length !== 1 ? 's' : '' }}</span>
    </div>

    <div class="overflow-y-auto max-h-[50vh] -mx-6 px-6">
      <div v-if="modalLoading" class="flex items-center justify-center py-16 text-muted-foreground">Cargando...</div>
      <table v-else class="min-w-full divide-y divide-border">
        <thead class="bg-muted/50 sticky top-0">
          <tr>
            <th class="px-5 py-3 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">#</th>
            <th class="px-5 py-3 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Fecha</th>
            <th class="px-5 py-3 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Hora</th>
            <th class="px-5 py-3 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Nombre</th>
            <th class="px-5 py-3 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Cédula</th>
            <th class="px-5 py-3 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Sector</th>
            <th class="px-5 py-3 text-center text-xs font-bold text-muted-foreground uppercase tracking-wider">Visitas</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-border">
          <tr v-for="(a, i) in attendeesList" :key="i" class="hover:bg-primary/5 transition-colors">
            <td class="px-5 py-3 text-sm text-muted-foreground">{{ i + 1 }}</td>
            <td class="px-5 py-3 text-sm font-bold text-foreground">{{ a.ultima_asistencia }}</td>
            <td class="px-5 py-3 text-sm font-bold text-primary">{{ a.ultima_hora || '—' }}</td>
            <td class="px-5 py-3 text-sm text-foreground">{{ a.nombre }}</td>
            <td class="px-5 py-3 text-sm text-muted-foreground">{{ a.cedula }}</td>
            <td class="px-5 py-3 text-sm text-muted-foreground">{{ a.sector }}</td>
            <td class="px-5 py-3 text-sm text-center">
              <Badge class="text-xs">{{ a.total_visitas }}</Badge>
            </td>
          </tr>
          <tr v-if="!modalLoading && attendeesList.length === 0">
            <td colspan="7" class="px-5 py-10 text-center text-muted-foreground text-lg">No hay asistentes registrados en este período.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import apiClient from '../plugins/axios'
import * as XLSX from 'xlsx'
import { jsPDF } from 'jspdf'
import autoTable from 'jspdf-autotable'
import { Star, BarChart3, CalendarRange, ArrowLeft, FileText, FileSpreadsheet, Search as SearchIcon, Plus, AlertTriangle, CheckCircle2 } from 'lucide-vue-next'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Dialog, DialogHeader, DialogTitle } from '@/components/ui/dialog'

const loading = ref(false)
const hasSearched = ref(false)

const showAttendeesModal = ref(false)
const modalLoading = ref(false)
const modalRecord = ref(null)
const attendeesList = ref([])

const quickFilters = [
  { key: 'hoy', label: 'Hoy' },
  { key: 'ayer', label: 'Ayer' },
  { key: 'semana', label: 'Semana' },
  { key: 'semana_pasada', label: 'Semana<br>pasada' },
  { key: 'mes', label: 'Mes' },
  { key: 'mes_pasado', label: 'Mes<br>pasado' },
]

const openAttendeesModal = async (record) => {
    modalRecord.value = record
    showAttendeesModal.value = true
    modalLoading.value = true
    attendeesList.value = []
    try {
        const params = new URLSearchParams()
        params.append('activity_name', record.activity_name)
        params.append('event_name', record.event_name)
        if (filters.value.start_date) params.append('start_date', filters.value.start_date)
        if (filters.value.end_date) params.append('end_date', filters.value.end_date)
        const res = await apiClient.get(`reports/event-attendees/?${params.toString()}`)
        attendeesList.value = res.data
    } catch (e) { console.error('Error fetching attendees', e) } finally { modalLoading.value = false }
}

const exportAttendeesExcel = () => {
    const ws = XLSX.utils.json_to_sheet(attendeesList.value.map((a, i) => ({
        '#': i + 1, 'Fecha': a.ultima_asistencia, 'Hora': a.ultima_hora || '', 'Nombre': a.nombre,
        'Cédula': a.cedula, 'Sector': a.sector, 'Total Visitas': a.total_visitas,
    })))
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, ws, 'Asistentes')
    XLSX.writeFile(wb, `Asistentes_${modalRecord.value?.activity_name}_${modalRecord.value?.event_name}_${getLocalISODate()}.xlsx`)
}

const exportAttendeesPDF = () => {
    const doc = new jsPDF()
    const title = `Asistentes: ${modalRecord.value?.activity_name} - ${modalRecord.value?.event_name}`
    doc.text(title, 14, 15)
    doc.setFontSize(9); doc.setTextColor(120)
    doc.text(`Período: ${filters.value.start_date} – ${filters.value.end_date}`, 14, 22)
    autoTable(doc, {
        head: [['#', 'Fecha', 'Hora', 'Nombre', 'Cédula', 'Sector', 'Visitas']],
        body: attendeesList.value.map((a, i) => [i + 1, a.ultima_asistencia, a.ultima_hora || '', a.nombre, a.cedula, a.sector, a.total_visitas]),
        startY: 27, theme: 'grid', headStyles: { fillColor: [234, 88, 12] }
    })
    doc.save(`Asistentes_${modalRecord.value?.activity_name}_${getLocalISODate()}.pdf`)
}

const selectedReport = ref(null)
const attendanceRecords = ref([])
const activityRecords = ref([])
const eventRecords = ref([])
const riskRecords = ref([])

const filters = ref({ start_date: '', end_date: '', start_time: '', end_time: '' })

const currentRecords = computed(() => {
    if (selectedReport.value === 'attendance') return attendanceRecords.value
    if (selectedReport.value === 'activities') return activityRecords.value
    if (selectedReport.value === 'events') return eventRecords.value
    if (selectedReport.value === 'risk') return riskRecords.value
    return []
})

watch(selectedReport, () => {
    if (selectedReport.value === 'risk') return; // Risk doesn't need date manual search clearance
    hasSearched.value = false
    attendanceRecords.value = []; activityRecords.value = []; eventRecords.value = []; riskRecords.value = []
    filters.value.start_time = ''; filters.value.end_time = ''
})

const fetchRiskReport = async () => {
    loading.value = true; hasSearched.value = true;
    try {
        const res = await apiClient.get(`reports/retention-risk/`)
        riskRecords.value = res.data
    } catch (e) {
        console.error("Error fetching risk report", e)
    } finally {
        loading.value = false
    }
}

const fetchReport = async () => {
    if (!filters.value.start_date && !filters.value.end_date) return
    loading.value = true; hasSearched.value = true
    try {
        const params = new URLSearchParams()
        if (filters.value.start_date) params.append('start_date', filters.value.start_date)
        if (filters.value.end_date) params.append('end_date', filters.value.end_date)
        if (filters.value.start_time) params.append('start_time', filters.value.start_time)
        if (filters.value.end_time) params.append('end_time', filters.value.end_time)
        if (selectedReport.value === 'attendance') { attendanceRecords.value = (await apiClient.get(`reports/attendance/?${params.toString()}`)).data }
        else if (selectedReport.value === 'activities') { activityRecords.value = (await apiClient.get(`reports/activity-attendance/?${params.toString()}`)).data }
        else { eventRecords.value = (await apiClient.get(`reports/event-report/?${params.toString()}`)).data }
    } catch (e) { console.error("Error fetching report", e) } finally { loading.value = false }
}

const getLocalISODate = (date = new Date()) => {
    const y = date.getFullYear(); const m = String(date.getMonth() + 1).padStart(2, '0'); const d = String(date.getDate()).padStart(2, '0');
    return `${y}-${m}-${d}`;
}

const setQuickFilter = (type) => {
    const today = new Date(); let start, end;
    switch(type) {
        case 'hoy': start = end = today; break;
        case 'ayer': { const y = new Date(today); y.setDate(today.getDate() - 1); start = end = y; break; }
        case 'semana': { const d = (today.getDay() + 6) % 7; start = new Date(today); start.setDate(today.getDate() - d); end = today; break; }
        case 'semana_pasada': { const d2 = (today.getDay() + 6) % 7; end = new Date(today); end.setDate(today.getDate() - d2 - 1); start = new Date(end); start.setDate(end.getDate() - 6); break; }
        case 'mes': start = new Date(today.getFullYear(), today.getMonth(), 1); end = today; break;
        case 'mes_pasado': start = new Date(today.getFullYear(), today.getMonth() - 1, 1); end = new Date(today.getFullYear(), today.getMonth(), 0); break;
    }
    filters.value.start_date = getLocalISODate(start); filters.value.end_date = getLocalISODate(end);
    fetchReport();
}

const exportToExcel = () => {
    let ws;
    if (selectedReport.value === 'attendance') {
        ws = XLSX.utils.json_to_sheet(attendanceRecords.value.map(r => ({ 'Fecha': r.date, 'Hora': r.time, 'Usuario': r.beneficiary_name, 'Cédula': r.beneficiary_ci, 'Actividad': r.activity_name, 'Evento': r.event_name })))
    } else if (selectedReport.value === 'activities') {
        ws = XLSX.utils.json_to_sheet(activityRecords.value.map(r => ({ 'Actividad': r.activity_name, 'Evento': r.event_name, 'Nº de Asistentes Únicos': r.attendees })))
    } else if (selectedReport.value === 'events') {
        ws = XLSX.utils.json_to_sheet(eventRecords.value.map(r => ({ 'Evento': r.event_name, 'Actividad': r.activity_name, 'Fecha Evento': r.event_date, 'Asistentes Únicos': r.attendees })))
    } else if (selectedReport.value === 'risk') {
        ws = XLSX.utils.json_to_sheet(riskRecords.value.map(r => ({ 'Usuario': r.name, 'Cédula': r.ci, 'Teléfono': r.phone, 'Sector': r.sector, 'Última Asistencia': r.last_attendance, 'Días Ausente': r.days_since })))
    }
    const wb = XLSX.utils.book_new(); XLSX.utils.book_append_sheet(wb, ws, "Reporte")
    let filename = 'Reporte_';
    if (selectedReport.value === 'attendance') filename += 'Asistencia_Diaria_';
    else if (selectedReport.value === 'activities') filename += 'Actividades_Top_';
    else if (selectedReport.value === 'risk') filename += 'Riesgo_Abandono_';
    else filename += 'Eventos_';
    XLSX.writeFile(wb, `${filename}${getLocalISODate()}.xlsx`)
}

const exportToPDF = () => {
    const doc = new jsPDF()
    let title = "Reporte - Centro Juvenil Las Mañanitas", head = [], bodyData = [], filename = 'Reporte_';
    if (selectedReport.value === 'attendance') {
        title = "Reporte de Asistencia Diaria"
        head = [['Fecha', 'Hora', 'Usuario', 'Cédula', 'Actividad', 'Evento']]
        bodyData = attendanceRecords.value.map(r => [r.date, r.time, r.beneficiary_name, r.beneficiary_ci, r.activity_name, r.event_name])
        filename += 'Asistencia_Diaria_'
    } else if (selectedReport.value === 'activities') {
        title = "Reporte de Actividades más Visitadas"
        head = [['Actividad', 'Evento / Detalles', 'Asistentes Únicos']]
        bodyData = activityRecords.value.map(r => [r.activity_name, r.event_name, r.attendees])
        filename += 'Actividades_Top_'
    } else if (selectedReport.value === 'events') {
        title = "Reporte por Eventos"
        head = [['Evento', 'Actividad', 'Fecha', 'Asistentes']]
        bodyData = eventRecords.value.map(r => [r.event_name, r.activity_name, r.event_date, r.attendees])
        filename += 'Eventos_'
    } else if (selectedReport.value === 'risk') {
        title = "Reporte de Riesgo de Abandono (Churn Risk)"
        head = [['Nombre', 'Cédula', 'Sector', 'Última Asistencia', 'Días sin asistir']]
        bodyData = riskRecords.value.map(r => [r.name, r.ci, r.sector, r.last_attendance, r.days_since])
        filename += 'Riesgo_Abandono_'
    }
    doc.text(title, 14, 15)
    autoTable(doc, { head, body: bodyData, startY: 25, theme: 'grid', headStyles: { fillColor: [234, 88, 12] } })
    doc.save(`${filename}${getLocalISODate()}.pdf`)
}
</script>
