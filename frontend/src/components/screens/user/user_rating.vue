<template>
    <div>
        <h1>Product Ratings</h1>
        <div class="wrapper " v-if="ratings?.length > 0">
            <ProductRatingCard v-for="rating in ratings" :key="rating.id" :rating="rating"
                class="product-rating-card card" />
        </div>
        <div v-else>
            <h5>No Product Rating Found</h5>
        </div>
    </div>
</template>

<script>
import { productRatingMethods } from '@/services/HTTPRequests/productRatingMethods';
import { onMounted, ref } from 'vue';
import ProductRatingCard from "@/components/widgets/cards/product_rating_card.vue"
export default {
    name: "UserRatingPage",
    components: {
        ProductRatingCard
    },
    setup() {
        const ratings = ref();
        const fetchRatingsForUser = async () => {
            const response = await productRatingMethods.getAllRatingByUser();
            ratings.value = response;
        }

        onMounted(() => {
            fetchRatingsForUser();
        })
        return {
            ratings,
        }
    }
}
</script>

<style scoped>
.wrapper {
    margin: auto;
    background-color: #ffffff;
    /* box-shadow: 0px 14px 80px rgba(34, 35, 58, 0.2); */
    padding: 40px 55px 45px 55px;
    border-radius: 15px;
    transition: all .3s;
    display: flex;
    flex-wrap: wrap;
}

.product-rating-card {
    border: none;
    box-shadow: 3px 3px 5px rgba(34, 35, 58, 0.2);
    border-radius: 15px;
    transition: all .3s;
    flex: auto;
    max-width: 540px;
    margin: 10px;
}
</style>