<template>
    <div class="row g-0">
        <div class="col-md-4 align-self-center">
            <img v-if="productData.img != null" :src="imageData" class="rounded-start card-img image img-fluid "
                alt="Base64 Image">
            <img v-else src="@/assets/img_notavailable.jpeg" alt="" class="rounded-start card-img  img-fluid"
                aria-hidden="true">
        </div>
        <!-- <img src="..." class="card-img-top" alt="..."> -->
        <div class="col-md-8 p-2">
            <div class="card-body text-start">
                <h5 class="card-title">
                    <span>
                        {{ productData.name }}
                    </span>
                    <span class="float-end" v-if="loggedInRole === 'manager'">
                        <button class="btn" @click="$emit('show-addimagemodal')">
                            <font-awesome-icon :icon="['fas', 'image']" class="faa-horizontal animated-hover"
                                style="color: #4D6DE3;" />
                        </button>
                    </span>
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
                    <br>
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
                <div v-else class="d-flex justify-content-end ">
                    <form @submit.prevent="$emit('add-to-cart', cartForm)" class="row end-0"
                        v-if="productData.availableAmount > 0">
                        <input type="number" v-model="cartForm.numOfProduct" class="form-control mb-2 col" required
                            :max="productData.availableAmount" min="1">
                        <button class="btn col-auto" type="submit">
                            <font-awesome-icon :icon="['fas', 'fa-cart-plus']" class="faa-horizontal animated-hover"
                                style="color: #4D6DE3;" />
                        </button>
                    </form>
                    <button v-else disabled class="btn btn-danger">Unavailable </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { reactive, watch, computed } from 'vue';
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
            cartForm.numOfProduct = newCartData?.numOfProduct ?? null;
        });

        const imageData = computed(
            () => {
                return `data:image/png;base64,${props.productData.img}`
            }
        )

        return {
            cartForm,
            imageData
        }
    }
}
</script>

<style scoped>
.modal {
    display: block;
    position: fixed;
    /* Stay in place */
    z-index: 1;
    /* Sit on top */
    left: 0;
    top: 0;
    width: 100%;
    /* Full width */
    height: 100%;
    /* Full height */
    overflow: auto;
    /* Enable scroll if needed */
    background-color: rgb(0, 0, 0);
    /* Fallback color */
    background-color: rgba(0, 0, 0, 0.4);
    /* Black w/ opacity */
}

.modal-content {
    background-color: #fefefe;
    margin: 15% auto;
    /* 15% from the top and centered */
    padding: 20px;
    border: 1px solid #888;
    width: max-content;
    /* Could be more or less, depending on screen size */

}

.image {
    height: 80%;
    width: auto;
}

.placeholder {
    height: 100%;
}
</style>