<template>
    <div class="cart-container modal-overlay " @click="closeCart($event)">
        <div class="modal-content cart p-3 ">
            <h6 class="">Shopping Cart</h6>
            <!-- <div class="row card-header mb-2">
                <a href="" class="col-auto float-end">Remove All</a>
            </div> -->
            <div class="">
                <!-- <div class="col-md-8  details"> -->
                <div style="padding-inline: 10px;" v-if="cart?.length > 0">
                    <div v-for="cartItem in cart" :key="cartItem.id" class="row p-2">
                        <div class=" col-md-3 col-sm-12">
                            <strong class="m-0">{{ cartItem.product.name }}</strong>
                            <p class="text-secondary m-0 p-0">{{ cartItem.product.section.name }}</p>
                        </div>
                        <div class="col-md-3 col-sm-12">
                            <!-- TODO ADD increase and decreasing button -->
                            <p class="text-secondary">
                                {{ cartItem.numOfProduct }} {{ cartItem.product.section.unit }}
                            </p>
                        </div>
                        <div class="col-md-3  m-0 col-sm-6">
                            <strong class="m-0 p-0">
                                ₹ {{ cartItem.totalSum }}
                            </strong>
                            <p class="text-secondary m-0 p-0">
                                {{ cartItem.product.rate }}/{{ cartItem.product.section.unit }}
                            </p>
                        </div>
                        <div class="col-md-3 float-end m-0 col-sm-6">
                            <button class="btn float-end" @click="removeCartItem(cartItem)">
                                <font-awesome-icon :icon="['fas', 'trash-can']" class="faa-horizontal animated-hover"
                                    style="color: #c01c28;" />
                            </button>
                        </div>
                    </div>
                </div>
                <div v-else class="text-center">
                    <h5 class="text-secondary">No Items in Cart</h5>
                </div>
                <!-- </div> -->
                <!-- <div class="vr">
                </div> -->
            </div>
            <hr>
            <div class=" coupons " :style="{ pointerEvents: pointer_css }">
                <h6>Apply Coupons</h6>
                <form class="input-group mb-3 " @submit.prevent="checkCouponAvailability">
                    <input type="text" id="couponInput" class="form-control " placeholder="Coupon Code"
                        v-model="selectedCouponCode" required>
                </form>
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
                <h4 class="col-auto float-end">₹ {{ cartStateStore.sum }}</h4>
                <div v-if="selectedCoupon != null">
                    <p>
                        <strong>Coupon Discount</strong>
                        <span class="float-end" style="font-size: calc(1.275rem + .3vw);">{{ selectedCoupon.discount
                        }}%</span>
                        <br>

                    </p>
                    <p>
                        <strong>Final Amount</strong>
                        <strong class="float-end" style="font-size: calc(1.275rem + .3vw);">₹ {{ finalAmount
                        }}</strong>
                    </p>

                </div>
            </div>
            <div class="d-grid gap-2 mt-2">
                <button v-if="isCartEmpty" class="btn btn-primary" type="button"
                    @click="isBuyConfirmationShown = true">Checkout</button>
                <button v-else class="btn btn-primary" type="button" disabled>Checkout</button>
            </div>
        </div>
    </div>
    <teleport to="#modal-root">
        <BuyConfirmation v-show="isBuyConfirmationShown" :finalAmount="finalAmount" @close="isBuyConfirmationShown = false"
            @confirm="buyAllItems" />
    </teleport>
</template>

<script>
import { couponMethods } from '@/services/HTTPRequests/couponMethods';
import { computed, onBeforeMount, ref, watch } from 'vue';
import { CartStateStore } from '@/services/cartStateManager';
import BuyConfirmation from '@/components/widgets/buy_confirmation.vue'
import { buyMethods } from '@/services/HTTPRequests/buyMethods';
export default {
    name: "CartPage",
    components: {
        BuyConfirmation
    },
    setup(props, { emit }) {
        const cartStateStore = CartStateStore();
        const cart = ref(cartStateStore.cart);
        // const finalAmount = ref(cartStateStore.finalAmount);
        //watcher for updating cart value in the component
        watch(() => cartStateStore.cart, (newData) => {
            if (newData) {
                cart.value = cartStateStore.cart
            }
        })

        const removeCartItem = async (cartItem) => {
            await cartStateStore.removeCartItem(cartItem);
        }
        const coupons = ref([]);
        const selectedCoupon = ref(null);
        const selectedCouponCode = ref(null);
        const selectCouponFromDropdown = (coupon) => {
            selectedCoupon.value = coupon;
            selectedCouponCode.value = coupon.coupon_code
        }
        const checkCouponAvailability = async () => {
            // first checking if the selectedCoupon is null or not
            if (selectedCoupon.value == null) {
                const data = await couponMethods.fetchCouponFromCouponCode(selectedCouponCode.value);
                selectedCoupon.value = data;
                // emit("update-coupon", selectedCoupon.value);
            } else {
                // checking if the coupon_code is changed after selecting the coupon
                if (selectedCoupon.value.coupon_code != selectedCouponCode.value) {
                    const data = await couponMethods.fetchCouponFromCouponCode(selectedCouponCode.value);
                    selectedCoupon.value = data;
                    // emit("update-coupon", selectedCoupon);
                }
            }
        }

        const closeCart = ($event) => {
            if ($event.target.classList.contains('cart-container')) {
                emit('close');
            }
        }

        const isCartEmpty = computed(() => {
            if (cartStateStore?.cart?.length > 0) {
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
            if (data != null) {
                coupons.value = data;
            }
        }

        const finalAmount = computed(() => {
            const sum = cartStateStore.sum;
            if (selectedCoupon.value != null) {
                return sum - (selectedCoupon.value.discount * sum) / 100
            } else {
                return sum;
            }
        })

        // Buy methods 
        const isBuyConfirmationShown = ref(false);
        const buyAllItems = async () => {
            // buying all the items
            const response = await buyMethods.buyAllCartItems(selectedCoupon.value?.id);
            if (response) {
                // close both buy confirmation and cart modal
                isBuyConfirmationShown.value = false;
                // updating the cart by calling the fetchCartfunction again
                cartStateStore.fetchCartForUser();
                emit('close');
            }

        }
        onBeforeMount(async () => {
            await fetchAllCoupons();
            // console.log(coupons.value)
            await cartStateStore.fetchCartForUser();
        })
        return {
            cart,
            cartStateStore,
            closeCart,
            isCartEmpty,
            selectedCoupon,
            coupons,
            selectedCouponCode,
            selectCouponFromDropdown,
            checkCouponAvailability,
            pointer_css,
            removeCartItem,
            finalAmount,
            isBuyConfirmationShown,
            buyAllItems,
        }
    }
}
</script>

<style scoped>
.cart {
    display: block;
    /* width: max-content; */
    padding: 10px;
    box-sizing: border-box;
    justify-content: center;
    overflow: scroll;
    /* background-color: white; */
    /* border: 0.5px solid grey; */
    /* min-height: inherit; */
    /* border-radius: 2%; */
    /* max-height: none !important
    ; */
}

.cart-container {
    display: flex;
    flex-wrap: wrap;
    padding: 15%;
    align-content: center;
    /* Add the blur effect */
    backdrop-filter: blur(8px);
}

/* .coupons {} */

.vr {
    padding: 0px
}

.dropdown-item {
    cursor: pointer;
}

@media only screen and (max-width:768) {
    .cart {
        /* width: 90% !important; */
        width: 100% !important;
        max-width: 100% !important;
    }
}

@import "@/static/css/modal.css"
</style>