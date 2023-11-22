<template>
    <div class="dashboard">
        <h1>Manager Dashboard</h1>
        <div class="card management-data">
            <div class="card-header text-start">
                Management Data
            </div>
            <div class="card-body">
                <h5 class="card-title text-start">Total Revenue(Month) <strong class="float-end">$ {{
                    managementData?.revenue
                }}</strong>
                </h5>
                <hr>
                <h5 class="card-title">Inventory Details</h5>
                <div class="row">
                    <div class="col">
                        <h6>Empty Section Details</h6>
                        <table class="table table-hover border-1 border">
                            <thead>
                                <tr>
                                    <th scope="col">#</th>
                                    <th scope="col">Name</th>
                                    <th scope="col">Unit</th>
                                    <!-- <th scope="col">Handle</th> -->
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="section in managementData?.sections" :key="section.id">
                                    <th scope="row">{{ section.id }}</th>
                                    <td>
                                        {{ section.name }}
                                    </td>
                                    <td>
                                        {{ section.unit }}
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="col">
                        <h6>Unavailable Product Details</h6>
                        <table class="table table-hover border-1 border">
                            <thead>
                                <tr>
                                    <th scope="col">#</th>
                                    <th scope="col">Name</th>
                                    <th scope="col">Section Name</th>
                                    <!-- <th scope="col">Handle</th> -->
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="product in managementData?.products" :key="product.id">
                                    <th scope="row">{{ product.id }}</th>
                                    <td>
                                        {{ product.name }}
                                    </td>
                                    <td>{{ product.section.name }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <!-- <a href="#" class="btn btn-primary">Go somewhere</a> -->
            </div>
        </div>
        <hr class="border border-dark border-2 rounded-circle opacity-50">
        <div class="row align-items-center border border-1 border-secondary m-4 rounded rounded-2 p-4">
            <div class="col">
                <h1>Download Zip File</h1>
                <p class="text-secondary p-0 m-0">Download Zip File containing csv files with engagement data</p>
            </div>
            <div class="col ">
                <button @click="downloadZipFile" class="btn btn-outline-secondary float-end">Download</button>
            </div>
        </div>

        <hr class="border border-dark border-2 rounded-circle opacity-50">
        <h3 class="">Various Engagement Graphs</h3>
        <div class="img-container">
            <div class="img-div">
                <img :src="boughtProductGraph" alt="Graph showing frequency at which products are bougth">
                <p>This Graph shows the frequency at which each product is bought by user</p>
            </div>
            <div>
                <img :src="couponGraph" alt="Graph showing frequency at which coupons are used">
                <p>This Graph shows the frequency at which each coupon is used by user</p>
            </div>
            <div>
                <img :src="favProductGraph" alt="Graph showing frequency at which products are wishlisted by users">
                <p>This Graph shows the frequency at which each product is wishlisted by user</p>
            </div>

        </div>
        <!-- <p>{{ managementData }}</p> -->
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
        const managementData = ref(null);
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

        const downloadZipFile = async () => {
            await reportMethods.downloadReportCSV();
        }
        return {
            couponGraph,
            boughtProductGraph,
            favProductGraph,
            managementData,
            downloadZipFile
        }
    }
}
</script>

<style scoped>
.dashboard {
    display: grid;
}

.card {
    justify-self: center;
    width: fit-content;
    margin: 5px;
}

.management-data {
    width: 80% !important;
}

.img-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
}
</style>