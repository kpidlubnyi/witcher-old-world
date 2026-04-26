<script setup>
import GameLobbyCard from './GameLobbyCard.vue'
import AuthButton from './AuthButton.vue'
import UserButton from './UserButton.vue'

import { useWebSocket } from '../useWebSocket'
import { ref, onMounted } from 'vue'
import { lobbiesApi } from '@/api/lobbies'


const { data, connect } = useWebSocket("ws://localhost:8000/lobbies/")
const activeLobbyId = ref(null)
const showCreateForm = ref(false)
const isLoggedIn = ref(false)

onMounted(async () => {
  connect()
  try {
    const status = await lobbiesApi.getMyStatus()
    isLoggedIn.value = true
    activeLobbyId.value = status.lobby_id
  } catch (err) {
    isLoggedIn = false
    console.error(`Failed to get status: ${err}`)
  }
})

const updateActiveLobby = (id) => {
  activeLobbyId.value = id
}

const lobbyName = ref("")
const maxPlayers = ref(4)

const handleCreateLobby = async () => {
  try {
    const formData = new FormData()
    formData.append("name", lobbyName.value)
    formData.append("max_players", maxPlayers.value)

    const res = await lobbiesApi.createLobby(formData)

    activeLobbyId.value = res.id
    showCreateForm.value = false
    lobbyName.value = ""
  } catch (err) {
    alert(err.response?.data?.detail || "Failed to create lobby!")
  }
}
</script>

<template>
  <div class="top-right-corner">
    <UserButton v-if="isLoggedIn"/>
    <AuthButton v-else class="auth-button"/>
  </div>

  <h1>Lobbies:</h1>

  <button
    v-if="!showCreateForm && isLoggedIn"
    :disabled="activeLobbyId"
    @click="showCreateForm = true"
    class="open-form-btn"
  >
    Create New Lobby
  </button>

  <div v-if="showCreateForm" class="craete-form">
    <input v-model="lobbyName" placeholder="Lobby Name" type="text" required />
    <div class="player-input-group">
      <label for="max-players">Players (2-5):</label>
      <input id="max-players" v-model.number="maxPlayers"  type="number" min="2" max="5" step="1"/>
    </div>

    <div class="form-actions">
      <button @click="handleCreateLobby" class="submit-btn">Create</button>
      <button @click="showCreateForm = false" class="cancel-btn">Cancel</button>
    </div>
  </div> 

  <ul>
    <li v-for="lobby in data || []" :key="lobby.id">
      <GameLobbyCard 
        :data="lobby" 
        :activeLobbyId="activeLobbyId"
        :isLoggedIn="isLoggedIn"
        @status-changed="updateActiveLobby"
      />
    </li>
  </ul>
</template>

<style scoped>
.top-right-corner {
  position: fixed;
  right: 120px;
}

.create-lobby-btn {
  width: 200px;
  height: 60px;
  font-size: 20pt;
}

</style>