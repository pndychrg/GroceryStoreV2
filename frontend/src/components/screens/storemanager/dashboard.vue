<template>
    <div>
        <h1>Manager Dashboard</h1>
        <h3>Engagement Graphs</h3>
        <img :src="boughtProductGraph" alt="Product Bought Graph">
        
        <img :src="couponGraph" alt="Coupon Usage Graph">
        <!-- <p>{{ managementData }}</p> -->
    </div>
</template>

<script>
import { reportMethods } from '@/services/HTTPRequests/reportMethods';
import { onMounted, reactive, ref } from 'vue';
export default {
    name: "ManagerDashboard",
    setup() {
        const couponGraph = ref(null);
        const boughtProductGraph = ref(null);
        const favProductGraph = ref(null);
        const managementData = reactive({
            revenue: null,
            sections: null,
            products: null,
        });
        const fetchCouponGraph = async () => {
            const response = await reportMethods.getCouponGraph();
            couponGraph.value = URL.createObjectURL(response);
        }
        const fetchFavProductGraph = async () => {
            const response = await reportMethods.getFavProductGraph()
            favProductGraph.value = URL.createObjectURL(response);
        }
        const fetchBoughtProductGraph = async () => {
            const response = await reportMethods.getBoughtProductGraph();
            boughtProductGraph.value = URL.createObjectURL(response);
        }
        const fetchManagementData = async () => {
            const response = await reportMethods.getManagementData();
            managementData.value = response;
            console.log(managementData.value);
        }
        onMounted(async () => {
            // await reportMethods.downloadReportCSV()
            fetchCouponGraph();
            fetchFavProductGraph();
            fetchBoughtProductGraph();
            fetchManagementData();
        })

        return {
            couponGraph,
            boughtProductGraph,
            favProductGraph,
            managementData
        }
    }
}
</script>

<style scoped></style>