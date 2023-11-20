<template>
    <div>
        <h2>Browse Products
            <button class="ms-2 btn btn-lg" data-bs-toggle="modal" data-bs-target="#searchModal"
                id="openSearchModalButton"><font-awesome-icon :icon="['fas', 'magnifying-glass']"
                    class="faa-horizontal animated-hover " style="color: #4D6DE3;" />
            </button>
        </h2>
        <div class="row m-2 products-wrapper">
            <div v-for="product in products" :key="product.id" class="card"
                :class="{ 'card-unavailable': product.availableAmount == 0 }">
                <ProductCard :productData="product" loggedInRole="user" @add-to-cart="handleCart"
                    :cartData="getCartData(product.id)" @add-to-favourite="addProductToFavourite" />
            </div>
        </div>

        <button class="btn btn-lg floating-container btn-outline-danger cartFloatingButton" type="button" @click="showCart">
            <font-awesome-icon :icon="['fas', 'fa-cart-plus']" class="faa-horizontal animated-hover " />
            <span v-if="cartDetails?.cart != null && cartDetails.cart.length > 0"
                class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                {{ cartDetails?.cart?.length }}
            </span>
        </button>

        <!-- Modal -->
        <div class="modal fade" id="buyConfirmationModal" tabindex="-1" aria-labelledby="exampleModalLabel"
            aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered ">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="exampleModalLabel">Buy Confirmation</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"
                            id="closeBuyConfirmation"></button>
                    </div>
                    <div class="modal-body text-start">
                        <h5>Confirm and Pay for all the goods</h5>
                        <p>Total Order Sum = {{ finalAmount }}</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary" @click="buyAllItems">Buy</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Button trigger modal -->
        <button type="button" class="btn btn-primary" id="buyConfirmation" data-bs-toggle="modal"
            data-bs-target="#buyConfirmationModal" hidden>
            Launch static backdrop modal
        </button>


        <SearchProductModal @add-to-cart="handleCart" />

        <teleport to="#modal-root">
            <CartModal v-show="isCartShown" :cart="cartDetails?.cart" :cartSum="cartDetails?.sum" @close="showCart"
                @remove-cart-item="removeCartItem" @buy-all="buyModalSHow" @update-coupon="hanldeUpdatedCoupon" />
        </teleport>
    </div>
</template>

<script>
import CartModal from "@/components/widgets/cart.vue"
import { productMethods } from '@/services/HTTPRequests/productMethods';
// eslint-disable-next-line no-unused-vars
import { buyMethods } from "@/services/HTTPRequests/buyMethods";
import ProductCard from '@/components/widgets/cards/product_card.vue';
import { onMounted, ref, computed } from 'vue';
import { cartMethods } from '@/services/HTTPRequests/cartMethods';
import { UIStateStore } from "@/services/uiStateManager";
import { favouriteMethods } from "@/services/HTTPRequests/favouriteMethods";
import SearchProductModal from "@/components/widgets/search_products.vue"
export default {
    name: 'UserHome',
    components: {
        ProductCard,
        CartModal,
        SearchProductModal
    },
    setup() {
        const uiStore = UIStateStore()
        const products = ref([]);
        const cartDetails = ref({
            cart: null,
            sum: null,
        });
        const finalAmount = computed(
            () => {
                if (cartDetails.value.sum == null) {
                    return null;
                } else {
                    if (cartDetails.value.sum != null && selectedCoupon.value == null) {
                        return cartDetails.value.sum;
                    } else {
                        const retAmount = cartDetails.value.sum - (cartDetails.value.sum * selectedCoupon.value.discount) / 100;
                        return retAmount
                    }
                }
            }
        );
        const selectedCoupon = ref(null);
        const fetchProductsData = async () => {
            const productsData = await productMethods.fetchAllProducts();
            products.value = productsData;
        }
        const fetchCartForUser = async () => {
            const cartData = await cartMethods.fetchAllCartProducts();
            if (cartData != null) {
                cartDetails.value = cartData;
                // console.log(cartData);
                finalAmount.value = cartData.sum;
                // Object.assign(cartDetails.value, { finalAmount: null })
            }
        }
        const handleCart = async (cartForm) => {
            const dataObject = {
                "product_id": cartForm.product_id,
                "numOfProduct": cartForm.numOfProduct
            }

            const response = await cartMethods.addToCart(dataObject)

            if (response) {
                // console.log(response);
                // THIS PEICE OF CODE IS CAUSING MULTIPLE ENTRIES IN CART 
                // cartDetails?.value.cart.unshift(response);
                // cartDetails.value.sum += response.totalSum;
                // FOR SIMPLIFYING AT THE MOMENT WE WILL JUST FETCH THE CART FOR THE USER 
                fetchCartForUser()
            }
        }

        const productCartData = computed(
            function (product_id) {
                if (cartDetails.value && cartDetails.value.cart) {
                    return cartDetails.value.cart.find(cartElement => cartElement.product.id === product_id);
                } else {
                    return null;
                }
            }
        )
        const getCartData = (product_id) => {
            if (cartDetails.value && cartDetails.value.cart) {
                return cartDetails.value.cart.find(cartElement => cartElement.product.id === product_id);
            } else {
                return null;
            }
        }


        const removeCartItem = async (cartItem) => {
            // console.log(cartItem)
            const response = await cartMethods.deleteCartProduct(cartItem)
            if (response) {
                cartDetails.value.cart = cartDetails.value.cart.filter(s => s !== cartItem)
                // TODO update finalAmount
            }
        }

        const buyAllItems = async () => {
            console.log(selectedCoupon.value.id);
            const response = await buyMethods.buyAllCartItems(selectedCoupon.value.id);
            if (response) {
                console.log(response)
                cartDetails.value = {}
                finalAmount.value = null;
                // closing the cart
                isCartShown.value = false;
                //     // updating the home screen after buying so that updated available amount is shown
                //     // TODO YOU CAN DO IT THROUGH FRONTEND ONLY TRY THAT METHOD FOR BETTER PERFORMANCE
                document.getElementById("closeBuyConfirmation").click()
                fetchProductsData()
            }
        }

        const buyModalShow = () => {
            // check if products are available in cart
            if (cartDetails.value.cart.length > 0) {
                document.getElementById("buyConfirmation").click()
            }
            // document.getElementById("exampleModal").modal('show')
        }

        const hanldeUpdatedCoupon = (updatedCoupon) => {
            console.log(`coupon ${JSON.stringify(updatedCoupon)}`);
            selectedCoupon.value = updatedCoupon;
            console.log(`selectedCoupon ${selectedCoupon.value}`)
        }

        onMounted(() => {
            fetchProductsData()
            fetchCartForUser()
        })

        // Cart opening
        const isCartShown = ref(false);
        const showCart = () => {
            uiStore.toggleModal();
            isCartShown.value = !isCartShown.value;
        }

        // adding to favourite
        //TODO add remove from cart also which can be then activated if the product is already in cart

        const addProductToFavourite = async (product) => {
            await favouriteMethods.addToFavourite(product.id);
        }


        return {
            products,
            handleCart,
            getCartData,
            isCartShown,
            showCart,
            cartDetails,
            removeCartItem,
            productCartData,
            buyAllItems,
            buyModalSHow: buyModalShow,
            addProductToFavourite,
            finalAmount,
            hanldeUpdatedCoupon

        }
    }

}
</script>

<style scoped>
.products-wrapper {
    margin: auto;
    background-color: #ffffff;
    /* box-shadow: 0px 14px 80px rgba(34, 35, 58, 0.2); */
    padding: 40px 55px 45px 55px;
    border-radius: 15px;
    transition: all .3s;

}


.card {
    /* width: 180rem; */
    max-width: 540px;
    margin: 10px;
    border: none;
    background: #fff;
    box-shadow: 0 6px 10px rgba(0, 0, 0, .08), 0 0 6px rgba(0, 0, 0, .05);
    transition: .3s transform cubic-bezier(.155, 1.105, .295, 1.12), .3s box-shadow, .3s -webkit-transform cubic-bezier(.155, 1.105, .295, 1.12);
    cursor: pointer;
}

.card-unavailable {
    box-shadow: 0 6px 10px rgba(255, 0, 0, .10), 0 0 6px rgba(255, 0, 0, .15) !important;
}

.card-unavailable:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 20px rgba(255, 0, 0, .12), 0 4px 8px rgba(255, 0, 0, .06) !important;
}

.card:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 20px rgba(0, 0, 0, .12), 0 4px 8px rgba(0, 0, 0, .06);
}

.floating-container {

    /* border-radius: 15px;
    border: 2px solid red; */
    /* position: fixed; */
    position: fixed;
    bottom: 10px;
    right: 0px;
    /* float: right; */
    margin-right: 25px;
    box-shadow: 0 6px 10px rgba(0, 0, 0, .08), 0 0 6px rgba(0, 0, 0, .05);
    transition: .3s transform cubic-bezier(.155, 1.105, .295, 1.12), .3s box-shadow, .3s -webkit-transform cubic-bezier(.155, 1.105, .295, 1.12);
}

.floating-container:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 20px rgba(0, 0, 0, .12), 0 4px 8px rgba(0, 0, 0, .06);
}

.cartFloatingButton {
    color: #4D6DE3;
}

.cartFloatingButton:hover {
    color: white;
}
</style>