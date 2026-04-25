import { api } from "./client";

export const lobbiesApi = {
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

