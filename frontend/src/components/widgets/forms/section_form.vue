<template>
    <div class="section-form ">
        <h4>{{ formTitle }}</h4>
        <form @submit.prevent="submitHandler">
            <div class="form-group">
                <label for="sectionName">Section Name</label>
                <input v-model="formData.name" type="text" id="sectionName" required>
            </div>

            <div class="form-group">
                <label for="sectionUnit">Section Unit</label>
                <input v-model="formData.unit" type="text" id="sectionUnit" required>
            </div>

            <div class="form-actions">
                <button type="submit">
                    {{ submitButtonText }}
                </button>
                <button type="button" @click="handleCancel">
                    Cancel
                </button>
            </div>
        </form>

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