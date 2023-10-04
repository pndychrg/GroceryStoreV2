<template>
    <div class="modal-overlay">
        <div class="modal-content text-start">
            <div class="modal-header">
                <h4 class="modal-title">{{ formTitle }}</h4>
            </div>
            <div class="section-form ">
                <form @submit.prevent="submitHandler">
                    <div class="modal-body">
                        <div class="form-group">
                            <label for="sectionName">Section Name</label>
                            <input v-model="formData.name" type="text" id="sectionName" class="form-control mb-2" required>
                        </div>
                        <div class="form-group">
                            <label for="sectionUnit">Section Unit</label>
                            <input v-model="formData.unit" class="form-control mb-2" type="text" id="sectionUnit" required>
                        </div>
                        <div class="form-actions modal-footer">
                            <button type="button" @click="handleCancel" class="btn btn-secondary">
                                Cancel
                            </button>
                            <button type="submit" class="btn btn-primary">
                                {{ submitButtonText }}
                            </button>
                        </div>
                    </div>
                </form>

            </div>
        </div>
    </div>
</template>

<script>
import { computed, reactive, watch } from 'vue';
import { sectionMethods } from '@/services/HTTPRequests/sectionMethods';

export default {
    name: "SectionFormModal",
    emits: ["close", "section-edited", "section-added"],
    props: {
        initialData: Object
    },
    setup(props, { emit }) {
        // initialising the data models
        const formData = reactive({
            name: "",
            unit: '',
        });

        const formTitle = computed(() => {
            if (props.initialData == null) {
                return "Add Section"
            }
            return "Edit Section"
        })

        const submitButtonText = computed(() => {
            if (props.initialData == null) {
                return "Submit"
            }
            return "Update"
        })

        const submitHandler = async () => {
            const dataObject = {
                "name": formData.name,
                "unit": formData.unit,
            }
            if (props.initialData == null) {
                // backend request
                const response = await sectionMethods.addSection(dataObject)
                if (response) {
                    emit('section-added', response)
                }
            } else {
                console.log("Update button clicked")
            }

        }

        watch(() => props.initialData, (newData) => {
            if (newData) {
                formData.name = newData.name;
                formData.unit = newData.unit;
            }
        }, { immediate: true })


        const handleCancel = () => {
            Object.assign(formData, {
                "name": "",
                "unit": ""
            })
            emit('close');
        }
        return {
            formData,
            handleCancel,
            submitHandler,
            formTitle,
            submitButtonText
        }
    }
}
</script>

<style scoped>
@import "@/static/css/modal.css";
</style>