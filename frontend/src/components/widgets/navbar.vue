<template>
    <nav class="navbar navbar-expand navbar-light fixed-top bg-body-tertiary">
        <div class="container-fluid">
            <RouterLink to="/" class="navbar-brand">
                <img src="@/assets/logo.png" alt="Bootstrap" width="30" height="24">
                Grocery Store
            </RouterLink>
            <div class="collapse navbar-collapse justify-content-end">
                <ul class="navbar-nav ml-auto">
                    <li class="nav-item">
                        <!-- <RouterLink to="/login" class="nav-link">Login</RouterLink> -->
                        <RouterLink to="/login" class="nav-link" v-if="$route.path === '/register'">Login</RouterLink>
                    </li>
                    <li class="nav-item">
                        <RouterLink to="/register" class="nav-link" v-if="$route.path === '/login'">Register
                        </RouterLink>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<script>
import { ref } from 'vue';
import { RouterLink, useRouter } from 'vue-router';

export default {
    // eslint-disable-next-line vue/multi-word-component-names
    name: 'Navbar',
    setup() {
        const router = useRouter();
        const routeName = ref(router.currentRoute.value.name);
        console.log(routeName);
        return {
            routeName
        };
    },
    components: { RouterLink }
}
</script>

<style scoped></style>