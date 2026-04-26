<script setup>
import { onMounted } from 'vue';
import { useAuthStore } from '@/stores/useAuthStore';
import { useRouter, useRoute } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();

onMounted(async () => {
  const queryParams = new URLSearchParams(window.location.search);
  const code = queryParams.get("code");
  const provider = route.params.provider;

  if (code && provider) {
    try {
      await authStore.handleSocialCallback(provider, code);
      router.push({ name: "home" }); 
    } catch (err) {
      console.error(`${provider} auth failed:`, err);
      router.push({ name: "login", query: { error: 'auth_failed' } });
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