<template>
    <div class="modal-overlay" @click="$emit('close')">
        <div class="modal-content">
            <h3>Buy Confirmation</h3>
            <h5>Confirm and pay for all the goods <br>
                TOTAL ORDER SUM = {{ finalAmount }}
            </h5>
            <button @click="$emit('confirm')" class="btn btn-success float-end">Buy</button>
            <button @click="$emit('close')" class="btn float-end">Close</button>
        </div>
    </div>
</template>

<script>
export default {
    name: "BuyConfirmationModal",
    emits: [
        "close",
        "confirm"
    ],
    props: {
        finalAmount: Number
    }
}
</script>

<style scoped>
@import "@/static/css/modal.css";

.modal-content {
    width: 50%;
}
</style>