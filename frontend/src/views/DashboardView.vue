<template>
  <div class="min-h-screen bg-background transition-colors duration-200">
    <div class="max-w-[1400px] mx-auto p-6 md:p-8 space-y-8">

      <!-- Loading State -->
      <div v-if="loading" class="text-center p-12 text-muted-foreground">
          Cargando estadísticas...
      </div>

      <template v-else>
          <!-- Stats Grid -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6"
               v-motion
               :initial="{ opacity: 0, y: 20 }"
               :enter="{ opacity: 1, y: 0, transition: { duration: 500 } }">

            <!-- Card 1: Asistencias Hoy -->
            <Card class="hover:shadow-md transition-shadow">
              <CardContent class="flex items-center gap-4 p-6 relative overflow-hidden">
                <div class="w-12 h-12 bg-primary/10 text-primary rounded-xl flex items-center justify-center shrink-0 z-10">
                  <UserGroupIcon class="h-6 w-6" />
                </div>
                <div class="flex-1 min-w-0 z-10">
                  <p class="text-muted-foreground text-xs font-semibold uppercase tracking-wider">Asistencias Hoy</p>
                  <div class="flex items-end gap-3 mt-0.5">
                      <p class="text-3xl font-extrabold text-foreground"><AnimatedCounter :value="stats.attendances_today" /></p>
                      <Badge v-if="stats.attendances_trend !== undefined" :variant="stats.attendances_trend >= 0 ? 'default' : 'destructive'" class="mb-1 bg-emerald-500/10 text-emerald-600 hover:bg-emerald-500/20 shadow-none border-0" :class="{'bg-red-500/10 text-red-600 hover:bg-red-500/20': stats.attendances_trend < 0}">
                          <ArrowTrendingUpIcon v-if="stats.attendances_trend >= 0" class="w-3 h-3 mr-1 stroke-2" />
                          <ArrowTrendingDownIcon v-else class="w-3 h-3 mr-1 stroke-2" />
                          {{ Math.abs(stats.attendances_trend) }}%
                      </Badge>
                  </div>
                </div>
              </CardContent>
            </Card>

            <!-- Card 2: Usuarios Activos -->
            <Card class="hover:shadow-md transition-shadow">
              <CardContent class="flex items-center gap-4 p-6 relative overflow-hidden">
                <div class="w-12 h-12 bg-chart-2/10 text-chart-2 rounded-xl flex items-center justify-center shrink-0 z-10">
                  <UserPlusIcon class="h-6 w-6" />
                </div>
                <div class="flex-1 min-w-0 z-10">
                  <p class="text-muted-foreground text-xs font-semibold uppercase tracking-wider">Usuarios Activos (Mes)</p>
                  <div class="flex items-end gap-3 mt-0.5">
                      <p class="text-3xl font-extrabold text-foreground"><AnimatedCounter :value="stats.active_users" /></p>
                      <Badge v-if="stats.users_trend !== undefined" :variant="stats.users_trend >= 0 ? 'default' : 'destructive'" class="mb-1 bg-emerald-500/10 text-emerald-600 hover:bg-emerald-500/20 shadow-none border-0" :class="{'bg-red-500/10 text-red-600 hover:bg-red-500/20': stats.users_trend < 0}">
                          <ArrowTrendingUpIcon v-if="stats.users_trend >= 0" class="w-3 h-3 mr-1 stroke-2" />
                          <ArrowTrendingDownIcon v-else class="w-3 h-3 mr-1 stroke-2" />
                          {{ Math.abs(stats.users_trend) }}%
                      </Badge>
                  </div>
                </div>
              </CardContent>
            </Card>

            <!-- Card 3: Actividad Principal -->
            <Card class="hover:shadow-md transition-shadow">
              <CardContent class="flex items-center gap-4 p-6">
                <div class="w-12 h-12 bg-violet-500/10 text-violet-500 rounded-xl flex items-center justify-center shrink-0">
                  <PuzzlePieceIcon class="h-6 w-6" />
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-muted-foreground text-xs font-semibold uppercase tracking-wider">Actividad Principal</p>
                  <p class="text-2xl font-extrabold text-foreground mt-0.5">{{ stats.top_activity_name }}</p>
                </div>
              </CardContent>
            </Card>

          </div>

          <!-- Bottom Section: Chart and Top Users -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6"
               v-motion
               :initial="{ opacity: 0, y: 30 }"
               :enter="{ opacity: 1, y: 0, transition: { duration: 600, delay: 200 } }">
            
            <!-- Charts Area -->
            <Card>
              <CardHeader class="pb-2">
                <CardTitle class="text-xl font-extrabold">Asistencia Anual</CardTitle>
                <p class="text-sm text-muted-foreground mt-0.5">Tendencia mensual de asistencias registradas</p>
              </CardHeader>
              <CardContent class="pt-2">
                <apexchart type="bar" height="340" :options="chartOptions" :series="chartSeries"></apexchart>
              </CardContent>
            </Card>

            <!-- Top 5 Attendees Leaderboard -->
            <Card class="border-amber-200/50 dark:border-amber-500/20 shadow-amber-500/5 overflow-hidden relative">
              <div class="absolute inset-x-0 top-0 h-1 bg-gradient-to-r from-amber-400 via-yellow-500 to-amber-600"></div>
              <CardHeader class="pb-2">
                <div class="flex items-center justify-between">
                    <div>
                        <CardTitle class="text-xl font-extrabold flex items-center gap-2">
                            <TrophySolidIcon class="w-6 h-6 text-amber-500" /> Leaderboard Mensual
                        </CardTitle>
                        <p class="text-sm text-muted-foreground mt-0.5">Podio de los mayores asistentes del mes en curso</p>
                    </div>
                </div>
              </CardHeader>
              <CardContent>
                <div class="overflow-x-auto">
                  <table class="min-w-full divide-y divide-border">
                    <tbody class="divide-y divide-border">
                      <tr v-for="(user) in leaderboard" :key="user.id" class="hover:bg-muted/30 transition-colors group">
                        <td class="pr-2 py-4 whitespace-nowrap w-12 text-center font-bold">
                            <div v-if="user.rank === 1" class="flex justify-center" title="1er Lugar">
                                <TrophySolidIcon class="w-7 h-7 text-yellow-500 drop-shadow-md" />
                            </div>
                            <div v-else-if="user.rank === 2" class="flex justify-center" title="2do Lugar">
                                <StarSolidIcon class="w-7 h-7 text-slate-400 drop-shadow" />
                            </div>
                            <div v-else-if="user.rank === 3" class="flex justify-center" title="3er Lugar">
                                <StarSolidIcon class="w-7 h-7 text-amber-700 drop-shadow" />
                            </div>
                            <span v-else class="text-muted-foreground">{{ user.rank }}</span>
                        </td>
                        <td class="px-4 py-4 whitespace-nowrap">
                          <div class="flex items-center">
                            <span class="font-bold text-foreground text-base">{{ user.name }}</span>
                          </div>
                        </td>
                        <td class="px-4 py-4 whitespace-nowrap text-right">
                          <Badge variant="secondary" class="font-extrabold group-hover:bg-primary group-hover:text-primary-foreground transition-colors px-3">
                              {{ user.attendances }} asistencias
                          </Badge>
                        </td>
                      </tr>
                      <tr v-if="loadingLeaderboard">
                         <td colspan="3" class="px-4 py-12 text-center text-muted-foreground text-sm">Cargando podio...</td>
                      </tr>
                      <tr v-if="!loadingLeaderboard && leaderboard.length === 0">
                        <td colspan="3" class="px-4 py-12 text-center text-muted-foreground text-sm">
                          Aún no hay asistencias suficientes este mes.
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </CardContent>
            </Card>

          </div>
      </template>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '../plugins/axios'
import AnimatedCounter from '../components/AnimatedCounter.vue'
import { UserGroupIcon, UserPlusIcon, PuzzlePieceIcon, ArrowTrendingUpIcon, ArrowTrendingDownIcon } from '@heroicons/vue/24/outline'
import { TrophyIcon as TrophySolidIcon, StarIcon as StarSolidIcon } from '@heroicons/vue/24/solid'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

const loading = ref(true)
const loadingLeaderboard = ref(true)
const leaderboard = ref([])
const stats = ref({
    attendances_today: 0,
    attendances_trend: 0,
    active_users: 0,
    users_trend: 0,
    top_activity_name: 'N/A',
    chart_data: []
})

const chartOptions = ref({
    chart: { type: 'bar', toolbar: { show: false }, background: 'transparent', fontFamily: 'Inter, sans-serif' },
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: '55%',
        borderRadius: 4
      },
    },
    colors: ['#ea580c', '#6366f1', '#eab308'],
    stroke: { show: true, width: 2, colors: ['transparent'] },
    dataLabels: { enabled: false },
    xaxis: {
      categories: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
      labels: {
        style: {
          colors: Array(12).fill('#9ca3af'),
          fontSize: '12px',
          fontWeight: 600,
        },
        rotate: 0,
      },
      axisBorder: { show: false },
      axisTicks: { show: false },
    },
    yaxis: {
      labels: {
        style: { colors: ['#9ca3af'], fontSize: '12px' },
        formatter: val => Math.round(val),
      }
    },
    grid: { borderColor: '#e5e7eb', strokeDashArray: 4 },
    tooltip: {
      theme: 'light',
      y: { formatter: val => `${val} asistencias` },
      style: { fontSize: '13px' },
    },
    fill: { opacity: 1 }
})

const chartSeries = ref([{ name: 'Asistencias', data: [] }])

const fetchStats = async () => {
    try {
        const res = await apiClient.get('dashboard-stats/')
        stats.value = res.data
        if (res.data.chart_data) {
            chartSeries.value = res.data.chart_data
        }
    } catch (e) {
        console.error("Error fetching stats:", e)
    } finally {
        loading.value = false
    }
}

const fetchLeaderboard = async () => {
    try {
        const res = await apiClient.get('dashboard/leaderboard/')
        leaderboard.value = res.data
    } catch (e) {
        console.error("Error fetching leaderboard:", e)
    } finally {
        loadingLeaderboard.value = false
    }
}

onMounted(() => {
    fetchStats()
    fetchLeaderboard()
})
</script>
