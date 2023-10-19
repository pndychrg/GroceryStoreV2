<template>
    <div class="section-card">
        <div class="card-body text-start">
            <h5 class="card-title">
                {{ productData.name }}
            </h5>
            <h6 class="card-subtitle">
                {{ productData.section.name }}
            </h6>
            <hr>
            <p class="card-text">
                Available Amount : {{ productData.availableAmount }}
                <br>
                Rate : {{ productData.rate }}
                <br>
                Manufacture Date : {{ productData.manufactureDate }}
                <br>
                Expiry Date : {{
                    productData.expiryDate }}
            </p>
            <div class="d-flex justify-content-end" v-if="loggedInRole == 'manager'">
                <button class="btn" @click="$emit('delete-product')">
                    <font-awesome-icon :icon="['fas', 'trash-can']" class="faa-horizontal animated-hover"
                        style="color: #c01c28;" />
                </button>
                <button class="btn" @click="$emit('edit-product')">
                    <font-awesome-icon :icon="['fas', 'pen-to-square']" class="faa-horizontal animated-hover" />
                </button>

            </div>
            <div v-else class="d-flex justify-content-end">
                <form @submit.prevent="$emit('add-to-cart', cartForm)" class="row">
                    <input type="number" v-model="cartForm.numOfProduct" class="form-control mb-2 col" required
                        :max="productData.availableAmount" min="1">
                    <button class="btn col-auto" type="submit">
                        <font-awesome-icon :icon="['fas', 'fa-cart-plus']" class="faa-horizontal animated-hover"
                            style="color: #4D6DE3;" />
                    </button>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import { reactive, watch } from 'vue';
export default {
    name: "ProductCard",
    props: {
        productData: Object,
        loggedInRole: String,
        cartData: Object,
    },
    setup(props) {

        const cartForm = reactive({
            product_id: props.productData.id,
            numOfProduct: null
        });

        watch(() => props.cartData, (newCartData) => {
            if (newCartData) {
                cartForm.numOfProduct = newCartData.numOfProduct
            }
        });

        return {
            cartForm,
        }
    }
}
</script>

<style scoped></style>