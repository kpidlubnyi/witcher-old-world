<script setup>
import { ref } from 'vue';
import SvgIcon from './UI/SvgIcon.vue';

const isExpanded = ref(false);

const toggleExpand = () => {
  isExpanded.value = !isExpanded.value;
};

function loginWithGoogle() {
    window.location.href = 'http://localhost:8000/auth/google/url';
}
</script>

<template>
    <div auth-zone>
        <div :class="['auth-expand-toggler', {'expanded': isExpanded}]" @click="toggleExpand" >
            <SvgIcon :name="isExpanded? 'cross': 'login'" class="main-auth-icon"/>
        </div>

        <div :class="['auth-wrapper', {'expanded': isExpanded}]">
            <div :class="['content-side', {'expanded': isExpanded}]" v-show="isExpanded">
                <button class="auth-btn" @click="toggleExpand">
                    <SvgIcon name="signup" class="icon"/>
                </button>
                <button class="auth-btn" @click="toggleExpand(), loginWithGoogle()">
                    <SvgIcon name="google" class="icon"/>
                </button>
                <button class="auth-btn" @click="toggleExpand">
                    <SvgIcon name="github" class="icon"/>
                </button>
            </div>
        </div>
    </div>
    
</template>

<style scoped>
@keyframes expandWrapper {
  0% {
    background-color: lightgray;
    height: 100px;
    box-shadow: none;
  }
  1% {
    background-color: #e0e0e0;
    height: 100px;
    box-shadow: none;
  }
  100% {
    background-color: #e0e0e0;
    height: 375px;
    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.4);
  }
}

@keyframes collapseWrapper {
  0% {
    height: 375px;
    background-color: #e0e0e0;
    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.4);
  }
  1% {
    background-color: #e0e0e0;
    box-shadow: none;
    height: 375px;
  }
  100% {
    height: 100px;
    background-color: transparent;
  }
}

.auth-zone {
    width: 100px;
    height: 100px;
    position: relative;
}

.auth-wrapper {
    position: absolute;
    display: flex;
    align-items: center;
    width: 100px; 
    height: 100px;
    border-radius: 50px; 
    cursor: pointer;
    overflow: hidden; 
    animation: collapseWrapper 0.4s ease-in-out forwards;
}

.auth-wrapper.expanded {
    animation: expandWrapper 0.4s ease-in-out forwards;
}

.auth-expand-toggler {
    position: absolute;
    top: 8px;
    left: 8px;

    background-color: #e0e0e0;
    border-radius: 50%;

    width: 85px;
    height: 85px;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 10;

    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.4);
    transition: 0.2s ease-in-out;
}

.auth-expand-toggler.expanded  {
    box-shadow: none;
    background-color: #bdbdbd;

}

.auth-expand-toggler.expanded .main-auth-icon {
    fill: #ececec;

}

.main-auth-icon {
    width: 75px;
    height: 75px;
    fill: black;
    transition: 0.2s ease-in-out;
}

.auth-expand-toggler:hover {
    background-color: #bdbdbd;
    transition: 0.2s ease-in-out;
}

.auth-expand-toggler:hover .main-auth-icon {
    fill: #ececec;
    transition: 0.2s ease-in-out;
}

.icon {
    width: 40px;
    height: 40px;
    fill: #333;
}

.content-side {
    display: flex;
    flex-direction: column;

    padding-left: 15px;
    padding-top: 90px;

    gap: 15px;
    transform: translateX(-20px);
    transition: all 0.4s ease;
    white-space: nowrap;
}

.expanded .content-side {
    transform: translateX(0);
}

.auth-btn {
    width: 75px;
    height: 75px;
    border-radius: 50%;
    border: none;
    background: white;
    cursor: pointer;
    transition: 0.4s;
}

.auth-btn:hover {
    transform: scale(1.05);
    background-color: darkgray;
    color: whitesmoke;
    transition:  0.4s;
}
</style>