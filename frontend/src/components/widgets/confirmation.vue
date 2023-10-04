<template>
    <div class="modal-overlay" @click="$emit('close')">
        <div class="modal-content">
            <h3>Delete this {{ element?.name }} {{ deleteElement }} </h3>
            <button @click="$emit('confirm', element)" class="btn btn-danger float-end">Delete</button>
            <button @click="$emit('close')" class="btn float-end">Close</button>
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
</style>