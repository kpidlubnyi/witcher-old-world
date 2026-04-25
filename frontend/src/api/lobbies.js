import { api } from "./client";

export const lobbiesApi = {
    async joinToLobby(lobbyId) {
        try {
            const response = await api.post(`/lobbies/${lobbyId}/join`);
            return response.data; 
        } catch (error) {
            throw error;
        }
    }
}