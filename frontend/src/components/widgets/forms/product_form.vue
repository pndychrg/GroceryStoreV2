<template>
    <div class="modal-overlay" @click="closeModal($event)">
        <div class="modal-content text-start">
            <div class="modal-header">
                <h4 class="modal-title">{{ formTexts.title }} {{ itemType }}</h4>
            </div>
            <div class="product-form">
                <form @submit.prevent="submitHandler">
                    <div class="modal-body">
                        <div class="form-group">
                            <label for="productName">Product Name</label>
                            <input v-model="formData.name" type="text" id="productName" class="form-control mb-2" required>
                        </div>
                        <div class="form-group">
                            <label for="productDescription">Product Description</label>
                            <textarea class="form-control mb-2" id="productDescription" rows="3"
                                v-model="formData.description"></textarea>
                        </div>

                        <div class="form-group">
                            <label for="availableAmount">Available Amount</label>
                            <input type="number" v-model="formData.availableAmount" class="form-control mb-2"
                                id="availableAmount" required min="0">
                        </div>

                        <div class="form-group">
                            <label for="rate">Rate</label>
                            <input type="number" v-model="formData.rate" class="form-control mb-2" id="rate" required
                                min="0">
                        </div>
                        <!-- TODO add minimum dates -->
                        <div class="form-group">
                            <label for="manufactureDate">Manufacture Date</label>
                            <input type="date" v-model="formData.manufactureDate" class="form-control mb-2"
                                id="manufactureDate" :max="today">
                        </div>
                        <div class=" form-group">
                            <label for="expiryDate">Expiry Date</label>
                            <input type="date" v-model="formData.expiryDate" class="form-control mb-2" id="expiryDate"
                                :min="today">
                        </div>
                        <div class="form-group mb-2 ">
                            <label for="section">Choose a Section:</label>
                            <select name="section" id="section" class="ms-2 form-control" v-model="formData.section_id">
                                <option default value="null">Section</option>
                                <option v-for="section in sectionsData" :key="section.id" :value="section.id">
                                    {{ section.name }}
                                </option>
                            </select>
                        </div>

                        <div class="form-actions modal-footer">
                            <button type="button" @click="handleCancel" class="btn btn-secondary">
                                Cancel
                            </button>
                            <button type="submit" class="btn btn-primary ms-2" @click="handleSubmit">
                                {{ formTexts.buttonText }}
                            </button>
                        </div>
                    </div>
                </form>

            </div>
        </div>

    </div>
</template>

<script>
import { productMethods } from '@/services/HTTPRequests/productMethods'
import { computed, reactive, watch } from 'vue'
export default {
    name: "ProductForm",
    props: {
        itemType: String,
        initialData: Object,
        sectionsData: Array,
    },
    setup(props, { emit }) {
        const today = new Date().toISOString().split('T')[0];
        const formData = reactive({
            name: "",
            description: "",
            availableAmount: null,
            rate: null,
            manufactureDate: null,
            expiryDate: null,
            section_id: null,
        })

        const clearForm = () => {
            Object.assign(formData, {
                name: "",
                description: "",
                availableAmount: null,
                rate: null,
                manufactureDate: null,
                expiryDate: null,
                section_id: null
            })
        }

        const handleCancel = () => {
            clearForm()
            emit('close');
        }
        const closeModal = ($event) => {
            if ($event.target.classList.contains('modal-overlay')) {
                emit('close');
            }
        }
        const handleSubmit = async () => {
            const dataObject = {
                "name": formData.name,
                "description": formData.description,
                "availableAmount": formData.availableAmount,
                "rate": formData.rate,
                "manufactureDate": formData.manufactureDate,
                "expiryDate": formData.expiryDate,
                "section_id": formData.section_id,
            }
            if (props.initialData == null) {
                const response = await productMethods.addProduct(
                    dataObject
                );
                if (response) {
                    clearForm()
                    emit('product-added', response);
                }
            } else {
                console.log(dataObject);
                const response = await productMethods.updateProduct(
                    props.initialData.id, dataObject
                );
                if (response) {
                    clearForm()
                    emit('product-edited', response);
                }
            }
            // console.log(formData);
        }


        const formTexts = computed(() => {
            if (props.initialData == null) {
                return {
                    title: "Add Product",
                    buttonText: "Submit"
                }
            }
            return {
                title: "Edit Product",
                buttonText: "Update"
            }
        })

        watch(() => props.initialData, (newData) => {
            if (newData) {
                formData.name = newData.name;
                formData.availableAmount = newData.availableAmount;
                formData.rate = newData.rate;
                formData.manufactureDate = newData.manufactureDate;
                formData.expiryDate = newData.expiryDate;
                formData.section_id = newData.section.id;
                formData.description = newData.description;
            }
        })

        return {
            closeModal,
            formTexts,
            formData,
            handleCancel,
            handleSubmit,
            today
        }
    }
}
</script>

<style scoped>
@import "@/static/css/modal.css";


.modal-content {
    max-width: 90% !important;
}

/* .dropdown-options {
    display: none;
    position: absolute;
    overflow: auto;
}


.dropdown:hover .dropdown-options {
    display: block;
} */
</style>