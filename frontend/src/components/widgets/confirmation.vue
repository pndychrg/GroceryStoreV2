<template>
    <div class="modal-overlay" @click="$emit('close')">
        <div class="modal-content">
            <h3>Delete this {{ element?.name }} {{ deleteElement }} </h3>
            <button @click="$emit('close')" class="btn">Close</button>
            <button @click="$emit('confirm', element)" class="btn btn-danger">Delete</button>
        </div>
    </div>
</template>
  
<script>
export default {
    // eslint-disable-next-line vue/multi-word-component-names
    name: "Modal",
    emits: ["close", "confirm"],
    props: {
        deleteElement: String,
        element: Object,
    }
};
</script>
  
<style>
.modal-overlay {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    display: grid;
    justify-content: center;
    align-items: center;
    background-color: rgba(0, 0, 0, 0.3);
}

.modal-content {
    background: white !important;
    font-family: "Fondamento", cursive;
    padding: 20px;
    border-radius: 12px !important;
    border: 2px;
    display: inline-block;
    /* min-height: 300px; */
    margin: 1rem;
    position: relative;
    /* min-width: 300px; */
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.26), 0 3px 6px rgba(0, 0, 0, 0.36);
    justify-self: center;
}
</style>