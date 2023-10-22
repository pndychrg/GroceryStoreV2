<template>
    <div>
        <h2>User Dashboard</h2>
        <div class="bills-container">
            <div v-for="bill in bills" :key="bill.id" class="bill-card card">
                <BillCard :bill="bill" />
            </div>
        </div>
    </div>
</template>

<script>
import { buyMethods } from '@/services/HTTPRequests/buyMethods';
import { onMounted, ref } from 'vue';
import BillCard from '@/components/widgets/cards/bill_card.vue'
export default {
    name: "UserDashboard",
    components: {
        BillCard,
    },
    setup() {
        const bills = ref([]);

        const fetchAllBills = async () => {
            const response = await buyMethods.getAllBills()
            bills.value = response;
        }

        onMounted(() => {
            fetchAllBills();
        })

        return {
            bills
        }
    }
}
</script>

<style scoped>
.bills-container {
    display: flex;
    flex-wrap: wrap;
    background-color: #f9f9f9;
}

.bill-card {
    border: none;
    flex-grow: 1;
    box-shadow: rgba(0, 0, 0, 0.15) 1.95px 1.95px 2.6px;
    margin: 10px;
}
</style>