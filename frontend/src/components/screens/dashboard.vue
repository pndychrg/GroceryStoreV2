<template>
    <div class="dashboard">
        <AdminDashboard v-if="loggedInRole == 'admin'" />
        <UserDashboard v-else-if="loggedInRole == 'user'" />
        <ManagerDashboard v-else-if="loggedInRole == 'manager'" />
    </div>
</template>

<script>
import AdminDashboard from '@/components/screens/admin/admin_dashboard.vue'
import UserDashboard from '@/components/screens/user/user_dashboard.vue'
import ManagerDashboard from '@/components/screens/storemanager/dashboard.vue'
import { userStateStore } from '@/services/stateManager';
import { computed } from 'vue';
export default {
    // eslint-disable-next-line vue/multi-word-component-names
    name: "Dashboard",
    components: {
        AdminDashboard,
        UserDashboard,
        ManagerDashboard,
    },
    setup() {
        const store = userStateStore()

        const loggedInRole = computed(
            () => {
                return store.user?.role;
            }
        )
        return {
            loggedInRole,
        }
    }
}
</script>

<style scoped>
.dashboard {
    background-color: white;
    display: grid;
}
</style>