<template>
    <div class="card-body text-start">
        <h5 class="card-title">
            Coupon Code : <span class="float-end " style="font-weight: bold;">{{ coupon.coupon_code }}</span>
        </h5>
        <p class="card-text">
            Discount : <span class="float-end" style="font-weight: bold;">{{ coupon.discount }}%</span>
            <br>
            Expiry Date : <span class="float-end" style="font-weight: bold;">
                {{ coupon.expiryDate ?? 'None' }}
            </span>
        </p>
        <div class="">
            <button v-if="coupon.hasExpired == 1" class="float-start btn btn-danger ms-2" disabled>
                Expired
            </button>

            <button class="float-end btn btn-outline-secondary m-2" @click="$emit('edit-coupon')">
                Edit <font-awesome-icon :icon="['fas', 'pen-to-square']" class="faa-horizontal animated-hover" />
            </button>

            <button class="float-end m-2 btn btn-outline-danger" @click="$emit('delete-coupon')">
                Delete <font-awesome-icon :icon="['fas', 'trash-can']" class="faa-horizontal animated-hover" />
            </button>
        </div>
    </div>
</template>

<script>
export default {
    name: "CouponCard",
    props: {
        coupon: Object,
    }
}
</script>

<style scoped></style>