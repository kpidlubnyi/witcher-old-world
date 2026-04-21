<script setup>
defineProps(['data'])

function pretifyDate(timestamp) {
    const date = new Date(Number(timestamp) * 1000)
    return date.toLocaleString()
}
</script>


<template>
<div class="card-container">
    <h2>{{ data.name }}</h2>
    <h4>created by {{ data.host_id }} at {{ pretifyDate(data.created_at) }}</h4>
</div>
</template>


<style>
.card-container {
    width: 300px;
    height: 100px;
    background-color: lightgray;
    border-radius: 10px;
}
</style>