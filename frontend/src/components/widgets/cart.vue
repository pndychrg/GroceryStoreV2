<template>
    <div class="cart-container modal-overlay " @click="closeCart($event)">
        <div class="modal-content cart p-3 ">
            <div class="row card-header mb-2">
                <h6 class="col">Shopping Cart</h6>
                <a href="" class="col-auto float-end">Remove All</a>
            </div>
            <div class="row">
                <div class="col details">
                    <div style="padding-inline: 10px;" v-if="cart?.length > 0">
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
                    <div v-else class="text-center">
                        <h5 class="text-secondary">No Items in Cart</h5>
                    </div>
                </div>
                <div class="vr">
                </div>
                <div class="col-auto coupons " :style="{ pointerEvents: pointer_css }">
                    <h6>Apply Coupons</h6>
                    <form class="input-group mb-3" @submit.prevent="checkCouponAvailability">
                        <input type="text" id="couponInput" class="form-control" placeholder="Coupon Code"
                            v-model="selectedCouponCode" required>
                        <button type="button" class="btn btn-outline-secondary dropdown-toggle dropdown-toggle-split"
                            data-bs-toggle="dropdown" aria-expanded="false">
                            <span class="visually-hidden">Toggle Dropdown</span>
                        </button>
                        <ul class="dropdown-menu dropdown-menu-end">
                            <li v-for="coupon in coupons" :key="coupon.id" class="dropdown-item">
                                <a @click="selectCouponFromDropdown(coupon)">
                                    {{ coupon.coupon_code }}
                                </a>
                            </li>
                        </ul>
                    </form>
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
                <div v-if="selectedCoupon != null">
                    <p>
                        <strong>Coupon Discount</strong>
                        <span class="float-end" style="font-size: calc(1.275rem + .3vw);">{{ selectedCoupon.discount
                        }}%</span>
                    </p>
                    <p>
                        <strong>Final Amount</strong>
                        <strong class="float-end" style="font-size: calc(1.275rem + .3vw);">$ {{ finalAmount }}</strong>
                    </p>

                </div>
            </div>
            <div class="d-grid gap-2 mt-2">
                <button v-if="isCartEmpty" class="btn btn-primary" type="button"
                    @click="$emit('buy-all', finalAmount)">Checkout</button>
                <button v-else class="btn btn-primary" type="button" @click="$emit('buy-all')" disabled>Checkout</button>
            </div>
        </div>

    </div>
</template>

<script>
import { couponMethods } from '@/services/HTTPRequests/couponMethods';
import { computed, onBeforeMount, ref } from 'vue';

export default {
    name: "CartPage",
    props: {
        cart: Array,
        cartSum: Number,
    },
    components: {

    },
    setup(props, { emit }) {
        const coupons = ref([]);
        const selectedCoupon = ref(null);
        const selectedCouponCode = ref(null);
        const selectCouponFromDropdown = (coupon) => {
            selectedCoupon.value = coupon;
            selectedCouponCode.value = coupon.coupon_code
        }
        const finalAmount = computed(() => {
            if (selectedCoupon.value != null) {
                return props.cartSum -
                    (props.cartSum * selectedCoupon.value.discount) / 100
            } else {
                return props.cart
            }
        })
        const checkCouponAvailability = async () => {

            // first checking if the selectedCoupon is null or not
            if (selectedCoupon.value == null) {
                const data = await couponMethods.fetchCouponFromCouponCode(selectedCouponCode.value);
                selectedCoupon.value = data;
            } else {
                // checking if the coupon_code is changed after selecting the coupon
                if (selectedCoupon.value.coupon_code != selectedCouponCode.value) {
                    const data = await couponMethods.fetchCouponFromCouponCode(selectedCouponCode.value);
                    selectedCoupon.value = data;
                }
            }
        }

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

        const pointer_css = computed(() => {
            if (isCartEmpty.value) {
                return "all"
            } else {
                return "none";
            }
        })

        const fetchAllCoupons = async () => {
            const data = await couponMethods.fetchAllUnexpiredCoupons()
            coupons.value = data;
            console.log('SDL coupons.value: ' + coupons.value[0].coupon_code);

        }

        onBeforeMount(() => {
            fetchAllCoupons();
        })
        return {
            closeCart,
            isCartEmpty,
            selectedCoupon,
            coupons,
            selectedCouponCode,
            selectCouponFromDropdown,
            checkCouponAvailability,
            finalAmount,
            pointer_css
        }
    }
}
</script>

<style scoped>
.cart {
    height: auto;
    width: auto;
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

.details {
    width: auto;
}

/* .coupons {
    max-width: 30%;
} */

.vr {
    padding: 0px
}

.dropdown-item {
    cursor: pointer;
}

@import "@/static/css/modal.css"
</style>