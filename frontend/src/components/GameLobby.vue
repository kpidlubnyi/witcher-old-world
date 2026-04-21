<script setup>
import GameLobbyCard from './GameLobbyCard.vue'
import { useWebSocket } from '../useWebSocket'
import AuthButton from './AuthButton.vue'

const { data, connect } = useWebSocket("ws://localhost:8000/lobbies/")
connect()


</script>

<template>
  <AuthButton class="auth-button"/>
<h1>Lobbies:</h1>
<ul>
  <li v-for="lobby in data || []" :key="lobby.id">
    <GameLobbyCard :data="lobby" />
  </li>
</ul>
</template>

<style scoped>
.auth-button {
  position: fixed;
  left: 93%
}
</style>