<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-orange-400 via-primary to-red-500 font-sans text-white p-4 overflow-hidden relative">
    
    <!-- Decorative blobs -->
    <div class="absolute top-10 left-10 w-72 h-72 bg-yellow-300 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob"></div>
    <div class="absolute top-10 right-10 w-72 h-72 bg-pink-400 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob" style="animation-delay: 2s;"></div>
    <div class="absolute -bottom-20 left-40 w-72 h-72 bg-orange-300 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob" style="animation-delay: 4s;"></div>

    <!-- Central glassmorphism card -->
    <div class="relative max-w-3xl w-full flex flex-col items-center justify-center bg-white/10 backdrop-blur-lg rounded-3xl p-8 md:p-12 shadow-2xl border border-white/20 z-10 text-center"
         v-motion
         :initial="{ opacity: 0, scale: 0.95, y: 30 }"
         :enter="{ opacity: 1, scale: 1, y: 0, transition: { duration: 700, type: 'spring', stiffness: 100 } }">
      
      <div class="space-y-8 w-full flex flex-col items-center">
        
        <div class="space-y-3">
          <p class="text-orange-100 font-semibold tracking-widest uppercase text-sm md:text-base">
             Bienvenidos al
          </p>
          <h1 class="text-4xl md:text-5xl lg:text-6xl font-extrabold leading-tight drop-shadow-md">
            Centro Juvenil <br />
            <span class="text-orange-200">Y Biblioteca</span>
          </h1>
          <h2 class="text-3xl md:text-4xl font-bold mt-2 text-white/90 tracking-wide drop-shadow-sm">
            Las Mañanitas
          </h2>
        </div>

        <p class="text-orange-50 text-base md:text-lg max-w-md font-light">
          Tu espacio interactivo para el aprendizaje, la lectura y el desarrollo personal. Selecciona una opción para continuar.
        </p>

        <!-- CTA Buttons -->
        <div class="flex flex-col sm:flex-row gap-5 justify-center pt-2">
          
          <router-link to="/login" class="group flex items-center justify-center gap-3 bg-white text-primary px-8 py-4 rounded-2xl font-bold text-lg shadow-xl hover:shadow-2xl hover:-translate-y-1 transition-all duration-300 focus:outline-none focus:ring-4 focus:ring-white/50">
            <LogIn class="h-6 w-6 group-hover:translate-x-1 transition-transform" />
            Entrar
          </router-link>
          
          <router-link to="/attendance" class="flex items-center justify-center gap-3 bg-white/15 hover:bg-white/25 border border-white/30 text-white px-8 py-4 rounded-2xl font-bold text-lg shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all duration-300 backdrop-blur-sm focus:outline-none focus:ring-4 focus:ring-white/30">
            <ClipboardList class="h-6 w-6" />
            Asistencia
          </router-link>
        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
import { LogIn, ClipboardList } from 'lucide-vue-next'
</script>

<style scoped>
@keyframes blob {
  0%   { transform: translate(0px, 0px) scale(1); }
  33%  { transform: translate(30px, -50px) scale(1.1); }
  66%  { transform: translate(-20px, 20px) scale(0.9); }
  100% { transform: translate(0px, 0px) scale(1); }
}

.animate-blob {
  animation: blob 7s infinite;
}
</style>
