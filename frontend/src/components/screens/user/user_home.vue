<template>
    <div>
        <h2>Browse Products</h2>
        <div class="row m-2 products-wrapper">
            <ProductCard v-for="product in products" :key="product.id" :productData="product" loggedInRole="user"
                class="card" :class="{ 'card-unavailable': product.availableAmount == 0 }" @add-to-cart="handleCart"
                :cartData="getCartData(product.id)" />
        </div>

        <button class="btn btn-lg floating-container btn-outline-danger cartFloatingButton" type="button" @click="showCart">
            <font-awesome-icon :icon="['fas', 'fa-cart-plus']" class="faa-horizontal animated-hover " />
            <span v-if="cartDetails.cart?.length > 0"
                class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                {{ cartDetails.cart.length }}
            </span>

        </button>

        <teleport to="#modal-root">
            <CartModal v-show="isCartShown" :cart="cartDetails?.cart" :cartSum="cartDetails?.sum"
                @close="isCartShown = false" @remove-cart-item="removeCartItem" @buy-all="buyAllItems" />
        </teleport>
    </div>
</template>

<script>
import CartModal from "@/components/widgets/cart.vue"
import { productMethods } from '@/services/HTTPRequests/productMethods';
import { buyMethods } from "@/services/HTTPRequests/buyMethods";
import ProductCard from '@/components/widgets/cards/product_card.vue';
import { onMounted, ref, computed } from 'vue';
import { cartMethods } from '@/services/HTTPRequests/cartMethods';
export default {
    name: 'UserHome',
    components: {
        ProductCard,
        CartModal
    },
    setup() {
        const products = ref([]);
        const cartDetails = ref({});
        const fetchProductsData = async () => {
            const productsData = await productMethods.fetchAllProducts();
            products.value = productsData;
        }
        const fetchCartForUser = async () => {
            const cartData = await cartMethods.fetchAllCartProducts();
            cartDetails.value = cartData;
        }
        const handleCart = async (cartForm) => {
            const dataObject = {
                "product_id": cartForm.product_id,
                "numOfProduct": cartForm.numOfProduct
            }

            const response = await cartMethods.addToCart(dataObject)

            if (response) {
                // console.log(response);
                cartDetails.value.cart.unshift(response);
                cartDetails.value.sum += response.totalSum;
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

            }
        }

        const buyAllItems = async () => {
            const response = await buyMethods.buyAllCartItems();
            if (response) {
                console.log(response)
                cartDetails.value = {}
                // closing the cart
                isCartShown.value = false;
                // updating the home screen after buying so that updated available amount is shown
                // TODO YOU CAN DO IT THROUGH FRONTEND ONLY TRY THAT METHOD FOR BETTER PERFORMANCE
                fetchProductsData()
            }
        }
        onMounted(() => {
            fetchProductsData()
            fetchCartForUser()
        })

        // Cart opening
        const isCartShown = ref(false);
        const showCart = () => {
            isCartShown.value = true;
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
            buyAllItems
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
    width: 18rem;
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