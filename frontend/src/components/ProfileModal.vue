<script setup>
defineProps(['isOpen', 'userStats']);
const emit = defineEmits(['close']);
import SvgIcon from './UI/SvgIcon.vue';
import { authApi } from '@/api/auth';


const handleLogout = async () => {
    try {
        await authApi.logout();
        window.location.reload(); 
    } catch (err) {
        console.error("Logout failed", err);
    }
};
</script>

<template>
  <Teleport to="body">
    <Transition name="fade">
      <div v-if="isOpen" class="modal-overlay" @click.self="emit('close')">
        <div class="modal-window">
          <button class="close-btn" @click="emit('close')">&times;</button>

          <div class="modal-content">
            <div class="content-header">
              <img v-if="userStats?.picture" :src="userStats.picture" class="header-photo" referrerpolicy="no-referrer">
              <div class="header-info">
                <div class="user-name">{{ userStats?.name || "Witcher" }}</div>
                <div class="created-at"> With us since: {{ userStats?.created_at }} </div>
              </div>
            </div>

            <div class="modal-divider"></div>
          
          </div>

          <button class="logout-btn" @click="handleLogout">
            <SvgIcon name="logout" class="svg-icon" />
          </button>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
@font-face {
  font-family: 'Witcher';
  src: url('./fonts/thewitcher.ttf') format('truetype');
  font-display: swap;
}

* {
  box-sizing: border-box;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-window {
  width: 800px;
  height: 600px;

  background: whitesmoke;
  padding: 30px;
  border-radius: 20px;
  position: relative;
  min-width: 300px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.2);
  color: #333;
}

.modal-content {
  width: 98%;
  height: 90%;
  margin: 1%;

  display: flex;
  flex-direction: column;
}

.content-header {
  width: 100%;
  height: 40%;

  display: flex;
  align-items: center;

  padding: 10px;
  gap: 16px;
}

.header-photo {
  width: 25%;
  height: 100%;
  border-radius: 50%;

  box-shadow: 0 0 20px rgba(0,0,0, 0.6);
}

.header-info {
  height: 100%;
  width: 75%;

  display: flex;
  flex-direction: column;
  gap: 12px;
  padding-top: 10px
}

.user-name {
  font-size: 40pt;
  font-family: "Witcher", sans-serif;
  font-weight: 800;
}


.created-at {
  font-size: 20pt;
  font-family: "Witcher", sans-serif;
  font-weight: 400;
}


.modal-divider {
  width: 100%;
  height: 6px;
  border-radius: 99px;

  background-color: rgb(109, 109, 109);
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

.logout-btn {
  width: 65px;
  height: 65px;
  border-radius: 50%;

  display: flex;
  
  position: absolute;
  bottom: 10px;
  right: 15px;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  transition: 0.2s ease-in-out;
}

.logout-btn:hover {
  background-color: red;
  transition: 0.2s ease-in-out;
}

.svg-icon {
  width: 50px;
  transition: 0.2s ease-in-out;
}

.logout-btn:hover .svg-icon {
  fill: white;
  transition: 0.2s ease-in-out;
}


.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>