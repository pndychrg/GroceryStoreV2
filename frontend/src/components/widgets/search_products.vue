<template>
    <!-- Modal -->
    <div class="modal fade" id="searchModal" tabindex="-1" aria-labelledby="searchModal" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable modal-xl">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">Search Products</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form class="d-flex" role="search" @submit.prevent="fetchProductsData">
                        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search"
                            v-model="searchData.name" id="nameTextField" autofocus>
                        <button class="btn btn-outline-success" type="submit">Search</button>
                    </form>
                    <!-- Showing products which are found -->
                    <div class="row">
                        <ProductCard v-for="product in products" :key="product.id" class="ProductCard card"
                            :productData="product" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
 
<script>
import { onMounted, reactive, ref } from 'vue';
import { productMethods } from '@/services/HTTPRequests/productMethods'
import ProductCard from './cards/product_card.vue';
export default {
    name: "SearchProductModal",
    components: {
        ProductCard,
    },
    setup() {
        const products = ref([]);
        const searchData = reactive({
            "name": null,
            "rate": null,
            "manufactureDate": null,
            "section": null
        });

        const fetchProductsData = async () => {
            const productsData = await productMethods.searchForProduct(
                {
                    name: searchData.name,
                    rate: searchData.rate,
                    manufactureDate: searchData.manufactureDate,
                    section_id: searchData.section?.section_id
                }
            );
            products.value = productsData
        };

        onMounted(() => {
            const myModal = document.getElementById('searchModal')
            const myInput = document.getElementById('nameTextField')

            myModal.addEventListener('shown.bs.modal', () => {
                myInput.focus()
            })

        })

        return {
            products,
            searchData,
            fetchProductsData
        }
    }
}
</script>
 
<style scoped>
.ProductCard {
    border: none;
    box-shadow: 3px 3px 5px rgba(34, 35, 58, 0.2);
    border-radius: 15px;
    transition: all .3s;
    margin: 10px;
}

.box {
    display: flex;
    flex-wrap: wrap;
}

.box>* {
    flex: auto
}
</style>