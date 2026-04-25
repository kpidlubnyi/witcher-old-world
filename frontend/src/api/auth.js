import { api } from "./client";

export const authApi = {
  async exchangeCodeForToken(code) {
    try {
      const response = await api.post("/auth/google/callback", { code });
      return response.data;
      
    } catch (error) {
      const message = error.response?.data?.detail || "Failed to authenticate";
      throw new Error(message);
    }
  }
};