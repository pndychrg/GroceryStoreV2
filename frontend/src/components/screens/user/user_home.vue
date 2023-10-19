<template>
    <div>
        <h2>Browse Products</h2>
        <div class="row m-2 products-wrapper">
            <ProductCard v-for="product in products" :key="product.id" :productData="product" loggedInRole="user"
                class="ProductCard card" @add-to-cart="handleCart" :cartData="getCartData(product.id)" />
        </div>
    </div>
</template>

<script>
import { productMethods } from '@/services/HTTPRequests/productMethods';
import ProductCard from '@/components/widgets/cards/product_card.vue';
import { onMounted, ref } from 'vue';
import { cartMethods } from '@/services/HTTPRequests/cartMethods';
export default {
    name: 'UserHome',
    components: {
        ProductCard
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
                console.log(response);
            }
        }

        const getCartData = (product_id) => {
            if (cartDetails.value && cartDetails.value.cart) {
                return cartDetails.value.cart.find(cartElement => cartElement.product.id === product_id);
            } else {
                return null;
            }
        }

        onMounted(() => {
            fetchProductsData()
            fetchCartForUser()
        })

        return {
            products,
            handleCart,
            getCartData
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


.ProductCard {
    border: none;
    box-shadow: 3px 3px 5px rgba(34, 35, 58, 0.2);
    border-radius: 15px;
    transition: all .3s;
    width: 18rem;
    margin: 10px;
}
</style>