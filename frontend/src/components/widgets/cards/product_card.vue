<template>
    <div class="row g-0  ">
        <div class="col-md-4 align-self-center">
            <img v-if="productData.img != null" :src="imageData" class="rounded-start card-img image img-fluid "
                alt="Base64 Image">
            <img v-else src="@/assets/img_notavailable.jpeg" alt="" class="rounded-start card-img  img-fluid"
                aria-hidden="true">
        </div>
        <div class="col-md-8 p-2">
            <div class="card-body text-start">
                <h5 class="card-title">
                    <span>
                        {{ productData.name }}
                    </span>
                    <span class="float-end" v-if="loggedInRole === 'manager'">
                        <button class="btn btn-outline-primary img-btn" @click="$emit('show-addimagemodal')">
                            <font-awesome-icon :icon="['fas', 'image']" class="faa-horizontal animated-hover " />
                        </button>
                    </span>
                    <span class="float-end" v-if="loggedInRole === 'user'">
                        <button class="btn" @click="$emit('add-to-favourite', productData)">
                            <font-awesome-icon :icon="['fas', 'heart']" class="faa-horizontal animated-hover"
                                style="color: #FF5733 ;" />
                        </button>
                    </span>
                </h5>
                <h6 class="card-subtitle">
                    {{ productData.section.name }}
                </h6>
                <hr>
                <p class="text-secondary" v-if="productData.description?.length > 0">
                    {{ productData.description }}
                </p>
                <hr v-if="productData.description?.length > 0">
                <p class="card-text">
                    Available Amount : <span v-if="productData.availableAmount > 0">
                        {{ productData.availableAmount }} {{ productData.section.unit }}
                    </span>
                    <span v-else>
                        <button disabled class="btn btn-sm btn-danger">Unavailable</button>
                    </span>
                    <br>
                    Rate : ₹ {{ productData.rate }}/{{ productData.section.unit }}
                    <br>
                    Manufacture Date : {{ productData.manufactureDate ?? "None" }}
                    <br>
                    Expiry Date :
                    {{ productData.expiryDate ?? "None" }}
                    <br>
                </p>
                <div class="d-flex justify-content-start">
                    <!-- <h5>{{ productData.avgRating }}</h5> -->
                    <RenderStarRating :avgRating="productData.avgRating" />
                </div>
                <div class="d-flex justify-content-end" v-if="loggedInRole == 'manager'">
                    <button class="btn btn-outline-danger me-3" @click="$emit('delete-product')">
                        <font-awesome-icon :icon="['fas', 'trash-can']" class="faa-horizontal animated-hover" />
                        <!-- style="color: #c01c28;"  -->
                    </button>
                    <button class="btn btn-outline-primary" @click="$emit('edit-product')">
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
import RenderStarRating from "@/components/widgets/render_star_rating.vue"
import { reactive, watch, computed } from 'vue';
export default {
    name: "ProductCard",
    components: {
        RenderStarRating,
    },
    props: {
        productData: Object,
        loggedInRole: String,
        cartData: Object,
    },
    setup(props) {

        const cartForm = reactive({
            product_id: props.productData?.id,
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
.image {
    height: 80%;
    width: auto;
}

.img-btn {
    color: #4D6DE3;
}

.img-btn:hover {
    color: white;
}
</style>