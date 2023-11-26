<template>
    <div class="dashboard">
        <h1>Manager Dashboard</h1>
        <div class="card user-details bg-body-secondary" style="width: 80%; !important">
            <!-- User Details -->
            <div class="d-flex pt-2" style="justify-content: center;">
                <div v-if="image != null" class="profile-img-container">
                    <img v-if="image != null" :src="'data:image/png;base64,' + image" class="image img-thumbnail  me-2">
                </div>
                <div class="card-body  profile-data">
                    <div class="text-center">
                        <!-- <p>{{ image }}</p> -->
                        <h1>
                            {{ user.name }}
                        </h1>
                        <h5 class="text-secondary text-center">
                            Username : @{{ user.username }}
                            <br>
                            Email : {{ user.email }}
                        </h5>
                        <!-- <h5 class="text-secondary"></h5> -->
                    </div>
                </div>
            </div>
            <hr>
            <div class="row m-2">
                <div class="col-md-6">
                    <button class="btn btn-outline-dark mb-2" @click="showProfileUpdateForm" style="width: 100%;"
                        id="updateProfileButton">Update Profile
                        <font-awesome-icon icon="fa-solid fa-edit" class="faa-horizontal animated-hover " /></button>
                </div>
                <div class="col-md-6 ">
                    <button class="btn btn-outline-dark mb-2" @click="downloadMonthlyReportPDF" style="width: 100%;">Monthly
                        Report
                        <font-awesome-icon icon="fa-solid fa-download" class="faa-horizontal animated-hover " /></button>
                </div>
            </div>
        </div>
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
        <teleport to="#modal-root">
            <UserProfileUpdateForm v-show="isProfileUpdateForm" @close="showProfileUpdateForm" />
        </teleport>
        <!-- <p>{{ managementData }}</p> -->
    </div>
</template>

<script>
import { userStateStore } from '@/services/stateManager';
import { reportMethods } from '@/services/HTTPRequests/reportMethods';
import { onMounted, ref, computed } from 'vue';
import UserProfileUpdateForm from "@/components/widgets/forms/profile_update.vue"
import { UIStateStore } from '@/services/uiStateManager';
export default {
    name: "ManagerDashboard",
    components: {
        // eslint-disable-next-line vue/no-unused-components
        UserProfileUpdateForm
    },
    setup() {
        const store = userStateStore();
        const uiStateStore = UIStateStore();
        const user = computed(() => {
            return store.user;
        })
        const image = computed(() => {
            return store.profile_img
        })
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

            await store.getUserImage();
            console.log("User Image updated")
        })

        const downloadZipFile = async () => {
            await reportMethods.downloadReportCSV();
        }

        // update user profile update form
        const isProfileUpdateForm = ref(false);
        const showProfileUpdateForm = () => {
            isProfileUpdateForm.value = !isProfileUpdateForm.value
            uiStateStore.toggleModal();
        }
        return {
            couponGraph,
            boughtProductGraph,
            favProductGraph,
            managementData,
            downloadZipFile,
            user,
            showProfileUpdateForm,
            isProfileUpdateForm,
            image,
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


.profile-data {
    /* display: flex;
    flex-direction: column;
    align-items: center;
    width: max-content; */
    flex-grow: 0;
    /* font-size: 10dvw; */
}

.profile-img-container {
    flex-shrink: 0;
    width: 20%;
}

/* Adjust the width for smaller screens */
@media only screen and (max-width:768px) {
    .img-container {
        width: 40%;
    }

    .profile-data h1,
    h5 {
        font-size: 80%;
    }
}

.image {
    width: auto;
    height: auto;
    max-width: 100%;
    max-height: 100%;
}
</style>