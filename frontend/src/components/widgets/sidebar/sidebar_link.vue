<template>
    <div class="sidebar-link ">
        <RouterLink :to="route" class="btn d-flex" @click="$emit('close')">
            <font-awesome-icon class="faa-horizontal animated-hover mt-1 me-2" :icon="icon" :style="{ color: color }" />
            <!-- {{ color }} -->
            <h5>{{ tag }}</h5>
        </RouterLink>
    </div>
</template>

<script>
import { RouterLink } from 'vue-router';

export default {
    name: "SidebarLink",
    props: {
        tag: String,
        icon: String,
        route: String,
        color: String
    },
    components: { RouterLink }
}
</script>

<style scoped>
.btn {
    color: white;
    /* width: 80%; */
    width: 100%;
}
</style>