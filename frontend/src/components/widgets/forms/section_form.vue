<template>
    <div class="modal-overlay" @click="closeModal($event)">
        <div class="modal-content text-start">
            <div class="modal-header">
                <h4 class="modal-title">{{ formTitle }} {{ itemType }}</h4>
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
                            <button type="button" @click="handleCancel" class="btn btn-secondary me-3">
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
import { userStateStore } from '@/services/stateManager';

export default {
    name: "SectionFormModal",
    emits: ["close", "section-edited", "section-added"],
    props: {
        itemType: String,
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
            if (props.itemType === 'section') {
                const store = userStateStore()
                if (store.user.role == 'admin') {
                    if (props.initialData == null) {
                        // backend request
                        const response = await sectionMethods.addSection(dataObject)
                        if (response) {
                            clearForm()
                            emit('section-added', response)
                        }
                    } else {
                        const response = await sectionMethods.updateSection(props.initialData.id, dataObject)
                        // console.log(response);
                        clearForm();
                        emit('section-edited', response)
                        console.log("Update button clicked")
                    }
                } else {
                    const dataObject = {
                        "name": formData.name,
                        "unit": formData.unit,
                        "request": props.initialData == null ? 'add' : 'edit',
                        "reg_section_id": props.initialData?.id ?? null,
                    }
                    const response = await sectionMethods.addSection(dataObject)
                    if (response) {
                        clearForm()
                        emit('section-added', response)
                    }
                }
            }
            else {
                const response = await sectionMethods.updateSectionRequest(
                    props.initialData.id, dataObject
                );
                if (response) {
                    clearForm()
                    emit('sectionRequest-edited', response);
                }
            }

        }
        const closeModal = ($event) => {
            if ($event.target.classList.contains('modal-overlay')) {
                emit('close');
            }
        }

        watch(() => props.initialData, (newData) => {
            if (newData) {
                formData.name = newData.name;
                formData.unit = newData.unit;
            }
        }, { immediate: true })
        const clearForm = () => {
            Object.assign(formData, {
                "name": "",
                "unit": '',
            })
        }

        const handleCancel = () => {
            clearForm();
            emit('close');
        }
        return {
            closeModal,
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

.modal-content {
    max-width: 90% !important;
}
</style>