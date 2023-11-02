<template>
    <div class="cart-container modal-overlay" @click="closeCart($event)">
        <div class="modal-content cart p-3">
            <div class="row card-header mb-2">
                <h6 class="col">Shopping Cart</h6>
                <a href="" class="col-auto float-end">Remove All</a>
            </div>
            <div style="padding-inline: 10px;">
                <div v-for="cartItem in cart" :key="cartItem.id" class="row p-2">
                    <div class="col-auto col-4">
                        <strong class="m-0">{{ cartItem.product.name }}</strong>
                        <p class="text-secondary m-0 p-0">{{ cartItem.product.section.name }}</p>
                    </div>
                    <div class="col-auto col-4 text-center">
                        <!-- TODO ADD increase and decreasing button -->
                        <p class="text-secondary">
                            {{ cartItem.numOfProduct }} {{ cartItem.product.section.unit }}
                        </p>
                    </div>
                    <div class="col text-end m-0">
                        <strong class="m-0 p-0">
                            $ {{ cartItem.totalSum }}
                        </strong>
                        <p class="text-secondary m-0 p-0">
                            {{ cartItem.product.rate }}/{{ cartItem.product.section.unit }}
                        </p>
                    </div>
                    <div class="col-auto float-end m-0">
                        <button class="btn" @click="$emit('remove-cart-item', cartItem)">
                            <font-awesome-icon :icon="['fas', 'trash-can']" class="faa-horizontal animated-hover"
                                style="color: #c01c28;" />
                        </button>
                    </div>
                </div>
            </div>
            <hr>
            <div class="row">
                <div class="col">
                    <p>
                        <strong>Sub-Total</strong>
                        <br>
                        <span class="text-secondary">{{ cart?.length }} items</span>
                    </p>
                </div>
                <h4 class="col-auto float-end">$ {{ cartSum }}</h4>
            </div>
            <div class="d-grid gap-2">
                <button v-if="isCartEmpty" class="btn btn-primary" type="button" @click="$emit('buy-all')">Checkout</button>
                <button v-else class="btn btn-primary" type="button" @click="$emit('buy-all')" disabled>Checkout</button>
            </div>
        </div>

    </div>
</template>

<script>
import { computed } from 'vue';

export default {
    name: "CartPage",
    props: {
        cart: Array,
        cartSum: Number
    },
    setup(props, { emit }) {
        const closeCart = ($event) => {
            if ($event.target.classList.contains('cart-container')) {
                emit('close');
            }
        }

        const isCartEmpty = computed(() => {
            if (props.cart?.length > 0) {
                return true;
            } else {
                return false;
            }
        });

        return {
            closeCart,
            isCartEmpty
        }
    }
}
</script>

<style scoped>
.cart {
    height: auto;
    flex-grow: 1;
    padding: 10px;
    box-sizing: border-box;
}

.cart-container {
    display: flex;
    flex-wrap: wrap;
    padding: 20%;
    align-content: center;
    /* Add the blur effect */
    backdrop-filter: blur(8px);
}

@import "@/static/css/modal.css"
</style>