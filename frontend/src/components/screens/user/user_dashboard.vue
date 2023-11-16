<template>
    <div>
        <div class="card user-details bg-body-secondary">
            <!-- User Details -->
            <div class="card-body">
                <h1>{{ user.name }}</h1>
                <h4 class="text-secondary">{{ user.username }}</h4>
            </div>
        </div>
        <div class="row">
            <div class="col p-4 favproduct-col">
                <h2>Favourite Products</h2>
                <div v-for="product in favProducts" :key="product.id" class="card product-card">
                    <ProductCard :productData="product" />
                </div>
            </div>
            <div class="col p-4">
                <h2>Bills for User</h2>
                <div v-for="bill in bills" :key="bill.id" class="bill-card card">
                    <BillCard :bill="bill" @show-billDetails="showBillDetails" />
                </div>
            </div>
        </div>
        <teleport to="#modal-root">
            <BillDetailsModal v-show="isBillDetailModalOpen" :bill="selectedBill" @close="showBillDetails" />
        </teleport>
    </div>
</template>

<script>
import { buyMethods } from '@/services/HTTPRequests/buyMethods';
import { favouriteMethods } from '@/services/HTTPRequests/favouriteMethods';
import { onMounted, ref } from 'vue';
import BillCard from '@/components/widgets/cards/bill_card.vue'
import ProductCard from '@/components/widgets/cards/product_card.vue';
import BillDetailsModal from '@/components/widgets/bill_details.vue'
import { UIStateStore } from '@/services/uiStateManager';
import { userStateStore } from '@/services/stateManager';
export default {
    name: "UserDashboard",
    components: {
        BillCard,
        ProductCard,
        BillDetailsModal,
    },
    setup() {
        const user = userStateStore().user;
        // const user = userStateStore.user;
        const bills = ref([]);
        const favProducts = ref([]);
        const uiStore = UIStateStore()
        const fetchAllBills = async () => {
            const response = await buyMethods.getAllBills()
            bills.value = response;
        }

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

        onMounted(() => {
            fetchAllBills();
            fetchAllFavouriteProducts();
        })

        return {
            bills,
            favProducts,
            isBillDetailModalOpen,
            showBillDetails,
            selectedBill,
            user
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
</style>