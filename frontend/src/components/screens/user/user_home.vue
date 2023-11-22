<template>
    <div>
        <h2>Browse Products
            <button class="ms-2 btn btn-lg" data-bs-toggle="modal" data-bs-target="#searchModal"
                id="openSearchModalButton"><font-awesome-icon :icon="['fas', 'magnifying-glass']"
                    class="faa-horizontal animated-hover " style="color: #4D6DE3;" />
            </button>
        </h2>
        <div class="row m-2 products-wrapper">
            <h5 class="text-start">Our Most Recent Products</h5>
            <div v-for="product in products" :key="product.id" class="card"
                :class="{ 'card-unavailable': product.availableAmount == 0 }">
                <ProductCard :productData="product" loggedInRole="user" @add-to-cart="handleCart"
                    :cartData="getCartData(product.id)" @add-to-favourite="addProductToFavourite" />
            </div>
        </div>
        <SearchProductModal @add-to-cart="handleCart" />

    </div>
</template>

<script>
// import CartModal from "@/components/widgets/cart.vue"
import { productMethods } from '@/services/HTTPRequests/productMethods';
// eslint-disable-next-line no-unused-vars
import { buyMethods } from "@/services/HTTPRequests/buyMethods";
import ProductCard from '@/components/widgets/cards/product_card.vue';
import { onMounted, ref, computed } from 'vue';
import { favouriteMethods } from "@/services/HTTPRequests/favouriteMethods";
import SearchProductModal from "@/components/widgets/search_products.vue"
import { CartStateStore } from '@/services/cartStateManager';
export default {
    name: 'UserHome',
    components: {
        ProductCard,
        // CartModal,
        SearchProductModal
    },
    setup() {
        // const uiStore = UIStateStore()
        const products = ref([]);
        const cartStore = CartStateStore()
        const fetchProductsData = async () => {
            const productsData = await productMethods.fetchRecentProducts(3);
            // console.log(productsData);
            products.value = productsData;
        }
        const handleCart = async (cartForm) => {
            const dataObject = {
                "product_id": cartForm.product_id,
                "numOfProduct": cartForm.numOfProduct
            }
            const response = await cartStore.addProductToCart(dataObject)
            if (response) {
                cartStore.fetchCartForUser()
            }
        }

        const productCartData = computed(
            function (product_id) {
                if (cartStore.cart) {
                    return cartStore.cart.find(cartElement => cartElement.product.id === product_id);
                } else {
                    return null;
                }
            }
        )
        const getCartData = (product_id) => {
            if (cartStore.cart) {
                return cartStore.cart.find(cartElement => cartElement.product.id === product_id);
            } else {
                return null;
            }
        }

        onMounted(() => {
            fetchProductsData()
            cartStore.fetchCartForUser()
        })
        const addProductToFavourite = async (product) => {
            await favouriteMethods.addToFavourite(product.id);
        }


        return {
            products,
            handleCart,
            getCartData,
            productCartData,
            addProductToFavourite,
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
</style>