<template>
    <div class="card-body text-start" @click="showOrderProductDetails(bill)">
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
                    {{ bill.billAmount }}
                </span>
            </h6>
            <h6 style="font-size: 15px;" class="text-spaced-between">
                <span>
                    Total Amount :
                </span>
                <span>
                    {{ bill.finalAmount }}
                </span>
            </h6>
            <!-- <button class="btn" @click="showOrderProductDetails(bill)">
                Show Product Details
            </button> -->
            <!-- TODO add coupon code and details here and update the total amount -->
        </div>
        <h6 class="card-text mb-2 ">Products Bought</h6>
        <div class="order-container collapse" :id="'productDetails' + bill.id">
            <div class="order-card " v-for="order in bill.orders" :key="order.id">
                <h6 class="product-title">{{ order.product.name }}</h6>
                <h6 class="text-body-secondary product-subtitle">{{ order.product.section.name }}
                </h6>
                <div class="product-text row">
                    <p class="col-auto">
                        Rate : {{ order.product.rate }} / {{ order.product.section.unit }}
                    </p>
                    <p class="col-auto">
                        {{ order.numOfProduct }} {{ order.product.section.unit }}
                    </p>
                    <p class="col-auto">
                        Sum : {{ order.totalSum }}
                    </p>
                </div>
            </div>
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
    setup() {

        const showOrderProductDetails = (bill) => {
            const productDetailsElement = document.getElementById("productDetails" + bill.id);
            if (productDetailsElement.classList.contains("show")) {
                productDetailsElement.classList.remove("show");
            } else {
                productDetailsElement.classList.add("show");
            }
        }

        return {
            showOrderProductDetails
        }
    }
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