<template>
  <div class="min-h-screen bg-background transition-colors duration-200">
    <div class="max-w-[1400px] mx-auto p-6 md:p-8 space-y-6">

     <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
       <h1 class="text-3xl font-bold text-foreground">Administradores del Sistema</h1>
       <Button @click="openCreateForm">
         <Plus class="w-4 h-4 mr-1" /> Nuevo Administrador
       </Button>
     </div>

    <Card>
      <table class="min-w-full divide-y divide-border">
        <thead class="bg-muted/50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Nombre</th>
            <th class="px-6 py-3 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Usuario</th>
            <th class="px-6 py-3 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Correo</th>
            <th class="px-6 py-3 text-left text-xs font-bold text-muted-foreground uppercase tracking-wider">Acciones</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-border">
          <tr v-for="user in users" :key="user.id" class="hover:bg-muted/30 transition-colors">
            <td class="px-6 py-4 whitespace-nowrap text-foreground font-medium">{{ user.first_name }} {{ user.last_name }}</td>
            <td class="px-6 py-4 whitespace-nowrap font-bold text-primary">{{ user.username }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-muted-foreground">{{ user.email }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
              <Button variant="ghost" size="sm" @click="openEditForm(user)" class="text-indigo-600 hover:text-indigo-700 hover:bg-indigo-50">Editar</Button>
              <Button variant="ghost" size="sm" @click="deleteItem(user.id)" class="text-destructive hover:bg-destructive/10">Eliminar</Button>
            </td>
          </tr>
          <tr v-if="users.length === 0">
              <td colspan="4" class="px-6 py-8 text-center text-muted-foreground">
                  No hay administradores registrados o cargando...
              </td>
          </tr>
        </tbody>
      </table>
    </Card>

    <!-- Modal Form -->
    <Dialog :open="showForm" @update:open="showForm = $event">
      <DialogHeader>
        <DialogTitle>{{ isEditing ? 'Editar Administrador' : 'Nuevo Administrador' }}</DialogTitle>
      </DialogHeader>
      <form @submit.prevent="saveUser" class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
              <div>
                  <Label class="mb-1">Nombre</Label>
                  <Input v-model="form.first_name" required type="text" />
              </div>
              <div>
                  <Label class="mb-1">Apellido</Label>
                  <Input v-model="form.last_name" required type="text" />
              </div>
          </div>
          <div>
             <Label class="mb-1">Usuario (Login)</Label>
             <Input v-model="form.username" required type="text" />
          </div>
          <div>
             <Label class="mb-1">Correo Electrónico</Label>
             <Input v-model="form.email" required type="email" />
          </div>
          <div v-if="!isEditing || form.password">
             <Label class="mb-1">
                 Contraseña <span v-if="isEditing" class="text-xs font-normal text-muted-foreground">(Déjalo en blanco para mantener la actual)</span>
             </Label>
             <input v-model="form.password" :required="!isEditing" type="password" class="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring" />
          </div>
          <div class="flex justify-end gap-3 mt-6">
              <Button type="button" variant="outline" @click="showForm = false">Cancelar</Button>
              <Button type="submit">Guardar</Button>
          </div>
      </form>
    </Dialog>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '../plugins/axios'
import { Plus } from 'lucide-vue-next'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Dialog, DialogHeader, DialogTitle } from '@/components/ui/dialog'

const users = ref([])
const showForm = ref(false)
const isEditing = ref(false)
const editingId = ref(null)
const form = ref({ username: '', email: '', first_name: '', last_name: '', password: '' })

const fetchItems = async () => {
    try {
        const res = await apiClient.get('users/')
        users.value = res.data
    } catch (e) { console.error(e) }
}

const openCreateForm = () => {
    isEditing.value = false
    editingId.value = null
    form.value = { username: '', email: '', first_name: '', last_name: '', password: '' }
    showForm.value = true
}

const openEditForm = (user) => {
    isEditing.value = true
    editingId.value = user.id
    form.value = { username: user.username, email: user.email, first_name: user.first_name, last_name: user.last_name, password: '' }
    showForm.value = true
}

const saveUser = async () => {
    try {
        const payload = { ...form.value }
        if (isEditing.value && !payload.password) delete payload.password
        if (isEditing.value) {
            await apiClient.patch(`users/${editingId.value}/`, payload)
        } else {
            await apiClient.post('users/', payload)
        }
        showForm.value = false
        fetchItems()
    } catch (e) {
        alert("Error al guardar usuario. Revisa que el usuario no exista previamente.")
        console.error(e)
    }
}

const deleteItem = async (id) => {
    if(confirm('¿Seguro que deseas eliminar este administrador?')) {
        try {
            await apiClient.delete(`users/${id}/`)
            fetchItems()
        } catch (e) { console.error(e); alert("No se pudo eliminar el administrador.") }
    }
}

onMounted(() => fetchItems())
</script>
