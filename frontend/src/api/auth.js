import { api } from "./client";

export const authApi = {
  async handleGoogleCallback(code) {
    try {
      const response = await api.post("/auth/google/callback", { code });
      return response.data;
      
    } catch (error) {
      const message = error.response?.data?.detail || "Failed to authenticate";
      throw new Error(message);
    }
  },
  async handleGithubCallback(code) {
    try {
      const response = await api.post("/auth/github/callback", { code });
      return response.data;
      
    } catch (error) {
      const message = error.response?.data?.detail || "Failed to authenticate";
      throw new Error(message);
    }
  },
  async getProfile() {
    try {
      const { data } = await api.get("/auth/profile")
      return data
    } catch (error) {
        throw error;
    }
  },
  async logout() {
    await api.post("/auth/logout");
  }
};