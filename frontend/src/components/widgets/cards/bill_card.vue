<template>
    <div class="card-body text-start" @click="$emit('show-billDetails', bill)">
        <h5 class="card-title text-spaced-between">
            <span>
                Bill ID :
            </span>
            <span>
                {{ bill.id }}
            </span>
        </h5>
        <h6 class="card-subtitle mb-2 text-body-secondary text-spaced-between">
            <span>
                Date :
            </span>
            <span>
                {{ bill.date }}
            </span>
        </h6>
        <div class="text-body-secondary">
            <h6 class="text-spaced-between">
                <span>
                    Bill Amount :
                </span>
                <span>
                    ₹ {{ bill.billAmount }}
                </span>
            </h6>
            <h6 style="font-size: 15px;" class="text-spaced-between">
                <span>
                    Final Amount :
                </span>
                <span>
                    ₹ {{ bill.finalAmount }}
                </span>
            </h6>
            <!-- <button class="btn" @click="showOrderProductDetails(bill)">
                Show Product Details
            </button> -->
            <!-- TODO add coupon code and details here and update the total amount -->
        </div>
    </div>
</template>

<script>

// import { ref } from 'vue';
export default {
    name: 'BillCard',
    props: {
        bill: Object
    },

}
</script>

<style scoped>
.order-card {
    font-size: smaller;
    border: 1px solid black;
    border-radius: 12px;
    padding: 12px;
    margin: 12px;
}

h6 {
    margin-bottom: 0px;
}

p {
    margin-bottom: 0px;
}

.product-title {
    font-size: 15px;
}

.product-subtitle {
    font-size: 13px;
}

.product-text {
    font-size: 11px
}

.text-spaced-between {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
</style>