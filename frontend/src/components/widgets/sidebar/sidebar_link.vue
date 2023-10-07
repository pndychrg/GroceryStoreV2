<template>
    <div class="sidebar-link">
        <RouterLink :to="route" class="btn" @click="$emit('close')">
            <font-awesome-icon :icon="['fas', icon]" class="faa-horizontal animated-hover" />
            {{ tag }}
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
        route: String
    },
    components: { RouterLink }
}
</script>

<style scoped></style>