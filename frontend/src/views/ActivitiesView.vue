<template>
  <div class="min-h-screen bg-background transition-colors duration-200">
    <div class="max-w-[1400px] mx-auto p-6 md:p-8 space-y-6">

     <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
       <h1 class="text-3xl font-bold text-foreground">Manejo de Actividades</h1>
       <div class="flex gap-3 items-center">
          <div class="relative w-full sm:w-56">
             <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
             <Input v-model="searchQuery" type="text" placeholder="Buscar actividad..." class="pl-9 h-9" />
          </div>
          <Button @click="showForm = true" class="bg-emerald-600 hover:bg-emerald-700">
            <Plus class="w-4 h-4 mr-1" /> Nueva Actividad
          </Button>
       </div>
     </div>

     <!-- Toggle Tabs -->
     <div class="flex border-b border-border mb-6">
        <button @click="activeTab = 'ACTIVE'" 
                class="px-6 py-3 font-semibold text-sm transition-colors border-b-2"
                :class="activeTab === 'ACTIVE' ? 'border-primary text-primary' : 'border-transparent text-muted-foreground hover:text-foreground hover:border-border'">
            Activas
        </button>
        <button @click="activeTab = 'ARCHIVED'" 
                class="px-6 py-3 font-semibold text-sm transition-colors border-b-2"
                :class="activeTab === 'ARCHIVED' ? 'border-destructive text-destructive' : 'border-transparent text-muted-foreground hover:text-foreground hover:border-border'">
            Archivadas
        </button>
     </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-6">
       <Card v-for="act in displayedActivities" :key="act.id" 
            @click="goToProfile(act.id)"
            class="hover:shadow-md hover:border-primary/30 cursor-pointer transition-all group flex flex-col justify-between h-full">
         
         <CardContent class="p-6">
             <div class="flex justify-between items-start mb-4">
                 <div class="w-12 h-12 bg-muted rounded-xl flex items-center justify-center text-muted-foreground group-hover:bg-primary/10 group-hover:text-primary transition-colors">
                   <LayoutGrid class="w-6 h-6" />
                 </div>
                 <div class="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                     <Button v-if="activeTab === 'ACTIVE'" variant="ghost" size="icon" @click.stop="confirmArchive(act)" title="Archivar" class="h-8 w-8 text-muted-foreground hover:text-primary">
                       <Archive class="w-4 h-4" />
                     </Button>
                     <Button v-else variant="ghost" size="icon" @click.stop="openReactivate(act, $event)" title="Reactivar" class="h-8 w-8 text-muted-foreground hover:text-emerald-500">
                       <Check class="w-4 h-4" />
                     </Button>
                     <Button variant="ghost" size="icon" @click.stop="confirmDeleteActivity(act)" title="Eliminar" class="h-8 w-8 text-muted-foreground hover:text-destructive">
                       <Trash2 class="w-4 h-4" />
                     </Button>
                 </div>
             </div>
             
             <h2 class="text-[17px] font-extrabold text-foreground">{{ act.name }}</h2>
             <Badge :class="act.category === 'PERMANENT' ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400' : 'bg-primary/10 text-primary'" class="mt-2 text-[10px] uppercase tracking-wider border-0">
                {{ act.category === 'PERMANENT' ? 'Permanente' : 'Eventual' }}
             </Badge>
             <p v-if="act.category === 'EVENTUAL' && act.deadline_date" class="text-xs text-destructive font-bold mt-2">
                Límite: {{ act.deadline_date }}
             </p>
             <p class="text-muted-foreground text-sm mt-4 line-clamp-3 leading-relaxed">{{ act.description || 'Sin descripción' }}</p>
         </CardContent>

         <div class="mx-6 mb-6 pt-4 border-t flex justify-between items-center text-sm font-semibold text-primary group-hover:text-primary/80">
             Ver perfil de actividad
             <ArrowRight class="w-4 h-4" />
         </div>
       </Card>

       <Card v-if="activities.length === 0" class="col-span-full">
         <CardContent class="text-center text-muted-foreground p-12">
           No hay actividades creadas. Haz clic en "Nueva Actividad" para comenzar.
         </CardContent>
       </Card>
       <Card v-else-if="displayedActivities.length === 0" class="col-span-full">
         <CardContent class="text-center text-muted-foreground p-12">
           No hay actividades {{ activeTab === 'ACTIVE' ? 'activas' : 'archivadas' }}{{ searchQuery ? ` que coincidan con "${searchQuery}"` : '' }}.
         </CardContent>
       </Card>
    </div>

    <!-- Activity Form Modal -->
    <Dialog :open="showForm" @update:open="showForm = $event">
      <DialogHeader>
        <DialogTitle>Crear Actividad</DialogTitle>
      </DialogHeader>
      <form @submit.prevent="saveActivity" class="space-y-4">
          <div>
             <Label class="mb-1">Nombre</Label>
             <Input v-model="form.name" required type="text" />
          </div>
          <div>
              <Label class="mb-1">Categoría</Label>
              <select v-model="form.category" required class="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring">
                  <option value="PERMANENT">Permanente</option>
                  <option value="EVENTUAL">Eventual</option>
              </select>
          </div>
          <div v-if="form.category === 'EVENTUAL'">
             <Label class="mb-1">Fecha Límite</Label>
             <Input v-model="form.deadline_date" required type="date" />
          </div>
          <div>
             <Label class="mb-1">Descripción</Label>
             <textarea v-model="form.description" rows="3" class="flex min-h-[60px] w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"></textarea>
          </div>
          <div class="flex justify-end gap-3 mt-6">
              <Button type="button" variant="ghost" @click="showForm = false">Cancelar</Button>
              <Button type="submit" class="bg-emerald-600 hover:bg-emerald-700">Guardar</Button>
          </div>
      </form>
    </Dialog>

    <!-- Reactivate Form Modal -->
    <Dialog :open="showReactivateForm" @update:open="showReactivateForm = $event">
      <DialogHeader>
        <DialogTitle>Reactivar Actividad Eventual</DialogTitle>
      </DialogHeader>
      <form @submit.prevent="submitReactivate" class="space-y-4">
          <p class="text-sm text-muted-foreground mb-4">Para reactivar esta actividad, debes establecer una nueva fecha límite obligatoria.</p>
          <div>
             <Label class="mb-1">Nueva Fecha Límite</Label>
             <Input v-model="reactivateForm.deadline_date" required type="date" />
          </div>
          <div class="flex justify-end gap-3 mt-6">
              <Button type="button" variant="ghost" @click="showReactivateForm = false">Cancelar</Button>
              <Button type="submit" class="bg-emerald-600 hover:bg-emerald-700">Activar</Button>
          </div>
      </form>
    </Dialog>

    <!-- Delete Confirmation Dialog -->
    <Dialog :open="showDeleteConfirm" @update:open="showDeleteConfirm = $event">
      <DialogHeader>
        <DialogTitle>Confirmar Eliminación</DialogTitle>
      </DialogHeader>
      <div class="space-y-4">
          <p class="text-sm text-muted-foreground">
            ¿Seguro que deseas eliminar permanentemente la actividad <span class="font-bold text-foreground">"{{ deleteTarget?.name }}"</span>?
          </p>
          <p class="text-xs text-destructive">Esta acción eliminará todos los eventos y registros asociados.</p>
          <div class="flex justify-end gap-3 mt-6 pt-4 border-t">
              <Button type="button" variant="outline" @click="showDeleteConfirm = false">Cancelar</Button>
              <Button variant="destructive" @click="executeDelete">Eliminar</Button>
          </div>
      </div>
    </Dialog>

    <!-- Archive Confirmation Dialog -->
    <Dialog :open="showArchiveConfirm" @update:open="showArchiveConfirm = $event">
      <DialogHeader>
        <DialogTitle>Archivar Actividad</DialogTitle>
      </DialogHeader>
      <div class="space-y-4">
          <p class="text-sm text-muted-foreground">
            ¿Seguro que deseas archivar la actividad <span class="font-bold text-foreground">"{{ archiveTarget?.name }}"</span>?
          </p>
          <p class="text-xs text-muted-foreground">Podrás reactivarla después desde la pestaña "Archivadas".</p>
          <div class="flex justify-end gap-3 mt-6 pt-4 border-t">
              <Button type="button" variant="outline" @click="showArchiveConfirm = false">Cancelar</Button>
              <Button @click="executeArchive">Archivar</Button>
          </div>
      </div>
    </Dialog>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../plugins/axios'
import { Plus, LayoutGrid, Archive, Check, Trash2, ArrowRight, Search } from 'lucide-vue-next'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Dialog, DialogHeader, DialogTitle } from '@/components/ui/dialog'

const router = useRouter()
const activities = ref([])
const showForm = ref(false)
const activeTab = ref('ACTIVE')
const searchQuery = ref('')

const form = ref({ name: '', category: 'PERMANENT', deadline_date: '', description: '' })

const displayedActivities = computed(() => {
    const today = new Date();
    today.setHours(0,0,0,0);
    let result = activities.value.filter(act => {
        let isExpired = false;
        if (act.category === 'EVENTUAL' && act.deadline_date) {
            const parts = act.deadline_date.split('-');
            const deadline = new Date(parts[0], parts[1] - 1, parts[2]);
            if (deadline < today) isExpired = true;
        }
        const isCurrentlyActive = act.is_active && !isExpired;
        return activeTab.value === 'ACTIVE' ? isCurrentlyActive : !isCurrentlyActive;
    })
    
    // Apply search filter
    if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        result = result.filter(act => 
            act.name.toLowerCase().includes(query) ||
            (act.description || '').toLowerCase().includes(query) ||
            (act.category || '').toLowerCase().includes(query)
        )
    }
    
    return result
})

const goToProfile = (id) => { router.push(`/activities/${id}`) }

const fetchActivities = async () => {
    try {
        const res = await apiClient.get('activities/')
        activities.value = res.data?.results ?? res.data
    } catch (e) { console.error(e) }
}

const saveActivity = async () => {
    try {
        const payload = { ...form.value }
        if (payload.category === 'PERMANENT' || !payload.deadline_date) delete payload.deadline_date
        await apiClient.post('activities/', payload)
        showForm.value = false
        form.value = { name: '', category: 'PERMANENT', deadline_date: '', description: '' }
        fetchActivities()
    } catch (e) { alert("Error al guardar"); console.error(e) }
}

// --- Delete with confirmation ---
const showDeleteConfirm = ref(false)
const deleteTarget = ref(null)

const confirmDeleteActivity = (act) => {
    deleteTarget.value = act
    showDeleteConfirm.value = true
}

const executeDelete = async () => {
    if (!deleteTarget.value) return
    try {
        await apiClient.delete(`activities/${deleteTarget.value.id}/`)
        showDeleteConfirm.value = false
        deleteTarget.value = null
        fetchActivities()
    } catch (e) { console.error(e) }
}

// --- Archive with confirmation ---
const showArchiveConfirm = ref(false)
const archiveTarget = ref(null)

const confirmArchive = (act) => {
    archiveTarget.value = act
    showArchiveConfirm.value = true
}

const executeArchive = async () => {
    if (!archiveTarget.value) return
    try {
        await apiClient.patch(`activities/${archiveTarget.value.id}/`, { is_active: false })
        showArchiveConfirm.value = false
        archiveTarget.value = null
        fetchActivities()
    } catch (e) { console.error(e) }
}

// --- Reactivate ---
const showReactivateForm = ref(false)
const reactivateForm = ref({ id: null, deadline_date: '' })

const openReactivate = (act, event) => {
    event.stopPropagation();
    if (act.category === 'EVENTUAL') {
        reactivateForm.value = { id: act.id, deadline_date: '' };
        showReactivateForm.value = true;
    } else {
        reactivateActivity(act.id, { is_active: true });
    }
}

const reactivateActivity = async (id, payload) => {
    try {
        await apiClient.patch(`activities/${id}/`, payload);
        if (showReactivateForm.value) showReactivateForm.value = false;
        fetchActivities();
    } catch (e) { alert("Error al reactivar la actividad."); }
}

const submitReactivate = () => {
    reactivateActivity(reactivateForm.value.id, { is_active: true, deadline_date: reactivateForm.value.deadline_date })
}

onMounted(() => fetchActivities())
</script>
