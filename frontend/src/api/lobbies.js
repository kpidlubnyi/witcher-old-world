import { api } from "./client";

export const lobbiesApi = {
    async createLobby(formData) {
        try {
            const { data } = await api.post("/lobbies/create", formData);
            return data;
        } catch (error) {
            console.error("Error creating lobby:", error);
            throw error;
        }
    },
    async joinToLobby(lobbyId) {
        try {
            const response = await api.post(`/lobbies/${lobbyId}/join`);
            return response.data; 
        } catch (error) {
            throw error;
        }
    },
    async leaveLobby(lobbyId) {
        try {
            const response = await api.post(`/lobbies/${lobbyId}/leave`);
            return response.data; 
        } catch (error) {
            throw error;
        }
    },    
    async getMyStatus() {
        try {
            const { data } = await api.get(`/lobbies/my-status`);
            return data; 
        } catch (error) {
            throw error;
        }
    }
}

