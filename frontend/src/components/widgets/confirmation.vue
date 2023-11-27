<template>
    <div class="modal-overlay" @click="$emit('close')">
        <div class="modal-content">
            <h5>Delete this {{ element?.name }} {{ deleteElement }} </h5>
            <button @click="$emit('confirm', element)" class="btn btn-danger float-end m-2">Delete</button>
            <button @click="$emit('close')" class="btn float-end btn-outline-secondary m-2">Close</button>
        </div>
    </div>
</template>
  
<script>
export default {
    name: "ConfirmationModal",
    emits: ["close", "confirm"],
    props: {
        deleteElement: String,
        element: Object,
    }
};
</script>
  
<style scoped>
@import "@/static/css/modal.css";

.modal-content {
    width: 40%;
}
</style>