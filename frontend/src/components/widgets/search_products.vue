<template>
    <!-- Modal -->
    <div class="modal fade " id="searchModal" tabindex="-1" aria-labelledby="searchModal" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable modal-xlg ">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">Search Products</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form class="" role="search" @submit.prevent="fetchProductsData">
                        <div class="d-flex">
                            <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search"
                                v-model="searchData.name" id="nameTextField" autofocus>
                            <button class="btn btn-outline-success" type="submit"><font-awesome-icon
                                    icon="fa-solid fa-magnifying-glass" /></button>
                            <button type="button" class="btn btn-outline-primary ms-2"
                                @click="isFilterFormShown = !isFilterFormShown">
                                <font-awesome-icon icon="fa-solid fa-filter" class="faa-horizontal animated-hover" />
                            </button>
                            <button class="btn btn-outline-danger ms-2" type="button" @click="clearForm">
                                <font-awesome-icon icon="fa-solid fa-xmark" class="faa-horizontal animated-hover " />
                            </button>
                        </div>
                        <div class="collapse p-3 border border-2 border-dark-subtle rounded-2 m-2"
                            :class="{ 'show': isFilterFormShown }" id="filterForm">
                            <div class="row g-2">
                                <div class="col-md">
                                    <input class="form-control" type="search" placeholder="Filter for Rate"
                                        aria-label="Search" v-model="searchData.rate" id="rateTextField" autofocus>
                                </div>
                                <div class="col-md">
                                    <input type="date" v-model="searchData.manufactureDate" class="form-control mb-2"
                                        id="manufactureDate">
                                </div>
                            </div>
                            <label for="section" class="float-start">Choose a Section:</label>
                            <select name="section" id="section" class="ms-2 form-select" v-model="searchData.section_id">
                                <option default value="null">Section</option>
                                <option v-for="section in sections" :key="section.id" :value="section?.id">
                                    {{ section.name }}
                                </option>
                            </select>
                        </div>
                    </form>
                    <!-- Showing products which are found -->
                    <div class="box">
                        <div v-for=" product  in  products " :key="product.id" class="card"
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
import { onMounted, reactive, ref } from 'vue';
import { productMethods } from '@/services/HTTPRequests/productMethods'
import ProductCard from './cards/product_card.vue';
import { sectionMethods } from '@/services/HTTPRequests/sectionMethods';
export default {
    name: "SearchProductModal",
    components: {
        ProductCard,
    },
    setup(props, { emit }) {
        const products = ref([]);
        const isFilterFormShown = ref(false);
        const sections = ref(null);
        const fetchAllSections = async () => {
            const response = await sectionMethods.fetchAllSections()
            sections.value = response;
        }
        const searchData = reactive({
            "name": null,
            "rate": null,
            "manufactureDate": null,
            "section_id": null
        });
        const clearForm = () => {
            products.value = [];
            Object.assign(searchData, {
                name: null,
                rate: null,
                manufactureDate: null,
                section_id: null
            })
            console.log("clearForm ran")

        }
        const fetchProductsData = async () => {
            console.log(searchData.section_id);
            // checking if products are already searched 
            // if yes then clear the search page
            const productsData = await productMethods.searchForProduct(
                {
                    name: searchData.name,
                    rate: searchData.rate,
                    manufactureDate: searchData.manufactureDate,
                    section_id: searchData.section_id
                }
            );
            products.value = productsData

        };

        onMounted(() => {
            fetchAllSections()
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
            isFilterFormShown,
            sections,
            clearForm
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
    justify-content: center;
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