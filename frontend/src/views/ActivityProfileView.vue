<template>
  <div class="min-h-screen bg-background transition-colors duration-200 pb-12">
    <div class="max-w-[1400px] mx-auto p-4 md:p-8 space-y-6">
      
      <div v-if="loading" class="flex flex-col items-center justify-center py-20 text-muted-foreground gap-4">
          <div class="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
          Cargando entorno de actividad...
      </div>

      <template v-else-if="profile">
        <!-- HEADER OVERLAY (Cover Style) -->
        <Card class="overflow-hidden border-0 shadow-lg relative rounded-3xl group">
            <div class="h-48 md:h-64 bg-slate-900 overflow-hidden relative">
                <img v-if="profile.image" :src="profile.image" alt="Cover" class="w-full h-full object-cover opacity-60 transition-transform duration-700 group-hover:scale-105" />
                <div v-else class="absolute inset-0 bg-gradient-to-r from-violet-600 to-indigo-600 opacity-90"></div>
                
                <input ref="imageInput" type="file" accept="image/*" class="hidden" @change="onImageSelected" />
                <Button @click="imageInput?.click()" variant="secondary" size="sm" class="absolute top-4 right-4 bg-white/20 hover:bg-white/40 text-white border-0 backdrop-blur-md">
                    <CameraIcon class="w-4 h-4 mr-2" /> {{ profile.image ? 'Cambiar Portada' : 'Añadir Portada' }}
                </Button>

                <div class="absolute inset-0 bg-gradient-to-t from-slate-900 via-slate-900/50 to-transparent"></div>
                
                <!-- Info Overlay -->
                <div class="absolute bottom-6 left-6 right-6 flex flex-col md:flex-row items-start md:items-end justify-between gap-4">
                    <div class="flex gap-6 items-end">
                        <div class="w-20 h-20 md:w-24 md:h-24 bg-card rounded-2xl shadow-xl flex items-center justify-center border-4 border-slate-900 shrink-0">
                            <PuzzlePieceIcon class="w-10 h-10 text-primary" />
                        </div>
                        <div>
                            <div class="flex items-center gap-3 mb-1">
                                <Badge :class="profile.category === 'PERMANENT' ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/50' : 'bg-primary/20 text-primary-200 border-primary/50'" class="text-xs uppercase tracking-wider backdrop-blur-md font-bold">
                                    {{ profile.category === 'PERMANENT' ? 'Permanente' : 'Eventual' }}
                                </Badge>
                                <Badge v-if="!profile.is_active" variant="destructive" class="text-xs uppercase tracking-wider">ARCHIVADA</Badge>
                                <Badge v-if="profile.category === 'EVENTUAL' && profile.deadline_date" variant="outline" class="text-xs text-white border-white/30 backdrop-blur-md">
                                   Límite: {{ profile.deadline_date }}
                                </Badge>
                            </div>
                            <h1 class="text-3xl md:text-4xl font-extrabold text-white tracking-tight drop-shadow-md">{{ profile.name }}</h1>
                        </div>
                    </div>
                </div>
            </div>
        </Card>

        <!-- RETURN BUTTON -->
        <router-link to="/activities" class="inline-flex items-center text-sm font-semibold text-muted-foreground hover:text-primary transition-colors py-2">
            <ArrowLeftIcon class="w-4 h-4 mr-1" /> Volver a Actividades principales
        </router-link>

        <!-- SHADCN TABS FOR MAIN CONTENT -->
        <div class="w-full mt-6">
            <Tabs defaultValue="summary" class="w-full">
                <!-- TABS HEADERS -->
                <TabsList class="w-full justify-start border-b rounded-none h-14 bg-transparent p-0 gap-6">
                    <TabsTrigger value="summary" class="data-[state=active]:border-primary data-[state=active]:bg-transparent data-[state=active]:shadow-none border-b-2 border-transparent rounded-none px-4 py-4 text-base font-semibold data-[state=active]:text-primary text-muted-foreground hover:text-foreground flex items-center gap-2">
                        <DocumentChartBarIcon class="w-5 h-5" /> Resumen
                    </TabsTrigger>
                    <TabsTrigger value="events" class="data-[state=active]:border-primary data-[state=active]:bg-transparent data-[state=active]:shadow-none border-b-2 border-transparent rounded-none px-4 py-4 text-base font-semibold data-[state=active]:text-primary text-muted-foreground hover:text-foreground flex items-center gap-2">
                        <CalendarDaysIcon class="w-5 h-5" /> Eventos
                    </TabsTrigger>
                    <TabsTrigger value="attendees" class="data-[state=active]:border-primary data-[state=active]:bg-transparent data-[state=active]:shadow-none border-b-2 border-transparent rounded-none px-4 py-4 text-base font-semibold data-[state=active]:text-primary text-muted-foreground hover:text-foreground flex items-center gap-2">
                        <UserGroupIcon class="w-5 h-5" /> Participantes
                    </TabsTrigger>
                </TabsList>

                <!-- TAB 1: SUMMARY -->
                <TabsContent value="summary" class="mt-8 space-y-6" v-motion :initial="{ opacity: 0, y: 10 }" :enter="{ opacity: 1, y: 0 }">
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <!-- Left metrics -->
                        <div class="col-span-1 space-y-6">
                            <!-- Quick Stats -->
                            <Card class="bg-gradient-to-br from-primary to-primary/90 text-primary-foreground border-0 shadow-lg">
                                <CardContent class="p-6">
                                    <div class="flex justify-between items-center mb-4">
                                        <h3 class="font-bold text-primary-foreground/80 uppercase tracking-widest text-xs">Total Histórico</h3>
                                        <div class="p-2 bg-white/20 shadow-inner rounded-xl"><UserIcon class="w-5 h-5 text-white" /></div>
                                    </div>
                                    <p class="text-5xl font-extrabold tracking-tighter">{{ profile.total_attendance }}</p>
                                    <p class="text-sm text-primary-foreground/80 mt-2 font-medium">Asistencias verificadas</p>
                                </CardContent>
                            </Card>

                            <Card class="shadow-sm">
                                <CardHeader>
                                    <CardTitle class="text-[17px] font-bold">Descripción</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <p class="text-muted-foreground text-sm leading-relaxed">{{ profile.description || 'Sin descripción disponible para esta actividad.' }}</p>
                                    <!-- A potential edit button here later -->
                                </CardContent>
                            </Card>
                        </div>
                        
                        <!-- Right Chart Area -->
                        <div class="col-span-1 md:col-span-2">
                           <Card class="h-full shadow-sm">
                                <CardHeader class="pb-2">
                                  <CardTitle class="text-lg font-extrabold text-foreground">Tráfico de Asistencia (Últimos 30 días)</CardTitle>
                                  <p class="text-sm text-muted-foreground mt-0.5">Comportamiento interactivo diario exclusivo de {{ profile.name }}.</p>
                                </CardHeader>
                                <CardContent class="pt-4 h-[320px]">
                                  <div v-if="chartLoading" class="w-full h-full flex items-center justify-center text-muted-foreground">Analizando tráfico...</div>
                                  <apexchart v-else type="line" height="100%" :options="chartOptions" :series="chartSeries"></apexchart>
                                </CardContent>
                            </Card>
                        </div>
                    </div>
                </TabsContent>

                <!-- TAB 2: EVENTS -->
                <TabsContent value="events" class="mt-8 space-y-6" v-motion :initial="{ opacity: 0, y: 10 }" :enter="{ opacity: 1, y: 0 }">
                    <Card class="shadow-sm p-6 border-0 shadow-md">
                        <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8">
                            <div>
                                <h3 class="text-xl font-extrabold">Gestor de Eventos</h3>
                                <p class="text-sm text-muted-foreground mt-1">Crea, edita o busca eventos históricos correspondientes a {{ profile.name }}.</p>
                            </div>
                            <div class="flex gap-3 w-full md:w-auto">
                                <div class="relative w-full md:w-64">
                                     <MagnifyingGlassIcon class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                                     <Input v-model="eventSearch" type="text" placeholder="Buscar evento..." class="pl-9 h-10 bg-muted/50 border-0" />
                                </div>
                                <Button @click="openEventForm" class="bg-primary shrink-0"><PlusIcon class="w-4 h-4 mr-1 stroke-2" /> Crear Evento</Button>
                            </div>
                        </div>

                        <div v-if="filteredEvents.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                            <Card v-for="ev in filteredEvents" :key="ev.id" class="flex flex-col justify-between hover:shadow-lg transition-all relative group border hover:border-primary/50 bg-card">
                                <Button @click="confirmDeleteEvent(ev)" variant="ghost" size="icon" class="absolute top-3 right-3 text-muted-foreground hover:bg-destructive/10 hover:text-destructive opacity-0 group-hover:opacity-100 transition-all h-8 w-8 z-10 rounded-full">
                                    <TrashIcon class="w-4 h-4" />
                                </Button>
                                <CardContent class="p-5 pt-6">
                                    <div class="w-10 h-10 bg-muted rounded-full flex items-center justify-center mb-4 text-muted-foreground">
                                        <CalendarIcon class="w-5 h-5 group-hover:text-primary transition-colors" />
                                    </div>
                                    <h4 class="font-extrabold text-foreground text-lg mb-1 pr-8 leading-tight">{{ ev.name }}</h4>
                                    <p class="text-sm font-medium text-muted-foreground">{{ ev.date || 'Evento general sin fecha' }}</p>
                                </CardContent>
                                <div class="mx-5 mb-5 flex items-center justify-between border-t pt-4 mt-2">
                                    <span class="text-xs text-muted-foreground font-semibold uppercase tracking-wide">Asistencias</span>
                                    <Badge class="bg-primary/10 text-primary border-primary/20 px-3 py-1 font-extrabold text-sm shadow-none">
                                        {{ ev.attendance_count }}
                                    </Badge>
                                </div>
                            </Card>
                        </div>
                        <div v-else class="text-center py-20 bg-muted/20 rounded-2xl border border-dashed text-muted-foreground flex flex-col items-center gap-3">
                            <FolderOpenIcon class="w-12 h-12 text-muted-foreground/40" />
                            <p class="text-base font-medium">No se encontraron eventos {{ eventSearch ? `llamados "${eventSearch}"` : 'registrados.' }}</p>
                        </div>
                    </Card>
                </TabsContent>

                <!-- TAB 3: ATTENDEES (PARTICIPANTES MÁXIMOS) -->
                <TabsContent value="attendees" class="mt-8 space-y-6" v-motion :initial="{ opacity: 0, y: 10 }" :enter="{ opacity: 1, y: 0 }">
                     <Card class="shadow-sm border-0 shadow-md">
                        <div class="px-6 py-6 border-b flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-muted/10">
                            <div>
                                <h3 class="text-xl font-extrabold flex items-center gap-2">
                                    Nómina Global de Participantes
                                    <Badge class="scale-90 bg-black text-white" variant="secondary">{{ attendees.length }}</Badge>
                                </h3>
                                <p class="text-sm text-muted-foreground mt-1">Beneficiarios únicos que han cruzado asistencia en {{ profile.name }}</p>
                            </div>
                            <div class="flex gap-2 w-full md:w-auto">
                                <Button @click="exportToExcel" :disabled="!attendees.length" variant="outline" class="flex-1 md:flex-none text-emerald-600 border-emerald-200 hover:bg-emerald-50">
                                    <TableCellsIcon class="w-4 h-4 mr-2" /> Excel
                                </Button>
                                <Button @click="exportToPDF" :disabled="!attendees.length" variant="outline" class="flex-1 md:flex-none text-destructive border-red-200 hover:bg-red-50">
                                    <DocumentTextIcon class="w-4 h-4 mr-2" /> PDF
                                </Button>
                            </div>
                        </div>

                        <div class="overflow-x-auto">
                           <div v-if="attendeesLoading" class="py-12 text-center text-muted-foreground">Calculando asistentes...</div>
                           <table v-else class="min-w-full divide-y divide-border">
                               <thead class="bg-muted/50">
                                   <tr>
                                       <th class="px-6 py-4 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">#</th>
                                       <th class="px-6 py-4 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Nombre Completo</th>
                                       <th class="px-6 py-4 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Cédula</th>
                                       <th class="px-6 py-4 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Última Visita</th>
                                       <th class="px-6 py-4 text-center text-xs font-bold text-muted-foreground uppercase tracking-wider">Visitas Totales a {{ profile.name }}</th>
                                   </tr>
                               </thead>
                               <tbody class="divide-y divide-border">
                                   <tr v-for="(b, i) in attendees" :key="b.id" class="hover:bg-muted/30 transition-colors">
                                       <td class="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">{{ i + 1 }}</td>
                                       <td class="px-6 py-4 whitespace-nowrap text-sm font-extrabold text-foreground">{{ b.name }}</td>
                                       <td class="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">{{ b.ci }}</td>
                                       <td class="px-6 py-4 whitespace-nowrap text-sm font-semibold text-primary">{{ b.last_visit }}</td>
                                       <td class="px-6 py-4 whitespace-nowrap text-center">
                                           <Badge variant="secondary" class="font-extrabold bg-primary/10 text-primary border-0 px-3">{{ b.total_visits }}</Badge>
                                       </td>
                                   </tr>
                                   <tr v-if="attendees.length === 0">
                                      <td colspan="5" class="px-6 py-16 text-center text-muted-foreground font-medium text-lg border-dashed">
                                          Totalmente vacío. Nadie ha participado todavía.
                                      </td>
                                   </tr>
                               </tbody>
                           </table>
                        </div>
                     </Card>
                </TabsContent>
            </Tabs>
        </div>

      </template>
    </div>

    <!-- Event Form Modal -->
    <Dialog :open="showEventForm" @update:open="showEventForm = $event">
      <DialogHeader>
        <DialogTitle>Crear Evento en {{ profile?.name }}</DialogTitle>
      </DialogHeader>
      <form @submit.prevent="saveEvent" class="space-y-4">
          <div>
             <Label class="mb-1">Nombre del Evento</Label>
             <Input v-model="eventForm.name" required type="text" placeholder="Ej: Torneo Sabatino, Clase Inaugural..." autofocus />
          </div>
          <div>
             <Label class="mb-1">Fecha (Opcional)</Label>
             <Input v-model="eventForm.date" type="date" />
          </div>
          <div class="flex justify-end gap-3 mt-8">
              <Button type="button" variant="ghost" @click="showEventForm = false">Cancelar</Button>
              <Button type="submit" class="bg-primary">Guardar Evento</Button>
          </div>
      </form>
    </Dialog>

    <!-- Delete Confirmation Dialog -->
    <Dialog :open="showDeleteConfirm" @update:open="showDeleteConfirm = $event">
      <DialogHeader>
        <DialogTitle>Eliminar Evento</DialogTitle>
      </DialogHeader>
      <div class="space-y-4">
          <p class="text-sm text-muted-foreground leading-relaxed">
            ¿Estás absolutamente seguro de querer eliminar el evento <span class="font-extrabold text-foreground px-1 bg-muted rounded">"{{ targetEvent?.name }}"</span>?
          </p>
          <div class="bg-destructive/10 border-l-4 border-destructive p-3 rounded">
             <p class="text-xs text-destructive font-bold uppercase tracking-wider mb-1">Advertencia Crítica</p>
             <p class="text-sm text-destructive/90">Esta acción purgará {{ targetEvent?.attendance_count }} registro(s) de asistencia históricos asociados a este evento. Las cifras estadísticas cuadradas caerán.</p>
          </div>
          <div class="flex justify-end gap-3 mt-8 pt-4 border-t">
              <Button type="button" variant="outline" @click="showDeleteConfirm = false">Cancelar</Button>
              <Button variant="destructive" @click="executeEventDeletion" :disabled="deleteLoading">
                  {{ deleteLoading ? 'Purgando...' : 'Sí, eliminar permanentemente' }}
              </Button>
          </div>
      </div>
    </Dialog>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import apiClient from '../plugins/axios'
import * as XLSX from 'xlsx'
import { jsPDF } from 'jspdf'
import autoTable from 'jspdf-autotable'
import { ArrowLeftIcon, CameraIcon, TrashIcon, CalendarIcon, FolderOpenIcon, MagnifyingGlassIcon, PlusIcon, TableCellsIcon, DocumentTextIcon, DocumentChartBarIcon, CalendarDaysIcon, UserGroupIcon } from '@heroicons/vue/24/outline'
import { PuzzlePieceIcon, UserIcon } from '@heroicons/vue/24/solid'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Dialog, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs'

const router = useRouter()
const route = useRoute()
const loading = ref(true)
const profile = ref(null)
const imageInput = ref(null)
const activityId = route.params.id

// Events logic
const showEventForm = ref(false)
const eventForm = ref({ activity: activityId, name: '-default-', date: '' })
const eventSearch = ref('')

// Analytics logic
const chartLoading = ref(true)
const chartSeries = ref([])
const chartOptions = ref({
    chart: { type: 'area', toolbar: { show: false }, background: 'transparent', fontFamily: 'Inter, sans-serif' },
    colors: ['#6366f1'],
    stroke: { curve: 'smooth', width: 3 },
    markers: { size: 4, strokeColors: '#fff', hover: { size: 7 } },
    dataLabels: { enabled: false },
    xaxis: {
      categories: [],
      labels: { style: { colors: '#9ca3af', fontSize: '11px', fontWeight: 600 }, hideOverlappingLabels: true },
      axisBorder: { show: false }, axisTicks: { show: false }
    },
    yaxis: {
      labels: { style: { colors: '#9ca3af', fontSize: '11px' }, formatter: val => Math.round(val) }
    },
    grid: { borderColor: '#f3f4f6', strokeDashArray: 4 },
    fill: {
        type: 'gradient',
        gradient: { shadeIntensity: 1, opacityFrom: 0.3, opacityTo: 0.05, stops: [0, 90, 100] }
    }
})

// Attendees logic
const attendees = ref([])
const attendeesLoading = ref(true)

const fetchProfile = async () => {
    try {
        const res = await apiClient.get(`reports/activity-profile/${activityId}/`)
        profile.value = res.data
    } catch (e) {
        console.error("Error fetching activity profile", e)
        alert("Actividad no encontrada")
        router.push('/activities')
    } finally { loading.value = false }
}

const fetchChartData = async () => {
    chartLoading.value = true
    try {
        const res = await apiClient.get(`reports/activity-chart/${activityId}/`)
        chartOptions.value = { ...chartOptions.value, xaxis: { ...chartOptions.value.xaxis, categories: res.data.categories } }
        chartSeries.value = res.data.series
    } catch (e) { console.error("Error chart:", e) } finally { chartLoading.value = false }
}

const fetchAttendees = async () => {
    attendeesLoading.value = true
    try {
        const res = await apiClient.get(`reports/activity-attendees/${activityId}/`)
        attendees.value = res.data
    } catch (e) { console.error("Error attendees:", e) } finally { attendeesLoading.value = false }
}

// EVENTS FUNC
const filteredEvents = computed(() => {
    if(!profile.value) return []
    let evts = profile.value.events
    if(eventSearch.value) {
        const query = eventSearch.value.toLowerCase()
        evts = evts.filter(e => e.name.toLowerCase().includes(query) || (e.date && e.date.includes(query)))
    }
    return evts.sort((a,b) => new Date(b.date || '2000-01-01') - new Date(a.date || '2000-01-01'))
})

const openEventForm = () => {
    eventForm.value.name = ''; eventForm.value.date = ''
    showEventForm.value = true
}

const saveEvent = async () => {
    try {
        const payload = { ...eventForm.value }
        if (!payload.date) delete payload.date
        await apiClient.post('events/', payload)
        showEventForm.value = false
        fetchProfile()
    } catch (e) { alert("Error al guardar el evento"); console.error(e) }
}

// DELETE EVENT DIALOG
const showDeleteConfirm = ref(false)
const deleteLoading = ref(false)
const targetEvent = ref(null)

const confirmDeleteEvent = (ev) => {
    targetEvent.value = ev
    showDeleteConfirm.value = true
}

const executeEventDeletion = async () => {
    deleteLoading.value = true
    try { 
        await apiClient.delete(`events/${targetEvent.value.id}/`)
        showDeleteConfirm.value = false
        targetEvent.value = null
        fetchProfile()
        fetchChartData() // Because attendance dropped!
        fetchAttendees() // Updating total unique visits
    } catch (e) { 
        console.error(e); alert("Error al eliminar el evento.") 
    } finally { deleteLoading.value = false }
}

// COVER IMAGE
const onImageSelected = (e) => {
    const file = e.target.files[0]
    if (!file) return
    const reader = new FileReader()
    reader.onload = async (evt) => {
        try {
            await apiClient.patch(`activities/${activityId}/`, { image: evt.target.result })
            profile.value.image = evt.target.result
        } catch (err) { alert('Error al guardar la imagen.'); console.error(err) }
    }
    reader.readAsDataURL(file)
}

// EXPORT Logic
const getLocalISODate = (date = new Date()) => {
    const y = date.getFullYear(); const m = String(date.getMonth() + 1).padStart(2, '0'); const d = String(date.getDate()).padStart(2, '0');
    return `${y}-${m}-${d}`;
}

const exportToExcel = () => {
    const ws = XLSX.utils.json_to_sheet(attendees.value.map((a, i) => ({
        '#': i + 1, 'Nombre Completo': a.name, 'Cédula': a.ci, 'Última Visita': a.last_visit, 'Total Visitas': a.total_visits
    })))
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, ws, "Nómina Participantes")
    XLSX.writeFile(wb, `Participantes_${profile.value.name.replace(/ /g, '_')}_${getLocalISODate()}.xlsx`)
}

const exportToPDF = () => {
    const doc = new jsPDF()
    doc.text(`Nómina Histórica: ${profile.value.name}`, 14, 15)
    doc.setFontSize(10); doc.setTextColor(100)
    doc.text(`Total de Participantes Únicos: ${attendees.value.length}`, 14, 22)
    
    autoTable(doc, {
        head: [['#', 'Nombre', 'Cédula', 'Última Visita', 'Visitas Totales']],
        body: attendees.value.map((a, i) => [i + 1, a.name, a.ci, a.last_visit, a.total_visits]),
        startY: 27, theme: 'grid', headStyles: { fillColor: [79, 70, 229] } // Indigo Color
    })
    doc.save(`Participantes_${profile.value.name.replace(/ /g, '_')}_${getLocalISODate()}.pdf`)
}

onMounted(() => { 
    fetchProfile()
    fetchChartData()
    fetchAttendees()
})
</script>
