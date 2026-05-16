import { defineStore } from 'pinia'
import { ref } from 'vue'
import apiClient from '../plugins/axios'

export const useUserStore = defineStore('user', () => {
    const user = ref({ first_name: '', last_name: '', username: '' })
    const loaded = ref(false)

    const fetchUser = async () => {
        try {
            const token = localStorage.getItem('access_token')
            if (!token) return
            const payload = JSON.parse(atob(token.split('.')[1]))
            if (payload.user_id) {
                const res = await apiClient.get(`users/${payload.user_id}/`)
                user.value = res.data
                loaded.value = true
            }
        } catch (error) {
            console.error("Error fetching user", error)
        }
    }

    const clearUser = () => {
        user.value = { first_name: '', last_name: '', username: '' }
        loaded.value = false
    }

    return { user, loaded, fetchUser, clearUser }
})
