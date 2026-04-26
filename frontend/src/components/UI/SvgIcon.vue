<script setup>
import Login from '../../../assets/icons/login.svg?component'
import Cross from '../../../assets/icons/cross.svg?component'
import Github from '../../../assets/icons/github.svg?component'
import Google from '../../../assets/icons/google.svg?component'
import Signup from '../../../assets/icons/signup.svg?component'
import Profile from '../../../assets/icons/profile.svg?component'

const props = defineProps({
  name: {
    type: String,
    required: true
  }
})

const iconMap = {
    profile: Profile,
    login: Login,   
    signup: Signup,      
    cross: Cross,

    github: Github,
    google: Google,
}
</script>

<template>
  <component 
    :is="iconMap[name]" 
    v-if="iconMap[name]" 
    class="svg-icon"
  />
  <span v-else style="color: red; font-size: 10px;">Icon "{{ name }}" not found</span>
</template>

<style scoped>
.svg-icon {
  width: 100%;
  height: 100%;
  fill: currentColor; 
  display: inline-block;
}
</style>