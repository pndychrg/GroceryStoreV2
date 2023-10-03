<template>
    <div class="confirmationModal">
        <div class="modal-box">
            <h3>{{ title }}</h3>
            <!-- The modal component body -->
            <button @click="$emit('confirm')">Yea Nigga</button>
            <button @click="$emit('cancel')">No Fuck You </button>
        </div>
    </div>
</template>

<script>
import { defineEmits } from 'vue';

export default {
    name: "ConfirmationDialog",
    props: {
        title: String,
    },
    setup() {
        const emit = defineEmits(['confirm', 'cancel'])
        return {
            emit
        }
    }
}
</script>

<style scoped>
.my-modal {
    display: flex;
    align-items: center;
    justify-content: center;
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background-color: #cecece89;
    transition-property: background-color, border-color, color, fill, stroke,
        opacity, box-shadow, transform;
    transition-duration: 0.15s;
    transition-duration: 0.2s;
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 100;
}
</style>
