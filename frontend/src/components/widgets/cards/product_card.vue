<template>
    <div class="row g-0  ">
        <div class="col-md-4 align-self-center">
            <img v-if="productData.img != null" :src="imageData" class="rounded-start card-img image img-fluid "
                alt="Base64 Image">
            <img v-else src="@/assets/img_notavailable.jpeg" alt="" class="rounded-start card-img  img-fluid"
                aria-hidden="true">
        </div>
        <div class="col-md-8 p-2">
            <div class="card-body text-start ">
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
                        <button class="btn" @click="showDetails">
                            <font-awesome-icon icon="fa-solid fa-comments" class="faa-horizontal animated-hover"
                                style="color: #4D6DE3;" />
                        </button>
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
                    <RenderStarRating :avgRating="productData.avgRating" iconSize="large" />
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
    <div class="details-container text-start p-3 " v-if="productData.ratings.length > 0"
        :class="{ renderDetails: isDetailsShown == true }" @click="showDetails">
        <div class="rating " v-for=" rating  in  productData.ratings " :key="rating">
            <!-- <h5>Rating: <span class="">{{ rating.rating }}</span></h5> -->
            <h6 style="margin: 0px;">{{ rating.user.name }}</h6>
            <RenderStarRating :avgRating="rating.rating" iconSize="small" />
            <p>
                Comment : {{ rating.comment }}
            </p>
            <hr>
        </div>
    </div>
    <div v-else class="details-container text-center p-3 " :class="{ renderDetails: isDetailsShown == true }"
        style="justify-content: center;" @click="showDetails">
        <h6>No Comments Available</h6>
    </div>
</template>

<script>
import RenderStarRating from "@/components/widgets/render_star_rating.vue"
import { reactive, watch, computed, ref } from 'vue';
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
    emits: [
        "add-to-cart",
        "edit-product",
        "delete-product",
        "add-to-favourite",
        "show-addimagemodal",

    ],
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
        // details-container setup
        const isDetailsShown = ref(false);

        const showDetails = () => {
            console.log("Button Pressed")
            isDetailsShown.value = !isDetailsShown.value
        }
        return {
            cartForm,
            imageData,
            isDetailsShown,
            showDetails,
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

.details-container {
    position: absolute;
    top: 50%;
    left: 50%;
    display: none;
    flex-direction: column;
    /* align-items: center; */
    justify-content: start;
    transform: translate(-50%, -50%) scale(1);
    /* opacity: 0; */
    background-color: rgba(255, 255, 255, 0.9);
    width: 100%;
    height: 100%;
    word-wrap: break-word;
    transition: opacity 0.3s ease-in-out, transform 0.3s ease-in-out;
    overflow-wrap: break-word;
    overflow-y: auto;
}

.renderDetails {
    /* opacity: 1; */
    display: flex;
    transform: translate(-50%, -50%) scale(1);
}

.card-body {
    border-left: 1px solid rgba(0, 0, 0, 0.1);
}

/* Show details on hover */
/* .card:hover .details-container {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1);
    pointer-events: none;
} */

/* .card:active .details-container {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1);
    pointer-events: none;
} */
</style>



<!-- 
ing : 4
Comment : Best laptop for gaming, would be better if the panel have mor esh rates

Best laptop for gaming, would be better if the panel have more refresh rates


 -->