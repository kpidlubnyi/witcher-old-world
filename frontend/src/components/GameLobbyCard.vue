<script setup>
defineProps(['data'])
</script>


<template>
<div class="card-container">
    <h2>{{ data.name }}</h2>
    <h3>created by {{ data.host_name }} </h3>
    <h4>{{ data.created_ago }}</h4>
</div>
</template>


<style>
.card-container {
    width: 300px;
    height: 120px;
    background-color: lightgray;
    border-radius: 10px;
}
</style>