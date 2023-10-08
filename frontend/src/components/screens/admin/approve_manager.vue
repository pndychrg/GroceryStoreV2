<template>
    <div>
        <h3>Approve Manager</h3>
        <div class="managers-wrapper row m-2 " v-if="unapprovedManagers?.length > 0">
            <div v-for="manager in unapprovedManagers" :key="manager.id" class="managerCard card">
                <ManagerCard :managerData="manager" @approved="handleApproval(manager.id)"
                    @rejected="handleRejection(manager.id)" />
            </div>
        </div>
        <div v-else>
            No manager requested
        </div>
    </div>
</template>

<script>

import { unapprovedManagersMethods } from '@/services/HTTPRequests/unApproved';
import { onMounted, ref } from 'vue';
import ManagerCard from "@/components/widgets/cards/manager_card.vue"
export default {
    name: "ApproveManager",
    components: {
        ManagerCard,
    },
    setup() {

        const unapprovedManagers = ref([]);

        const fetchUnapprovedManagers = async () => {
            try {
                unapprovedManagers.value = await unapprovedManagersMethods.fetchAllUnapprovedManagers()
            } catch (e) {
                console.error("Error fetching managers")
            }
        }

        const handleApproval = async (manager_id) => {
            const response = await unapprovedManagersMethods.approveManager(manager_id);
            // if manager is approved then remove it from frontend list
            unapprovedManagers.value = unapprovedManagers.value.filter(manager => manager.id != manager_id)
            console.log(response);

        }

        const handleRejection = async (manager_id) => {
            const response = await unapprovedManagersMethods.rejectManager(manager_id);
            // TODO remove manager if deleted
            unapprovedManagers.value = unapprovedManagers.value.filter(manager => manager.id != manager_id)
            console.log(response);
        }

        onMounted(() => {
            fetchUnapprovedManagers();
        })

        return {
            unapprovedManagers,
            handleApproval,
            handleRejection
        }
    },
}
</script>

<style scoped>
.managers-wrapper {
    margin: auto;
    background-color: #ffffff;
    /* box-shadow: 0px 14px 80px rgba(34, 35, 58, 0.2); */
    padding: 40px 55px 45px 55px;
    border-radius: 15px;
    transition: all .3s;

}

.managerCard {
    border: none;
    box-shadow: 3px 3px 5px rgba(34, 35, 58, 0.2);
    border-radius: 15px;
    transition: all .3s;
    width: 18rem;
    margin: 10px;
}
</style>