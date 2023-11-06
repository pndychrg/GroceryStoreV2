<template>
    <div class="modal-overlay" @click="closeBillDetailsModal($event)">
        <div class="modal-content p-3">
            <div class="card-header mb-2 ">
                <h6>
                    Bill Details {{ bill.id }}
                    <span class="float-end">
                        {{ bill.date }}
                    </span>
                </h6>
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
                    <div class="col-md-8 p-2">
                        <div class="card-body text-start">
                            <h5 class="card-title">
                                {{ order.product.name }}
                            </h5>
                            <h6 class="card-subtitle">
                                {{ order.product.section.name }}
                            </h6>
                            <p class="card-text">
                                Rate : <span class="float-end">{{ order.product.rate }} / {{ order.product.section.unit
                                }}</span>
                                <br>
                                Items Bought : <span class="float-end">
                                    {{ order.numOfProduct }}
                                </span>
                                <br>
                                Sum : <span class="float-end">
                                    {{ order.totalSum }}
                                </span>
                            </p>
                        </div>
                    </div>
                </div>
                <hr>
                <!-- bill Details -->
                <div>
                    <h6>Bill Amount : <span class="float-end">
                            {{ bill.billAmount }}
                        </span></h6>
                    <h6>
                        Final Amount : <span class="float-end">{{ bill.finalAmount }}</span>
                    </h6>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "BillDetailsModal",
    props: {
        bill: Object,
    },
    setup(props, { emit }) {
        const closeBillDetailsModal = ($event) => {
            if ($event.target.classList.contains('modal-overlay')) {
                emit('close');
            }
        }
        return {
            closeBillDetailsModal
        }
    }
}
</script>

<style scoped>
.product-details {
    /* border: 1px solid grey; */
    box-shadow: 0 0px 12px rgba(0, 0, 0, 0.12);
    border-radius: 12px;
    margin: 25px 5px 25px 5px;
    padding: 5px;
}

.modal-content {
    min-width: 1000px;
    font-size: large !important;
}

@import "@/static/css/modal.css"
</style>