<template>
    <div>
        <AdminDashboard v-if="loggedInRole == 'admin'" />
        <UserHome v-else-if="loggedInRole == 'user'" />
        <ManagerDashboard v-if="loggedInRole == 'manager'" />
    </div>
</template>

<script>
import AdminDashboard from '@/components/screens/admin/admin_dashboard.vue'
import UserHome from '@/components/screens/user/user_home.vue'
import ManagerDashboard from '@/components/screens/storemanager/dashboard.vue'
import { userStateStore } from '@/services/stateManager';
import { computed } from 'vue';
export default {
    name: 'HomeComponent',
    components: {
        AdminDashboard,
        UserHome,
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

<style scoped></style>