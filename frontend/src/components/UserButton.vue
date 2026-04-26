<script setup>
import { ref } from 'vue'
import ProfileModal from './ProfileModal.vue'
import SvgIcon from './UI/SvgIcon.vue'

const isModalOpen = ref(false)
const userStats = ref(null)

const toggleProfile = () => {
  isModalOpen.value = !isModalOpen.value
  if (isModalOpen.value) {
    userStats.value = { games_played: 120, wins: 45, win_rate: "37.5%" }
  }
}
</script>

<template>
  <div class="user-profile-wrapper">
    <button class="profile-btn" @click="toggleProfile">
      <SvgIcon name="profile" class="main-icon"/>
    </button>

    <ProfileModal 
      :isOpen="isModalOpen" 
      :userStats="userStats" 
      @close="isModalOpen = false" 
    />
  </div>
</template>

<style scoped>
.main-icon {
    width: 55px !important;
    height: 55px !important;
    fill: black;
    transition: 0.2s ease-in-out;
}

.profile-btn {
  position: absolute;
  top: 8px;
  left: 8px;
  width: 85px;
  height: 85px;
  

  background-color: #e0e0e0;
  border-radius: 50%;
  border: none;

  
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10;

  box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.4);
  transition: 0.2s ease-in-out;
}

.profile-btn:hover {
  background-color: #bdbdbd;
  transition: 0.2s ease-in-out;
}

.profile-btn:hover .main-icon {
  fill: #ececec;

}
</style>