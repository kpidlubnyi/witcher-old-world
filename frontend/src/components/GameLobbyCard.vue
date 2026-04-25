<script setup>
import { lobbiesApi } from "@/api/lobbies"
import { computed } from "vue";


const props = defineProps(['data', 'activeLobbyId'])  
const emit = defineEmits(['status-changed'])


const isMyLobby = computed(() => props.activeLobbyId === props.data.id)
const isInAnyLobby = computed(() => !!props.activeLobbyId)

const handleJoinToLobby = async (id) => {
    try {
        await lobbiesApi.joinToLobby(id);
        emit("status-changed", id)
    } catch (err) {
        alert(err.response?.data?.detail || "Failed to join");
    }
}

const handleLeaveLobby = async (id) => {
    try {
        await lobbiesApi.leaveLobby(id);
        emit("status-changed", null)
    } catch (err) {
        alert(err.response?.data?.detail || "Failed to leave");
    }
}
</script>


<template>
<div class="card-container">
    <div class="card-info">
        <div>{{ data.name }}</div>
        <div>created by {{ data.host_name }} </div>
        <div>{{ data.created_ago }}</div>
        <div>{{ data.current_players }} / {{ data.max_players }} players</div>
    </div>
    <div class="card-interaction">
        <button v-if="isMyLobby" class="leave-lobby-btn" @click="handleLeaveLobby(data.id)">
            -
        </button>

        <button v-else 
            class="join-lobby-btn" 
            :disabled="isInAnyLobby"
            :class="{ 'btn-disabled': isInAnyLobby}" 
            @click="handleJoinToLobby(data.id)">
            +
        </button>
    </div>
</div>
</template>


<style>
.card-container {
    width: 300px;
    height: 120px;
    background-color: lightgray;
    border-radius: 10px;
    display: flex;
}

.card-info {
    position: relative;
    width: 70%;
    height: 100%;
}

.card-interaction {
    position: relative;
    width: 30%;
    height: 100%;

    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.join-lobby-btn {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    border: none;
    background-color: #26b619;
    color: whitesmoke;
    font-size: 20pt;
}

.leave-lobby-btn {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    border: none;
    background-color: #d41b1b;
    color: whitesmoke;
    font-size: 20pt;
}

.btn-disabled {
    background-color: #95a5a6 !important;
    cursor: not-allowed;
    opacity: 0.6;
}

</style>