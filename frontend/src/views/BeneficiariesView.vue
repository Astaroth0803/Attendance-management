<template>
  <div class="min-h-screen bg-background transition-colors duration-200">
    <div class="max-w-[1400px] mx-auto p-6 md:p-8 space-y-6">

     <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
       <h1 class="text-3xl font-bold text-foreground">Manejo de Usuarios</h1>
       <div class="flex flex-col sm:flex-row w-full sm:w-auto gap-3">
          <div class="relative w-full sm:w-64">
             <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
             <Input v-model="searchQuery" type="text" placeholder="Buscar por nombre o cédula..." class="pl-9 h-9" />
          </div>
          <div class="flex gap-2">
            <Button @click="exportToExcel" :disabled="!filteredAndSortedBeneficiaries.length" variant="outline" class="text-emerald-600 border-emerald-200 hover:bg-emerald-50 hover:text-emerald-700">
              <FileSpreadsheet class="w-4 h-4 mr-1" /> Excel
            </Button>
            <Button @click="exportToPDF" :disabled="!filteredAndSortedBeneficiaries.length" variant="outline" class="text-destructive border-red-200 hover:bg-red-50">
              <FileText class="w-4 h-4 mr-1" /> PDF
            </Button>
          </div>
       </div>
     </div>

    <!-- Table -->
    <Card>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-border">
        <thead class="bg-muted/50">
          <tr>
            <th @click="sortBy('first_name')" class="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider cursor-pointer hover:bg-muted group select-none">
                <div class="flex items-center gap-1">
                    Nombre Completo
                    <span v-if="sortKey === 'first_name'" class="text-primary">{{ sortOrder === 1 ? '↑' : '↓' }}</span>
                    <span v-else class="text-muted-foreground/30 opacity-0 group-hover:opacity-100 transition-opacity">↕</span>
                </div>
            </th>
            <th @click="sortBy('ci')" class="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider cursor-pointer hover:bg-muted group select-none">
                <div class="flex items-center gap-1">
                    Cédula
                    <span v-if="sortKey === 'ci'" class="text-primary">{{ sortOrder === 1 ? '↑' : '↓' }}</span>
                    <span v-else class="text-muted-foreground/30 opacity-0 group-hover:opacity-100 transition-opacity">↕</span>
                </div>
            </th>
            <th @click="sortBy('sector')" class="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider cursor-pointer hover:bg-muted group select-none">
                <div class="flex items-center gap-1">
                    Sector
                    <span v-if="sortKey === 'sector'" class="text-primary">{{ sortOrder === 1 ? '↑' : '↓' }}</span>
                    <span v-else class="text-muted-foreground/30 opacity-0 group-hover:opacity-100 transition-opacity">↕</span>
                </div>
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Acciones</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-border">
          <tr v-for="b in filteredAndSortedBeneficiaries" :key="b.id" class="hover:bg-muted/30 transition-colors">
            <td class="px-6 py-4 whitespace-nowrap text-foreground font-medium">{{ b.first_name }} {{ b.last_name }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-muted-foreground">{{ b.ci }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-muted-foreground">{{ b.sector }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
              <router-link :to="`/beneficiaries/${b.id}`">
                <Button variant="ghost" size="sm" class="text-emerald-600 hover:text-emerald-700 hover:bg-emerald-50">Ver Perfil</Button>
              </router-link>
              <Button variant="ghost" size="sm" @click="openEditForm(b)" class="text-indigo-600 hover:text-indigo-700 hover:bg-indigo-50">Editar</Button>
              <Button variant="ghost" size="sm" @click="confirmDelete(b)" class="text-destructive hover:bg-destructive/10">Eliminar</Button>
            </td>
          </tr>
          <tr v-if="filteredAndSortedBeneficiaries.length === 0">
              <td colspan="4" class="px-6 py-8 text-center text-muted-foreground">
                <div v-if="searchQuery">
                    No se encontraron resultados para "<span class="font-semibold">{{ searchQuery }}</span>".
                </div>
                <div v-else>
                    No hay beneficiarios registrados.
                </div>
              </td>
          </tr>
        </tbody>
        </table>
      </div>
    </Card>

    <!-- Edit Beneficiary Modal -->
    <Dialog :open="showEditForm" @update:open="showEditForm = $event">
      <DialogHeader>
        <DialogTitle>Editar Usuario</DialogTitle>
      </DialogHeader>
      <form @submit.prevent="submitEdit" class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
              <div>
                  <Label class="mb-1">Nombre *</Label>
                  <Input v-model="editForm.first_name" required type="text" />
              </div>
              <div>
                  <Label class="mb-1">Apellido *</Label>
                  <Input v-model="editForm.last_name" required type="text" />
              </div>
          </div>
          <div>
             <Label class="mb-1">Cédula o ID</Label>
             <Input v-model="editForm.ci" type="text" />
          </div>
          <div class="grid grid-cols-2 gap-4">
              <div>
                  <Label class="mb-1">Fecha de Nac. *</Label>
                  <Input v-model="editForm.dob" required type="date" />
              </div>
              <div>
                  <Label class="mb-1">Sexo *</Label>
                  <select v-model="editForm.sex" required class="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring">
                      <option value="M">Masculino</option>
                      <option value="F">Femenino</option>
                      <option value="O">Otro</option>
                  </select>
              </div>
          </div>
          <div>
             <Label class="mb-1">Sector *</Label>
             <Input v-model="editForm.sector" required type="text" />
          </div>
          <div v-if="editError" class="text-sm text-destructive bg-destructive/10 p-3 rounded-lg border border-destructive/20">
              {{ editError }}
          </div>
          <div class="flex justify-end gap-3 mt-6 pt-4 border-t">
              <Button type="button" variant="outline" @click="showEditForm = false">Cancelar</Button>
              <Button type="submit" :disabled="editLoading">
                  {{ editLoading ? 'Guardando...' : 'Guardar Cambios' }}
              </Button>
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
            ¿Seguro que deseas eliminar permanentemente a <span class="font-bold text-foreground">{{ deleteTarget?.first_name }} {{ deleteTarget?.last_name }}</span>?
          </p>
          <p class="text-xs text-destructive">Esta acción no se puede deshacer.</p>
          <div class="flex justify-end gap-3 mt-6 pt-4 border-t">
              <Button type="button" variant="outline" @click="showDeleteConfirm = false">Cancelar</Button>
              <Button variant="destructive" @click="executeDelete" :disabled="deleteLoading">
                  {{ deleteLoading ? 'Eliminando...' : 'Eliminar' }}
              </Button>
          </div>
      </div>
    </Dialog>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import apiClient from '../plugins/axios'
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'
import * as XLSX from 'xlsx'
import { Search, FileSpreadsheet, FileText } from 'lucide-vue-next'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Dialog, DialogHeader, DialogTitle } from '@/components/ui/dialog'

const beneficiaries = ref([])

const fetchItems = async () => {
    try {
        const res = await apiClient.get('beneficiaries/')
        beneficiaries.value = res.data?.results ?? res.data
    } catch (e) { console.error(e) }
}

// --- Edit ---
const showEditForm = ref(false)
const editLoading = ref(false)
const editError = ref('')
const editForm = ref({ id: null, ci: '', first_name: '', last_name: '', dob: '', sex: 'M', sector: '' })

const openEditForm = (b) => {
    editForm.value = {
        id: b.id,
        ci: b.ci || '',
        first_name: b.first_name,
        last_name: b.last_name,
        dob: b.dob || '',
        sex: b.sex || 'M',
        sector: b.sector || ''
    }
    editError.value = ''
    showEditForm.value = true
}

const submitEdit = async () => {
    editLoading.value = true
    editError.value = ''
    try {
        const { id, ...payload } = editForm.value
        await apiClient.patch(`beneficiaries/${id}/`, payload)
        showEditForm.value = false
        fetchItems()
    } catch (e) {
        console.error(e)
        editError.value = e.response?.data?.ci?.[0] || e.response?.data?.detail || 'Error al guardar los cambios.'
    } finally { editLoading.value = false }
}

// --- Delete with confirmation dialog ---
const showDeleteConfirm = ref(false)
const deleteTarget = ref(null)
const deleteLoading = ref(false)

const confirmDelete = (b) => {
    deleteTarget.value = b
    showDeleteConfirm.value = true
}

const executeDelete = async () => {
    if (!deleteTarget.value) return
    deleteLoading.value = true
    try {
        await apiClient.delete(`beneficiaries/${deleteTarget.value.id}/`)
        showDeleteConfirm.value = false
        deleteTarget.value = null
        fetchItems()
    } catch (e) {
        console.error(e)
    } finally { deleteLoading.value = false }
}

// --- Search & Sort ---
const searchQuery = ref('')
const sortKey = ref('')
const sortOrder = ref(1)

const sortBy = (key) => {
    if (sortKey.value === key) {
        sortOrder.value = sortOrder.value * -1
    } else {
        sortKey.value = key
        sortOrder.value = 1
    }
}

const filteredAndSortedBeneficiaries = computed(() => {
    let result = beneficiaries.value
    if (searchQuery.value) {
        const query = searchQuery.value?.toLowerCase() || ''
        result = result.filter(b => {
            const fullName = `${b.first_name || ''} ${b.last_name || ''}`.toLowerCase()
            const ci = b.ci?.toLowerCase() || ''
            return fullName.includes(query) || ci.includes(query)
        })
    }
    if (sortKey.value) {
        result = [...result].sort((a, b) => {
            let valA = a[sortKey.value] || ''
            let valB = b[sortKey.value] || ''
            if (sortKey.value === 'first_name') {
                valA = `${a.first_name || ''} ${a.last_name || ''}`.toLowerCase()
                valB = `${b.first_name || ''} ${b.last_name || ''}`.toLowerCase()
            } else {
                valA = valA?.toString()?.toLowerCase() || ''
                valB = valB?.toString()?.toLowerCase() || ''
            }
            if (valA < valB) return -1 * sortOrder.value
            if (valA > valB) return 1 * sortOrder.value
            return 0
        })
    }
    return result
})

// --- Exports ---
const getLocalISODateStr = (d) => {
    const y = d.getFullYear()
    const m = String(d.getMonth() + 1).padStart(2, '0')
    const day = String(d.getDate()).padStart(2, '0')
    const h = String(d.getHours()).padStart(2, '0')
    const min = String(d.getMinutes()).padStart(2, '0')
    return `${y}-${m}-${day}_${h}${min}`
}

const exportToPDF = () => {
    if (!filteredAndSortedBeneficiaries.value.length) return
    const doc = new jsPDF()
    doc.text("Listado de Usuarios", 14, 15)
    const head = [['Nombre Completo', 'Cédula', 'Fecha Nacimiento', 'Sector']]
    const bodyDate = filteredAndSortedBeneficiaries.value.map(b => [
        `${b.first_name} ${b.last_name}`, b.ci, b.dob || 'N/A', b.sector || 'N/A'
    ])
    autoTable(doc, { head, body: bodyDate, startY: 25, theme: 'grid', headStyles: { fillColor: [234, 88, 12] } })
    doc.save(`Usuarios_${getLocalISODateStr(new Date())}.pdf`)
}

const exportToExcel = () => {
    if (!filteredAndSortedBeneficiaries.value.length) return
    const data = filteredAndSortedBeneficiaries.value.map(b => ({
        'Nombre Completo': `${b.first_name} ${b.last_name}`,
        'Cédula': b.ci,
        'Fecha Nacimiento': b.dob || 'N/A',
        'Sector': b.sector || 'N/A'
    }))
    const ws = XLSX.utils.json_to_sheet(data)
    ws['!cols'] = [{ wch: 35 }, { wch: 20 }, { wch: 20 }, { wch: 30 }]
    const range = XLSX.utils.decode_range(ws['!ref'])
    for (let c = range.s.c; c <= range.e.c; c++) {
        const cellAddress = XLSX.utils.encode_cell({ r: 0, c: c })
        if (!ws[cellAddress]) continue
        ws[cellAddress].s = { font: { bold: true } }
    }
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, ws, "Usuarios")
    XLSX.writeFile(wb, `Usuarios_${getLocalISODateStr(new Date())}.xlsx`)
}

onMounted(() => fetchItems())
</script>
