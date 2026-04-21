// src/stores/useAuthStore.js
import { defineStore } from 'pinia';
import { authApi } from '@/api/auth';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    loading: false,
    error: null,
  }),
  actions: {
    async handleGoogleCallback(code) {
      this.loading = true;
      try {
        const data = await authApi.exchangeCodeForToken(code);
        this.user = data.user;
        return data;
      } catch (err) {
        this.error = err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    }
  }
});