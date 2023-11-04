<template>
    <!-- Modal -->
    <div class="modal fade " id="searchModal" tabindex="-1" aria-labelledby="searchModal" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable modal-xlg">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">Search Products</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form class="d-flex" role="search" @submit.prevent="fetchProductsData">
                        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search"
                            v-model="searchData.name" id="nameTextField" autofocus>
                        <button class="btn btn-outline-success" type="submit">{{ buttonText }}</button>
                    </form>
                    <!-- Showing products which are found -->
                    <div class="box">
                        <div v-for="product in products" :key="product.id" class="card"
                            :class="{ 'card-unavailable': product.availableAmount == 0 }">
                            <ProductCard :productData="product" loggedInRole="user" @add-to-cart="handleCart" />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
 
<script>
import { computed, onMounted, reactive, ref } from 'vue';
import { productMethods } from '@/services/HTTPRequests/productMethods'
import ProductCard from './cards/product_card.vue';
export default {
    name: "SearchProductModal",
    components: {
        ProductCard,
    },
    setup(props, { emit }) {
        const products = ref([]);
        const searchData = reactive({
            "name": null,
            "rate": null,
            "manufactureDate": null,
            "section": null
        });
        const buttonText = computed(() => {
            if (products.value?.length > 0) {
                return "Clear";
            } else {
                return "Search";
            }
        })
        const fetchProductsData = async () => {

            // checking if products are already searched 
            // if yes then clear the search page

            if (products.value?.length > 0) {
                products.value = [];
                Object.assign(searchData, {
                    name: null,
                    rate: null,
                    manufactureDate: null,
                    section: null
                })
            } else {

                const productsData = await productMethods.searchForProduct(
                    {
                        name: searchData.name,
                        rate: searchData.rate,
                        manufactureDate: searchData.manufactureDate,
                        section_id: searchData.section?.section_id
                    }
                );
                products.value = productsData
            }

        };

        onMounted(() => {
            const myModal = document.getElementById('searchModal')
            const myInput = document.getElementById('nameTextField')

            myModal.addEventListener('shown.bs.modal', () => {
                myInput.focus()
            })

        })

        // emitting add to cart to the home page
        const handleCart = async (cartForm) => {
            emit("add-to-cart", cartForm)
        }

        return {
            products,
            searchData,
            fetchProductsData,
            handleCart,
            buttonText
        }
    }
}
</script>
 
<style scoped>
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

.box {
    display: flex;
    flex-wrap: wrap;
}

.box>* {
    flex: auto;
}

.modal-xlg {
    max-width: none;
}

@media (min-width: 1200px) {
    .modal-xlg {
        width: 85%;
    }
}
</style>