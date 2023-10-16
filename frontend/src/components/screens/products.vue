<template>
    <div class="">
        <h3>Products Page</h3>

        <div class="row m-2 border-dark-subtle products-wrapper border-2 border">
            <div class="row">
                <h2 class="col text-start">
                    Products

                    <button class="btn btn-primary" type="button" @click="showAddProductForm">
                        Add Product
                    </button>
                </h2>
            </div>

            <div v-for="product in products" :key="product.id" class="ProductCard card">
                <ProductCard :productData="product" @edit-product="showEditProductForm(product)" />
            </div>
        </div>

        <teleport to="#modal-root">
            <ProductForm v-show="isProductFormShown" :initialData="selectedProduct" @close="formClosed"
                :sectionsData="sections" @product-added="handleProductAdded" @product-edited="handleProductEdited" />
        </teleport>

    </div>
</template>

<script>
import { productMethods } from '@/services/HTTPRequests/productMethods'
import { onMounted, ref } from 'vue';
import ProductCard from '@/components/widgets/cards/product_card.vue'
import ProductForm from '@/components/widgets/forms/product_form.vue'
import { sectionMethods } from '@/services/HTTPRequests/sectionMethods';
export default {
    name: "ProductPage",
    components: {
        ProductCard,
        ProductForm,

    },
    setup() {

        const products = ref([]);
        const selectedProduct = ref(null);
        const isProductFormShown = ref(false);
        const sections = ref([]);
        const fetchProductsData = async () => {
            const productsData = await productMethods.fetchAllProducts();
            products.value = productsData;

        }
        const fetchSectionsData = async () => {
            const sectionsData = await sectionMethods.fetchAllSections();
            sections.value = sectionsData;
        }


        const formClosed = async () => {
            isProductFormShown.value = false;
            selectedProduct.value = null;
        }
        const showAddProductForm = () => {
            isProductFormShown.value = true;
        }

        const showEditProductForm = (product) => {
            isProductFormShown.value = true
            selectedProduct.value = product
        }

        const handleProductAdded = (newProduct) => {
            products.value?.unshift(newProduct);
            formClosed()
        }

        const handleProductEdited = (editedProduct) => {
            products.value.map((product, index) => {
                if (product.id == editedProduct.id) {
                    products.value[index] = editedProduct
                }
            })
            formClosed()
            console.log("product edited", editedProduct)
        }

        onMounted(() => {
            fetchProductsData();
            fetchSectionsData();
        })
        return {
            products,
            showAddProductForm,
            isProductFormShown,
            selectedProduct,
            showEditProductForm,
            formClosed,
            sections,
            handleProductAdded,
            handleProductEdited
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