<template>
    <div class="" style="justify-self: center; width: 80%;">
        <div class="card user-details mb-4">
            <!-- User Details -->
            <div class="d-flex pt-2" style="justify-content: center;">
                <div v-if="image != null" class="img-container">
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
            <div>
                <button class="btn btn-danger mb-2 float-start" style="width: 20%;" @click="showUpdatePasswordForm">
                    Update Password
                </button>
                <button class="float-end btn btn-outline-dark mb-2" @click="showProfileUpdateForm" style="width: 30%;"
                    id="updateProfileButton">Update Profile
                    <font-awesome-icon icon="fa-solid fa-edit" class="faa-horizontal animated-hover " /></button>
                <button class="float-end me-2 btn btn-outline-dark mb-2" @click="downloadMonthlyReportPDF"
                    style="width: 30%;">Monthly
                    Report
                    <font-awesome-icon icon="fa-solid fa-download" class="faa-horizontal animated-hover " /></button>
            </div>
        </div>
        <div class="row " style="justify-content: center;">
            <div class="col-md-6 p-4 favproduct-col" v-if="favProducts.length > 0">
                <h2>Favourite Products</h2>
                <div v-for="product in favProducts" :key="product.id" class="card product-card">
                    <ProductCard :productData="product" loggedInRole="user"
                        @add-to-favourite="removeProductsFromFavourites" />
                </div>
            </div>
            <div class="col-md-6 p-4" v-if="bills.length > 0">
                <h2>Bills for User </h2>
                <h5>Total Expense ₹ {{ totalExpenditure }}</h5>
                <div v-for="bill in bills" :key="bill.id" class="bill-card card">
                    <BillCard :bill="bill" @show-billDetails="showBillDetails" />
                </div>
            </div>
        </div>
        <teleport to="#modal-root">
            <BillDetailsModal v-show="isBillDetailModalOpen" :bill="selectedBill" @close="showBillDetails" />
            <UserProfileUpdateForm v-show="isProfileUpdateFormShown" @close="showProfileUpdateForm" />
            <UpdatePasswordFormShown v-show="isUpdatePasswordFormShown" @close="showUpdatePasswordForm" />
        </teleport>
    </div>
</template>

<script>
import { buyMethods } from '@/services/HTTPRequests/buyMethods';
import { favouriteMethods } from '@/services/HTTPRequests/favouriteMethods';
import { onMounted, ref, computed } from 'vue';
import BillCard from '@/components/widgets/cards/bill_card.vue'
import ProductCard from '@/components/widgets/cards/product_card.vue';
import BillDetailsModal from '@/components/widgets/bill_details.vue'
import { UIStateStore } from '@/services/uiStateManager';
import { userStateStore } from '@/services/stateManager';
import { reportMethods } from '@/services/HTTPRequests/reportMethods';
import UserProfileUpdateForm from "@/components/widgets/forms/profile_update.vue"
import UpdatePasswordFormShown from "@/components/widgets/forms/update_password.vue"

export default {
    name: "UserDashboard",
    components: {
        BillCard,
        ProductCard,
        UserProfileUpdateForm,
        BillDetailsModal,
        UpdatePasswordFormShown,
    },
    setup() {
        const store = userStateStore();
        const user = computed(() => {
            return store.user;
        });
        const image = computed(() => {
            return store.profile_img
        });
        const uiStateManager = UIStateStore();
        // const user = userStateStore.user;
        const bills = ref([]);
        const favProducts = ref([]);
        const uiStore = UIStateStore()
        const fetchAllBills = async () => {
            const response = await buyMethods.getAllBills()
            bills.value = response;
        }
        const totalExpenditure = computed(() => {
            let totalExpense = 0;
            // for loop in bills
            bills.value.forEach((bill) => totalExpense += bill.finalAmount);
            return totalExpense
        })
        const fetchAllFavouriteProducts = async () => {
            const response = await favouriteMethods.fetchAllFavouriteForUser();

            favProducts.value = response;
        }
        const isBillDetailModalOpen = ref(false);
        const selectedBill = ref({});
        const showBillDetails = (bill) => {
            uiStore.toggleModal();
            isBillDetailModalOpen.value = !isBillDetailModalOpen.value;
            selectedBill.value = isBillDetailModalOpen.value ? bill : {};
        }
        const downloadMonthlyReportPDF = async () => {
            await reportMethods.downloadPDFReport();
        }


        onMounted(async () => {
            await fetchAllBills();
            await store.getUserImage();
            await fetchAllFavouriteProducts();
            // testing
            // document.getElementById("updateProfileButton").click()
        })

        // Profile update methods
        const isProfileUpdateFormShown = ref(false);
        const showProfileUpdateForm = () => {
            isProfileUpdateFormShown.value = !isProfileUpdateFormShown.value
            uiStateManager.toggleModal();
        }

        //removing products from favourites
        const removeProductsFromFavourites = async (product) => {
            await favouriteMethods.removeFromFavourite(product.id)
            await fetchAllFavouriteProducts();
        }

        // updating password setup

        const isUpdatePasswordFormShown = ref(false);
        const showUpdatePasswordForm = () => {
            isUpdatePasswordFormShown.value = !isUpdatePasswordFormShown.value
            uiStateManager.toggleModal();
        }
        return {
            bills,
            favProducts,
            isBillDetailModalOpen,
            showBillDetails,
            selectedBill,
            user,
            totalExpenditure,
            downloadMonthlyReportPDF,
            showProfileUpdateForm,
            isProfileUpdateFormShown,
            image,
            removeProductsFromFavourites,
            isUpdatePasswordFormShown,
            showUpdatePasswordForm,
        }
    }
}
</script>

<style scoped>
.bills-container {
    display: flex;
    flex-wrap: wrap;
    flex-direction: column;
    background-color: #f9f9f9;
}

.bill-card {
    border: none;
    flex-grow: 1;
    box-shadow: rgba(0, 0, 0, 0.15) 1.95px 1.95px 2.6px;
    margin: 10px;
    width: 100%;
    box-shadow: 0 6px 10px rgba(0, 0, 0, .08), 0 0 6px rgba(0, 0, 0, .05);
    transition: .3s transform cubic-bezier(.155, 1.105, .295, 1.12), .3s box-shadow, .3s -webkit-transform cubic-bezier(.155, 1.105, .295, 1.12);
    cursor: pointer;
}

.product-card {
    /* width: 180rem; */
    max-width: 540px;
    margin: 10px;
    border: none;
    background: #fff;
    box-shadow: 0 6px 10px rgba(0, 0, 0, .08), 0 0 6px rgba(0, 0, 0, .05);
    transition: .3s transform cubic-bezier(.155, 1.105, .295, 1.12), .3s box-shadow, .3s -webkit-transform cubic-bezier(.155, 1.105, .295, 1.12);
    cursor: pointer;
}

.product-card-unavailable {
    box-shadow: 0 6px 10px rgba(255, 0, 0, .10), 0 0 6px rgba(255, 0, 0, .15) !important;
}

.product-card-unavailable:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 20px rgba(255, 0, 0, .12), 0 4px 8px rgba(255, 0, 0, .06) !important;
}

.product-card:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 20px rgba(0, 0, 0, .12), 0 4px 8px rgba(0, 0, 0, .06);
}

.bill-card:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 20px rgba(0, 0, 0, .12), 0 4px 8px rgba(0, 0, 0, .06);
}

.favproduct-col {
    display: grid;
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

.img-container {
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

.user-details {
    padding: 20px;
    border: none;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    background-color: #D8E7F7;
}

.user-details h1 {
    color: #001F3F;
}

.user-details h5 {
    color: #333333
}
</style>