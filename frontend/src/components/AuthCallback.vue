<script setup>
import { onMounted } from 'vue';
import { useAuthStore } from '@/stores/useAuthStore';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

onMounted(async () => {
  const queryParams = new URLSearchParams(window.location.search);
  const code = queryParams.get("code");

  if (code) {
    try {
      await authStore.handleGoogleCallback(code);
      router.push({name: "home"}); 
    } catch (err) {
      console.error("Auth failed:", err);
    }
  }
});
</script>

<template>
  <div v-if="authStore.loading">Авторизація...</div>
  <div v-else-if="authStore.user">
    <h1>Siema, {{ authStore.user.name }}</h1>
    <img :src="authStore.user.picture" alt="Avatar">
  </div>
  <div v-else>Щось пішло не так...</div>
</template>