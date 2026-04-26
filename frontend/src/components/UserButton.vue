<script setup>
import { ref } from 'vue'
import ProfileModal from './ProfileModal.vue'
import SvgIcon from './UI/SvgIcon.vue'
import { authApi } from '@/api/auth'

const isModalOpen = ref(false)
const userData = ref(null)

const openProfile = async () => {
  isModalOpen.value = true
  try {
    userData.value = await authApi.getUserData() 
  } catch (err) {
    console.error("Failed to load profile", err)
  }
}
</script>

<template>
  <div class="user-profile-wrapper">
    <button class="profile-btn" @click="openProfile">
      <SvgIcon name="profile" class="main-icon"/>
    </button>

    <ProfileModal 
      :isOpen="isModalOpen" 
      :userStats="userData" 
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