<script setup>
defineProps(['isOpen', 'userStats']);
const emit = defineEmits(['close']);
</script>

<template>
  <Teleport to="body">
    <Transition name="fade">
      <div v-if="isOpen" class="modal-overlay" @click.self="emit('close')">
        <div class="modal-content">
          <button class="close-btn" @click="emit('close')">&times;</button>
          
          <h2>Profile Statistics</h2>
          <div v-if="userStats" class="stats-grid">
            <div class="stat-item">
              <span>Games Played:</span>
              <strong>{{ userStats.games_played }}</strong>
            </div>
            <div class="stat-item">
              <span>Wins:</span>
              <strong class="text-green">{{ userStats.wins }}</strong>
            </div>
            <div class="stat-item">
              <span>Win Rate:</span>
              <strong>{{ ((userStats.wins / userStats.games_played) * 100).toFixed(1) }}%</strong>
            </div>
          </div>
          <div v-else>Loading stats...</div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 15px;
  position: relative;
  min-width: 300px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.2);
  color: #333;
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 15px;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
}

.stats-grid {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.text-green { color: #26b619; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>