<template>
    <div class="modal-overlay">
        <div class="modal-content p-3">
            <h1>{{ bill.id }}</h1>
        </div>
    </div>
</template>

<script>
export default {
    name: "BillDetailsModal",
    props: {
        bill: Object
    }
}
</script>

<style scoped>
@import "@/static/css/modal.css"
</style>