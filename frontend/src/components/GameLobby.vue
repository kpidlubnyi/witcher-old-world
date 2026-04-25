<script setup>
import GameLobbyCard from './GameLobbyCard.vue'
import { useWebSocket } from '../useWebSocket'
import AuthButton from './AuthButton.vue'
import { ref, onMounted } from 'vue'
import { lobbiesApi } from '@/api/lobbies'


const { data, connect } = useWebSocket("ws://localhost:8000/lobbies/")
const activeLobbyId = ref(null)

onMounted(async () => {
  connect()
  try {
    const status = await lobbiesApi.getMyStatus()
    activeLobbyId.value = status.lobby_id
  } catch (err) {
    console.error(`Failed to get status: ${err}`)
  }
})

const updateActiveLobby = (id) => {
  activeLobbyId.value = id
}
</script>

<template>
  <AuthButton class="auth-button"/>
<h1>Lobbies:</h1>
<ul>
  <li v-for="lobby in data || []" :key="lobby.id">
    <GameLobbyCard 
      :data="lobby" 
      :activeLobbyId="activeLobbyId"
      @status-changed="updateActiveLobby"
    />
  </li>
</ul>
</template>

<style scoped>
.auth-button {
  position: fixed;
  left: 93%
}
</style>