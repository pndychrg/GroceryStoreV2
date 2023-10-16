<template>
    <div class="section-card">
        <div class="card-body text-start">
            <h5 class="card-title">
                {{ productData.name }}
            </h5>
            <h6 class="card-subtitle">
                {{ productData.section.name }}
            </h6>
            <hr>
            <p class="card-text">
                Available Amount : {{ productData.availableAmount }}
                <br>
                Rate : {{ productData.rate }}
                <br>
                Manufacture Date : {{ productData.manufactureDate }}
                <br>
                Expiry Date : {{
                    productData.expiryDate }}
            </p>
            <div class="d-flex justify-content-end">
                <button class="btn" @click="$emit('delete-product')">
                    <font-awesome-icon :icon="['fas', 'trash-can']" class="faa-horizontal animated-hover"
                        style="color: #c01c28;" />
                </button>
                <button class="btn" @click="$emit('edit-product')">
                    <font-awesome-icon :icon="['fas', 'pen-to-square']" class="faa-horizontal animated-hover" />
                </button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "ProductCard",
    props: {
        productData: Object,
    }
}
</script>

<style scoped></style>