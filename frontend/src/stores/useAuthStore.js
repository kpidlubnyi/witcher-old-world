import { defineStore } from 'pinia';
import { authApi } from '@/api/auth';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isLoggedIn: false,
    loading: false,
    error: null,
  }),
  
  actions: {
    async handleSocialCallback(provider, code) {
      this.loading = true;
      this.error = null;
      
      try {
        let userData;

        switch (provider) {
          case 'google':
            userData = await authApi.handleGoogleCallback(code);
            break;
            
          case 'github':
            userData = await authApi.handleGithubCallback(code);
            break;

          default:
            throw new Error(`Unsupported auth provider: ${provider}`);
        }

        this.user = userData;
        this.isLoggedIn = true;
        return userData;

      } catch (err) {
        this.user = null;
        this.isLoggedIn = false;
        this.error = err.response?.data?.detail || err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },

    async checkAuth() {
      try {
        const userData = await authApi.getProfile();
        this.user = userData;
        this.isLoggedIn = true;
      } catch (err) {
        this.user = null;
        this.isLoggedIn = false;
      }
    }
  }
});