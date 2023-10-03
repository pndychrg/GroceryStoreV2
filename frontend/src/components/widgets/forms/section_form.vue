<template>
    <div class="modal-dialog">
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
import { sectionMethods } from '@/services/HTTPRequests/sectionMethods';
import { reactive, watch } from 'vue';

export default {
    name: "SectionForm",
    props: {
        formTitle: String,
        submitButtonText: String,
        initalData: Object,
    },
    setup(props, { emit }) {
        // initialising the data models
        const formData = reactive({
            name: '',
            unit: '',
        });

        const submitHandler = async () => {
            const dataObject = {
                "name": formData.name,
                "unit": formData.unit,
            }
            // backend request
            const response = await sectionMethods.addSection(dataObject)
            // console.log(response)
            emit('section-added', response)
        }

        // watching the initialData prop for changes
        watch(() => props.initalData, (newData) => {
            if (newData) {
                formData.value.name = newData.name;
                formData.value.unit = newData.unit;
            }
        },

            { immediate: true });

        const handleCancel = () => {
            emit('cancel');
        }
        return {
            formData,
            handleCancel,
            submitHandler

        }
    }
}
</script>

<style scoped></style>