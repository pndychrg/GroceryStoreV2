<template>
    <form @submit.prevent="rateProduct">
        <div class="star-rating">
            <span v-for="index in 5" :key="index" @click="rate(index)"
                :class="{ 'filled': index <= currentRating, 'empty': index > currentRating }">
                ★
            </span>
        </div>
        <div class="mt-2">
            <textarea class="form-control" placeholder="Leave a comment here" id="floatingTextarea"
                v-model="comment"></textarea>
        </div>
        <div class="d-grid gap-2 mt-2">
            <button class="btn btn-outline-primary" type="submit">Submit</button>
        </div>
    </form>
</template>

<script>
import { ref, watch } from 'vue';
import { productRatingMethods } from '@/services/HTTPRequests/productRatingMethods';
export default {
    name: "RateProduct",
    props: {
        product_id: Number,
        initialData: Object,
    },
    setup(props) {

        const currentRating = ref(0);
        const comment = ref(null);
        const rate = (index) => {
            currentRating.value = index;
            // emit('rated', index);
        }

        const rateProduct = async () => {
            const response = await productRatingMethods.rateProduct(props.product_id, currentRating.value, comment.value);
            console.log(response);
        }

        //watcher for initialData for prefilling the form
        watch(() => props.initialData, (newData) => {
            if (newData) {
                currentRating.value = newData.rating;
                comment.value = newData.comment;
            }
        });


        return {
            currentRating,
            rate,
            comment,
            rateProduct
        }
    }
}
</script>

<style scoped>
.star-rating {
    display: inline-block;
    font-size: 32px;
    cursor: pointer;
}

.filled {
    color: orange;
}

.empty {
    color: gray;
}
</style>