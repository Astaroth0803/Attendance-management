<template>
  <div class="min-h-screen bg-background transition-colors duration-200 pb-12">
    <div class="max-w-[1400px] mx-auto p-4 md:p-8 space-y-6">

      <div v-if="loading" class="flex flex-col items-center justify-center py-20 text-muted-foreground gap-4">
          <div class="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
          Cargando entorno de cliente...
      </div>

      <template v-else-if="profile">
        <!-- HEADER OVERLAY (Cover Style) -->
        <Card class="overflow-hidden border-0 shadow-lg relative rounded-3xl group">
            <div class="h-48 md:h-56 bg-slate-900 overflow-hidden relative">
                <div class="absolute inset-0 bg-gradient-to-r from-blue-600 to-indigo-700 opacity-90"></div>
                <div class="absolute inset-0 bg-gradient-to-t from-slate-900 via-slate-900/50 to-transparent"></div>
                
                <!-- Info Overlay -->
                <div class="absolute bottom-6 left-6 right-6 flex flex-col md:flex-row items-start md:items-end justify-between gap-4">
                    <div class="flex gap-6 items-end">
                        <div class="w-20 h-20 md:w-24 md:h-24 rounded-full bg-card shadow-xl flex items-center justify-center text-4xl font-extrabold text-primary uppercase tracking-wider border-4 border-slate-900 shrink-0">
                            {{ initials }}
                        </div>
                        <div>
                            <div class="flex items-center gap-3 mb-1">
                                <Badge v-if="profile.is_active" class="bg-emerald-500/20 text-emerald-300 border-emerald-500/50 text-xs uppercase tracking-wider backdrop-blur-md font-bold">
                                    Usuario Activo
                                </Badge>
                                <Badge v-else variant="destructive" class="text-xs uppercase tracking-wider font-bold">INACO</Badge>
                                <Badge variant="outline" class="text-xs text-white border-white/30 backdrop-blur-md flex items-center gap-1">
                                   <TrophyIcon class="w-3 h-3 text-amber-400" />
                                   {{ profile.stats.total_attendance }} Asistencias
                                </Badge>
                            </div>
                            <h1 class="text-3xl md:text-4xl font-extrabold text-white tracking-tight drop-shadow-md">
                                {{ profile.first_name }} {{ profile.last_name }}
                            </h1>
                            <p class="text-white/70 text-sm mt-1 flex items-center gap-2">
                                <IdentificationIcon class="w-4 h-4" /> {{ profile.ci || 'Sin Cédula Registrada' }}
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </Card>

        <!-- RETURN BUTTON -->
        <router-link to="/beneficiaries" class="inline-flex items-center text-sm font-semibold text-muted-foreground hover:text-primary transition-colors py-2">
            <ArrowLeftIcon class="w-4 h-4 mr-1" /> Volver a Nómina de Clientes
        </router-link>

        <!-- SHADCN TABS FOR MAIN CONTENT -->
        <div class="w-full mt-6">
            <Tabs defaultValue="summary" class="w-full">
                <!-- TABS HEADERS -->
                <TabsList class="w-full justify-start border-b rounded-none h-14 bg-transparent p-0 gap-6">
                    <TabsTrigger value="summary" class="data-[state=active]:border-primary data-[state=active]:bg-transparent data-[state=active]:shadow-none border-b-2 border-transparent rounded-none px-4 py-4 text-base font-semibold data-[state=active]:text-primary text-muted-foreground hover:text-foreground flex items-center gap-2">
                        <UserIcon class="w-5 h-5" /> Resumen General
                    </TabsTrigger>
                    <TabsTrigger value="analytics" class="data-[state=active]:border-primary data-[state=active]:bg-transparent data-[state=active]:shadow-none border-b-2 border-transparent rounded-none px-4 py-4 text-base font-semibold data-[state=active]:text-primary text-muted-foreground hover:text-foreground flex items-center gap-2">
                        <ChartBarIcon class="w-5 h-5" /> Analítica Personal
                    </TabsTrigger>
                    <TabsTrigger value="history" class="data-[state=active]:border-primary data-[state=active]:bg-transparent data-[state=active]:shadow-none border-b-2 border-transparent rounded-none px-4 py-4 text-base font-semibold data-[state=active]:text-primary text-muted-foreground hover:text-foreground flex items-center gap-2">
                        <QueueListIcon class="w-5 h-5" /> Historial Completo
                    </TabsTrigger>
                </TabsList>

                <!-- TAB 1: SUMMARY -->
                <TabsContent value="summary" class="mt-8 space-y-6" v-motion :initial="{ opacity: 0, y: 10 }" :enter="{ opacity: 1, y: 0 }">
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <!-- Left Column: Demographics -->
                        <div class="col-span-1 space-y-6">
                             <Card class="shadow-sm border-0 shadow-md">
                                 <CardHeader>
                                     <CardTitle class="text-[17px] font-bold">Datos Demográficos</CardTitle>
                                 </CardHeader>
                                 <CardContent class="space-y-4">
                                     <div class="flex items-start gap-4">
                                         <MapPinIcon class="w-5 h-5 text-rose-500 shrink-0" />
                                         <div>
                                             <span class="block text-xs text-muted-foreground font-medium uppercase tracking-wider mb-0.5">Sector</span>
                                             <span class="font-bold text-foreground text-sm">{{ profile.sector || 'No especificado' }}</span>
                                         </div>
                                     </div>
                                     <div class="flex items-start gap-4 mt-4">
                                         <CalendarDaysIcon class="w-5 h-5 text-blue-500 shrink-0" />
                                         <div>
                                             <span class="block text-xs text-muted-foreground font-medium uppercase tracking-wider mb-0.5">Nacimiento</span>
                                             <span class="font-bold text-foreground text-sm">{{ profile.dob || 'No especificado' }}</span>
                                         </div>
                                     </div>
                                     <div class="flex items-start gap-4 mt-4">
                                         <UserGroupIcon class="w-5 h-5 text-indigo-500 shrink-0" />
                                         <div>
                                             <span class="block text-xs text-muted-foreground font-medium uppercase tracking-wider mb-0.5">Sexo</span>
                                             <span class="font-bold text-foreground text-sm">{{ profile.sex }}</span>
                                         </div>
                                     </div>
                                 </CardContent>
                             </Card>
                        </div>
                        
                        <!-- Right Column: Frequent Activities & Recent History -->
                        <div class="col-span-1 md:col-span-2 space-y-6">
                             <!-- Top Activities Breakdown -->
                             <Card class="shadow-sm border-0 shadow-md">
                                 <CardHeader class="flex flex-row items-center justify-between pb-4">
                                     <CardTitle class="text-lg font-extrabold flex items-center gap-2">
                                         <SparklesIcon class="w-5 h-5 text-amber-500" />
                                         Intereses Frecuentes
                                     </CardTitle>
                                 </CardHeader>
                                 <CardContent>
                                     <div v-if="profile.stats.top_activities.length > 0" class="space-y-3">
                                         <div v-for="(act, idx) in profile.stats.top_activities" :key="idx" class="flex items-center bg-muted/40 hover:bg-muted/70 transition-colors rounded-xl p-4 border">
                                             <div class="w-10 h-10 rounded-full bg-primary/10 text-primary flex items-center justify-center font-extrabold mr-4 shrink-0 shadow-sm border border-primary/20">
                                                 #{{ idx + 1 }}
                                             </div>
                                             <div class="flex-1">
                                                 <h4 class="font-extrabold text-foreground">{{ act.activity_name }}</h4>
                                                 <p class="text-xs font-semibold text-muted-foreground mt-0.5">{{ act.event_name }}</p>
                                             </div>
                                             <Badge class="ml-4 shrink-0 bg-emerald-500 text-white border-0 px-3 py-1 text-sm font-extrabold shadow-sm">
                                                {{ act.count }} <span class="uppercase tracking-wide ml-1 text-xs opacity-90">visitas</span>
                                             </Badge>
                                         </div>
                                     </div>
                                     <div v-else class="text-center py-8 text-muted-foreground flex flex-col items-center gap-2">
                                         <ExclamationCircleIcon class="w-10 h-10 text-muted-foreground/40" />
                                         Este cliente no reporta visitas.
                                     </div>
                                 </CardContent>
                             </Card>
                        </div>
                    </div>
                </TabsContent>

                <!-- TAB 2: ANALYTICS -->
                <TabsContent value="analytics" class="mt-8 space-y-6" v-motion :initial="{ opacity: 0, y: 10 }" :enter="{ opacity: 1, y: 0 }">
                    <Card class="shadow-sm border-0 shadow-md">
                        <CardHeader class="pb-2">
                          <CardTitle class="text-xl font-extrabold text-foreground flex items-center gap-2">
                              <ChartBarIcon class="w-6 h-6 text-primary" />
                              Retención Mensual
                          </CardTitle>
                          <p class="text-sm text-muted-foreground mt-0.5">Volumen histórico de asistencias consolidado por mes (Últimos 6 meses).</p>
                        </CardHeader>
                        <CardContent class="pt-6 h-[380px]">
                          <div v-if="chartLoading" class="w-full h-full flex items-center justify-center text-muted-foreground">Analizando data...</div>
                          <apexchart v-else type="bar" height="100%" :options="chartOptions" :series="chartSeries"></apexchart>
                        </CardContent>
                    </Card>
                </TabsContent>

                <!-- TAB 3: HISTORY (DATA TABLE) -->
                <TabsContent value="history" class="mt-8 space-y-6" v-motion :initial="{ opacity: 0, y: 10 }" :enter="{ opacity: 1, y: 0 }">
                     <Card class="shadow-sm border-0 shadow-md">
                        <div class="px-6 py-6 border-b flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-muted/10">
                            <div>
                                <h3 class="text-xl font-extrabold flex items-center gap-2">
                                    Tabla Histórica de Visitas
                                </h3>
                                <p class="text-sm text-muted-foreground mt-1">
                                    Auditoría detallada de todos los movimientos y escaneos de asistencia de {{ profile.first_name }}.
                                </p>
                            </div>
                            <div class="flex gap-2 w-full md:w-auto mt-4 md:mt-0">
                                <div class="relative w-full md:w-64 mr-2">
                                     <MagnifyingGlassIcon class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                                     <Input v-model="historySearch" type="text" placeholder="Filtrar eventos..." class="pl-9 h-10 bg-white dark:bg-card border-muted-foreground/20" />
                                </div>
                                <Button @click="exportToExcel" :disabled="!attendeesHistory.length" variant="outline" class="flex-1 md:flex-none text-emerald-600 border-emerald-200 hover:bg-emerald-50">
                                    <TableCellsIcon class="w-4 h-4 mr-2" /> Excel
                                </Button>
                                <Button @click="exportToPDF" :disabled="!attendeesHistory.length" variant="outline" class="flex-1 md:flex-none text-destructive border-red-200 hover:bg-red-50">
                                    <DocumentTextIcon class="w-4 h-4 mr-2" /> PDF
                                </Button>
                            </div>
                        </div>

                        <div class="overflow-x-auto">
                           <div v-if="historyLoading" class="py-12 text-center text-muted-foreground">Cargando registros...</div>
                           <table v-else class="min-w-full divide-y divide-border">
                               <thead class="bg-muted/50">
                                   <tr>
                                       <th class="px-6 py-4 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Fecha / Hora</th>
                                       <th class="px-6 py-4 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Actividad Principal</th>
                                       <th class="px-6 py-4 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Detalle del Evento</th>
                                       <th class="px-6 py-4 text-center text-xs font-bold text-muted-foreground uppercase tracking-wider">Estatus</th>
                                   </tr>
                               </thead>
                               <tbody class="divide-y divide-border">
                                   <tr v-for="(b, i) in filteredHistory" :key="b.id" class="hover:bg-muted/30 transition-colors">
                                       <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-foreground">
                                           <div class="flex items-center gap-2">
                                               <CalendarDaysIcon class="w-4 h-4 text-muted-foreground" />
                                               {{ b.date }}
                                           </div>
                                       </td>
                                       <td class="px-6 py-4 whitespace-nowrap text-sm font-semibold text-primary">{{ b.activity_name }}</td>
                                       <td class="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">{{ b.event_name }}</td>
                                       <td class="px-6 py-4 whitespace-nowrap text-center">
                                           <Badge variant="secondary" class="font-bold bg-emerald-500/10 text-emerald-600 border-0 px-3">Confirmada</Badge>
                                       </td>
                                   </tr>
                                   <tr v-if="filteredHistory.length === 0">
                                      <td colspan="4" class="px-6 py-16 text-center text-muted-foreground font-medium text-lg border-dashed">
                                          Totalmente vacío. No hay historial {{ historySearch ? 'con ese filtro.' : 'registrado.' }}
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
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import apiClient from '../plugins/axios'
import * as XLSX from 'xlsx'
import { jsPDF } from 'jspdf'
import autoTable from 'jspdf-autotable'

// HEROICONS EXCLUSIVAMENTE
import { 
    ArrowLeftIcon, MapPinIcon, CalendarDaysIcon, ChartBarIcon, QueueListIcon, UserIcon, 
    MagnifyingGlassIcon, TableCellsIcon, DocumentTextIcon, IdentificationIcon
} from '@heroicons/vue/24/outline'
import { TrophyIcon, SparklesIcon, UserGroupIcon, ExclamationCircleIcon } from '@heroicons/vue/24/solid'

import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs'

const router = useRouter()
const route = useRoute()
const loading = ref(true)
const profile = ref(null)
const userId = route.params.id

// CHART LOGIC
const chartLoading = ref(true)
const chartSeries = ref([])
const chartOptions = ref({
    chart: { type: 'bar', toolbar: { show: false }, background: 'transparent', fontFamily: 'Inter, sans-serif' },
    plotOptions: {
      bar: { horizontal: false, columnWidth: '55%', borderRadius: 4 },
    },
    colors: ['#3b82f6'],
    stroke: { show: true, width: 2, colors: ['transparent'] },
    dataLabels: { enabled: false },
    xaxis: {
      categories: [],
      labels: { style: { colors: '#9ca3af', fontSize: '11px', fontWeight: 600 } },
      axisBorder: { show: false }, axisTicks: { show: false }
    },
    yaxis: {
      labels: { style: { colors: '#9ca3af', fontSize: '11px' }, formatter: val => Math.round(val) }
    },
    grid: { borderColor: '#f3f4f6', strokeDashArray: 4 },
    fill: { opacity: 1 }
})

// HISTORY LOGIC
const historyLoading = ref(true)
const attendeesHistory = ref([])
const historySearch = ref('')

const initials = computed(() => {
    if(!profile.value) return '';
    return (profile.value.first_name.charAt(0) + profile.value.last_name.charAt(0)).toUpperCase();
})

const filteredHistory = computed(() => {
    if (!historySearch.value) return attendeesHistory.value
    const q = historySearch.value.toLowerCase()
    return attendeesHistory.value.filter(h => 
        h.activity_name?.toLowerCase().includes(q) || h.event_name?.toLowerCase().includes(q)
    )
})

const fetchProfile = async () => {
    try {
        const res = await apiClient.get(`reports/beneficiary-profile/${userId}/`)
        profile.value = res.data
    } catch (e) {
        console.error("Error fetching profile", e)
        alert("Cliente no encontrado")
        router.push('/beneficiaries')
    } finally { loading.value = false }
}

const fetchChart = async () => {
    chartLoading.value = true
    try {
        const res = await apiClient.get(`reports/beneficiary-chart/${userId}/`)
        chartOptions.value = { ...chartOptions.value, xaxis: { ...chartOptions.value.xaxis, categories: res.data.categories } }
        chartSeries.value = res.data.series
    } catch (e) { console.error("Error chart:", e) } finally { chartLoading.value = false }
}

const fetchHistory = async () => {
    historyLoading.value = true
    try {
        const res = await apiClient.get(`reports/beneficiary-attendances/${userId}/`)
        attendeesHistory.value = res.data
    } catch (e) { console.error("Error history:", e) } finally { historyLoading.value = false }
}

// EXPORT Logic
const getLocalISODate = (date = new Date()) => {
    const y = date.getFullYear(); const m = String(date.getMonth() + 1).padStart(2, '0'); const d = String(date.getDate()).padStart(2, '0');
    return `${y}-${m}-${d}`;
}

const exportToExcel = () => {
    const ws = XLSX.utils.json_to_sheet(filteredHistory.value.map(h => ({
        'Fecha': h.date, 'Actividad': h.activity_name, 'Evento / Detalle': h.event_name, 'Estado': 'Confirmada'
    })))
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, ws, "Historial Cliente")
    XLSX.writeFile(wb, `Historial_${profile.value.first_name}_${profile.value.last_name}_${getLocalISODate()}.xlsx`)
}

const exportToPDF = () => {
    const doc = new jsPDF()
    doc.text(`Auditoría de Asistencias - ${profile.value.first_name} ${profile.value.last_name}`, 14, 15)
    doc.setFontSize(10); doc.setTextColor(100)
    doc.text(`Total Visitas Históricas Exportadas: ${filteredHistory.value.length}`, 14, 22)
    
    autoTable(doc, {
        head: [['Fecha', 'Actividad', 'Evento / Fase', 'Estado']],
        body: filteredHistory.value.map(h => [h.date, h.activity_name, h.event_name, 'Confirmada']),
        startY: 27, theme: 'grid', headStyles: { fillColor: [59, 130, 246] } // Blue
    })
    doc.save(`Auditoria_${profile.value.first_name}_${profile.value.last_name}_${getLocalISODate()}.pdf`)
}

onMounted(() => { 
    fetchProfile()
    fetchChart()
    fetchHistory()
})
</script>
