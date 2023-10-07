<template>
    <nav class="navbar navbar-expand fixed-top">
        <div class="container-fluid">
            <button v-if="isAuthenticated" @click="showSidebar" id="sidebarButton" class="btn ">
                <font-awesome-icon :icon="['fas', 'bars']" class="faa-bounce animated-hover" />
            </button>
            <RouterLink to="/" class="navbar-brand">
                <img src="@/assets/logo.png" alt="Bootstrap" width="30" height="24">
                Grocery Store
            </RouterLink>
            <div class="collapse navbar-collapse justify-content-end">
                <ul class="navbar-nav ml-auto" v-if="!isAuthenticated">
                    <li class="nav-item">
                        <RouterLink to="/login" class="nav-link" v-if="$route.path === '/register'">Login</RouterLink>
                    </li>
                    <li class="nav-item">
                        <RouterLink to="/register" class="nav-link" v-if="$route.path === '/login'">Register
                        </RouterLink>
                    </li>
                </ul>
                <ul class="navbar-nav ml-auto" v-if="isAuthenticated">
                    <div class="row" v-if="isNotApproved">
                        <li class="nav-item">
                            <button @click="logoutMethod" class="nav-link">
                                <font-awesome-icon :icon="['fas', 'arrow-right-from-bracket']"
                                    class="faa-horizontal animated-hover" />
                            </button>
                        </li>
                    </div>
                    <div class="row" v-else>
                        <li class="nav-item col">
                            <RouterLink :to='dashboardLink' class="btn btn-dark profile-button">
                                <font-awesome-icon :icon="['fas', 'user']" class="faa-horizontal animated-hover" />
                            </RouterLink>
                        </li>
                        <li class="nav-item col">
                            <button @click="logoutMethod" class="nav-link">
                                <font-awesome-icon :icon="['fas', 'arrow-right-from-bracket']"
                                    class="faa-horizontal animated-hover" />
                            </button>
                        </li>
                    </div>
                </ul>
            </div>
        </div>
    </nav>
    <teleport to="#modal-root">
        <Sidebar v-show="isSidebarShown" @close="showSidebar" />
    </teleport>
</template>

<script>
import { ref, computed } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import { userStateStore } from '@/services/stateManager';
import Sidebar from '@/components/widgets/sidebar/sidebar.vue'
export default {
    // eslint-disable-next-line vue/multi-word-component-names
    name: 'Navbar',
    components: { RouterLink, Sidebar },
    setup() {
        const store = userStateStore();
        const router = useRouter();
        const routeName = ref(router.currentRoute.value.name);
        // Use a computed property for isAuthenticated
        const isAuthenticated = computed(() => store.isAuthenticated);
        const isNotApproved = computed(() => {
            // checking if the roles is "notApproved"
            if (store.user.role == "notApproved") {
                return true;
            } else {
                return false;
            }
        })
        const logoutMethod = store.logoutUser;
        // calculating the dashboard link according to user role
        const dashboardLink = computed(() => {
            return '/' + store.user.role + '/dashboard'
        });


        //sidebar setup
        const isSidebarShown = ref(false);
        const showSidebar = () => {
            isSidebarShown.value = !isSidebarShown.value
        }

        return {
            routeName,
            isAuthenticated,
            logoutMethod,
            dashboardLink,
            isNotApproved,
            isSidebarShown,
            showSidebar
        };
    },
}
</script>

<style scoped>
.profile-button {
    margin-right: 10px;
    border-radius: 30px;
    padding-left: 20px;
    padding-right: 20px;
    background-color: #393737;
}
</style>