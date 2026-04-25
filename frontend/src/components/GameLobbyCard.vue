<script setup>
import { lobbiesApi } from "@/api/lobbies"

defineProps(['data'])

const handleJoinToLobby = async (id) => {
    try {
        const res = await lobbiesApi.joinToLobby(id);
    } catch (err) {
        alert(err.response?.data?.detail || "Failed to join");
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
        <button class="join-lobby-btn" @click="handleJoinToLobby(data.id)">+</button>
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

</style>