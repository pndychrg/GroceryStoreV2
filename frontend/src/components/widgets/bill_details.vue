<template>
    <div class="modal-overlay" @click="closeBillDetailsModal($event)">
        <div class="modal-content ">
            <div class="card-header mb-2 ">
                <h6>
                    Bill Details {{ bill.id }}
                    <span class="float-end">
                        {{ bill.date }}
                    </span>
                </h6>
            </div>
            <div class="card-body">
                <hr>
                <h6>Product Details</h6>
                <!-- product cards below -->
                <!-- Different product details view so not using the product card  -->
                <div v-for="order in bill.orders" :key="order.id" class="row g-0 product-details">
                    <div class="col-md-4 align-self-center">
                        <img v-if="order.product.img != null" :src="'data:image/png;base64,' + order.product.img"
                            class="rounded-start card-img image img-fluid " alt="Base64 Image">
                        <img v-else src="@/assets/img_notavailable.jpeg" alt="" class="rounded-start card-img  img-fluid"
                            aria-hidden="true">
                    </div>
                    <div class="col-md-8 p-4">
                        <div class="card-body text-start">
                            <h5 class="card-title">
                                {{ order.product.name }}
                            </h5>
                            <h6 class="card-subtitle">
                                {{ order.product.section.name }}
                            </h6>
                            <p class="card-text">
                                Rate : <span class="float-end">₹ {{ order.product.rate }} / {{ order.product.section.unit
                                }}</span>
                                <br>
                                Items Bought : <span class="float-end">
                                    {{ order.numOfProduct }}
                                </span>
                                <br>
                                Sum : <span class="float-end">
                                    ₹ {{ order.totalSum }}
                                </span>
                            </p>
                            <hr>
                            <div class="card-footer border border-1 p-2 rounded">
                                <h6>Rate Product</h6>
                                <StarRating :product_id="order.product.id" />
                            </div>
                        </div>
                    </div>
                </div>
                <hr>
                <!-- bill Details -->
                <div>
                    <h6>Bill Amount : <span class="float-end">
                            ₹ {{ bill.billAmount }}
                        </span></h6>
                    <h6>Coupon Code : <span class="float-end">{{ bill.coupon?.coupon_code ?? 'None Applied' }}</span></h6>
                    <h6>Discount : <span class="float-end">{{ bill.coupon?.discount ?? 'None Applied' }}</span></h6>
                    <h6>
                        Final Amount : <span class="float-end">₹ {{ bill.finalAmount }}</span>
                    </h6>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue';
import StarRating from '@/components/widgets/star_rating.vue';
export default {
    name: "BillDetailsModal",
    props: {
        bill: Object,
    },
    components: {
        StarRating,
    },
    setup(props, { emit }) {

        const rating = ref(null);
        const setRating = (starRating) => {
            rating.value = starRating
        }
        const closeBillDetailsModal = ($event) => {
            if ($event.target.classList.contains('modal-overlay')) {
                emit('close');
            }
        }
        return {
            closeBillDetailsModal,
            rating,
            setRating
        }
    }
}
</script>

<style scoped>
.product-details {
    box-shadow: 0 0px 8px rgba(0, 0, 0, 0.12);
    /* Reduce the box shadow */
    border-radius: 8px;
    /* Smaller border radius */
    margin: 40px;
    /* Reduce margin */
    padding: 10px;
    /* Reduce padding */
}

.modal-content {
    max-width: 90%;
    width: 65%;
    font-size: large !important;
    /* margin-top: 50px !important; */
    max-height: 90% !important;
    /* margin-bottom: 50px !important; */

}

@import "@/static/css/modal.css"
</style>