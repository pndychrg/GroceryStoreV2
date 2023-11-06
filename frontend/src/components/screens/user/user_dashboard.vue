<template>
    <div>
        <h2>User Dashboard</h2>
        <div class="bills-container">
            <div v-for="bill in bills" :key="bill.id" class="bill-card card">
                <BillCard :bill="bill" />
            </div>

            <div v-for="product in favProducts" :key="product.id" class="card">
                <ProductCard :productData="product" />
            </div>
        </div>
    </div>
</template>

<script>
import { buyMethods } from '@/services/HTTPRequests/buyMethods';
import { favouriteMethods } from '@/services/HTTPRequests/favouriteMethods';
import { onMounted, ref } from 'vue';
import BillCard from '@/components/widgets/cards/bill_card.vue'
import ProductCard from '@/components/widgets/cards/product_card.vue';
export default {
    name: "UserDashboard",
    components: {
        BillCard,
        ProductCard,
    },
    setup() {
        const bills = ref([]);
        const favProducts = ref([]);
        const fetchAllBills = async () => {
            const response = await buyMethods.getAllBills()
            bills.value = response;
        }

        const fetchAllFavouriteProducts = async () => {
            const response = await favouriteMethods.fetchAllFavouriteForUser();

            favProducts.value = response;
        }

        onMounted(() => {
            fetchAllBills();
            fetchAllFavouriteProducts();
        })

        return {
            bills,
            favProducts
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