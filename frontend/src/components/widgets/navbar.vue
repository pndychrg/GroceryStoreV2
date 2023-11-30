<template>
    <nav class="navbar navbar-expand sticky-top  bg-body-secondary">
        <div class=" container-fluid">
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
                            <!-- Cart Button -->
                            <button class="btn btn-outline-dark" type="button" @click="showCart"
                                v-if="loggedInRole == 'user'" style="width: max-content;">
                                <font-awesome-icon :icon="['fas', 'fa-cart-plus']" class="faa-horizontal animated-hover" />
                                Show Cart
                            </button>
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
        <CartModal v-if="isCartShown" @close="showCart" />
    </teleport>
</template>

<script>
import { ref, computed } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import { userStateStore } from '@/services/stateManager';
import { UIStateStore } from '@/services/uiStateManager';
import Sidebar from '@/components/widgets/sidebar/sidebar.vue'
import CartModal from '@/components/widgets/cart.vue';
export default {
    // eslint-disable-next-line vue/multi-word-component-names
    name: 'Navbar',
    components: { RouterLink, Sidebar, CartModal },
    setup() {
        const store = userStateStore();
        const UIStore = UIStateStore();
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
        const loggedInRole = computed(() => {
            return store.user.role;
        })
        const logoutMethod = store.logoutUser;

        //sidebar setup
        const isSidebarShown = ref(false);
        const showSidebar = () => {
            UIStore.toggleModal()
            isSidebarShown.value = !isSidebarShown.value
        }

        // cart setup
        const isCartShown = ref(false);
        const showCart = () => {
            UIStore.toggleModal();
            isCartShown.value = !isCartShown.value;
        }
        return {
            routeName,
            isAuthenticated,
            logoutMethod,
            isNotApproved,
            isSidebarShown,
            showSidebar,
            isCartShown,
            showCart,
            loggedInRole
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