<template>
    <div>
        <h1>Manager Dashboard</h1>
        <img :src="couponGraph" alt="Coupon Usage Graph">
    </div>
</template>

<script>
import { reportMethods } from '@/services/HTTPRequests/reportMethods';
import { onMounted, ref } from 'vue';
export default {
    name: "ManagerDashboard",
    setup() {
        const couponGraph = ref(null);
        const boughtProductGraph = ref(null);
        const favProductGraph = ref(null);
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
        // const fetchMonthRevenue = async () => {
        //     const response = await
        // }

        onMounted(async () => {
            // await reportMethods.downloadReportCSV()
            fetchCouponGraph();
            fetchFavProductGraph();
            fetchBoughtProductGraph();
        })

        return {
            couponGraph,
            boughtProductGraph,
            favProductGraph
        }
    }
}
</script>

<style scoped></style>