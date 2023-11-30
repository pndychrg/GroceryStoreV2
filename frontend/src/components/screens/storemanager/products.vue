<template>
    <div class="">
        <h3 class="mb-3">Products Page <button class="btn btn-primary" type="button" @click="showAddProductForm">
                Add Product
            </button></h3>

        <div class="row m-2 border-dark-subtle products-wrapper border-2 border">
            <div v-for="product in products" :key="product.id" class="ProductCard card"
                :class="{ UnavailableProduct: product.availableAmount == 0 }">
                <ProductCard loggedInRole="manager" :productData="product" @edit-product="showEditProductForm(product)"
                    @delete-product="showDeleteConfirmation(product)"
                    @show-addimagemodal="showAddProductImageModal(product)" />
            </div>
        </div>
        <div v-show="isModalVisible" :class="{ 'modal': isModalVisible, 'hidden': !isModalVisible }">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            Add Product Image For Product : {{ selectedProduct?.name }}
                        </h5>
                        <button type="button" class="btn-close" @click="closeAddProductImageModal"></button>
                    </div>
                    <div v-if="selectedProduct?.img != null" class="pt-2">
                        <h6 class="">Product Already has a Image</h6>
                        <img :src="'data:image/png;base64,' + selectedProduct.img" class="image img-fluid">
                        <h6>Do You want to update ? </h6>
                    </div>
                    <div v-if="productImage != null">
                        <h6 class="pt-2">Image Preview</h6>
                        <img :src="previewImage" class="image img-fluid" />
                    </div>
                    <div class="modal-footer form ">
                        <input type="file" class="formFile form-control" @change="handleFileUpload">
                        <button @click="uploadImage" style="width: 100%;" class="btn btn-outline-primary">Upload</button>
                    </div>
                </div>
            </div>
        </div>
        <teleport to="#modal-root">
            <ConfirmationModal v-show="isDeleteModalShown" deleteElement="Product" :element="selectedProduct"
                @close="isDeleteModalShown = false" @confirm="deleteProduct" />

            <ProductForm v-show="isProductFormShown" :initialData="selectedProduct" @close="formClosed"
                :sectionsData="sections" @product-added="handleProductAdded" @product-edited="handleProductEdited" />
        </teleport>

    </div>
</template>

<script>
import { productMethods } from '@/services/HTTPRequests/productMethods'
import { computed, onMounted, ref } from 'vue';
import ProductCard from '@/components/widgets/cards/product_card.vue'
import ProductForm from '@/components/widgets/forms/product_form.vue'
import { sectionMethods } from '@/services/HTTPRequests/sectionMethods';
import ConfirmationModal from '@/components/widgets/confirmation.vue';
export default {
    name: "ProductPage",
    components: {
        ProductCard,
        ProductForm,
        ConfirmationModal
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
        const isDeleteModalShown = ref(false);
        const showDeleteConfirmation = (productData) => {
            // uiStateStore.toggleModal()
            selectedProduct.value = productData
            isDeleteModalShown.value = true;
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
            // uiStateStore.toggleModal()
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

        const deleteProduct = async (deletedProduct) => {
            console.log(deletedProduct)
            const response = await productMethods.deleteProduct(deletedProduct);
            if (response) {
                products.value = products.value.filter(s => s !== deletedProduct)
            }
        }

        // Image Methods
        const isModalVisible = ref(false);
        const productImage = ref(null);
        const showAddProductImageModal = (product) => {
            selectedProduct.value = product;
            isModalVisible.value = true;
        }
        const closeAddProductImageModal = () => {
            selectedProduct.value = null;
            isModalVisible.value = false;
        };
        const handleFileUpload = (event) => {
            // Handle file selection
            productImage.value = event.target.files[0];
            // console.log(productImage.value)
        };
        const previewImage = computed(() => {
            return URL.createObjectURL(productImage.value)
        })
        const uploadImage = async () => {
            console.log(productImage.value)
            // console.log(selectedProduct.value.id);
            const response = await productMethods.addProductImage(selectedProduct.value, productImage.value);
            console.log(response);
            if (response) {
                handleProductEdited(response);
            }
            // update the img according to response
            //clear selected files
            productImage.value = null;
            closeAddProductImageModal(); // Close the modal after uploading
        };



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
            handleProductEdited,
            isDeleteModalShown,
            showDeleteConfirmation,
            deleteProduct,
            productImage,
            previewImage,
            showAddProductImageModal,
            handleFileUpload,
            uploadImage,
            isModalVisible,
            closeAddProductImageModal
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
    justify-content: center;
}

.ProductCard {
    border: none;
    box-shadow: 3px 3px 5px rgba(34, 35, 58, 0.2);
    border-radius: 15px;
    transition: all .3s;

    max-width: 540px;
    margin: 10px;
}

.UnavailableProduct {
    box-shadow: 3px 3px 5px rgba(255, 25, 25, 0.2);
}

.modal {
    display: block;
    position: fixed;
    /* Stay in place */
    z-index: 1;
    /* Sit on top */
    left: 0;
    top: 0;
    width: 100%;
    /* Full width */
    height: 100%;
    /* Full height */
    overflow: auto;
    /* Enable scroll if needed */
    background-color: rgb(0, 0, 0);
    /* Fallback color */
    background-color: rgba(0, 0, 0, 0.4);
    /* Black w/ opacity */
}

.modal-content {
    background-color: #fefefe;
    margin: 15% auto;
    /* 15% from the top and centered */
    padding: 20px;
    border: 1px solid #888;
    width: max-content;
    /* Could be more or less, depending on screen size */

}
</style>