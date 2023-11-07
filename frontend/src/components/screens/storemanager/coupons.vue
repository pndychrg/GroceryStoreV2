<template>
    <div>
        <h3>Coupons Page
            <span>
                <button class="btn btn-primary " type="button" @click="showAddCouponForm" id="addCouponButton">
                    Add Coupon
                </button>
            </span>
        </h3>
        <div class="row m-2 coupons-wrapper">
            <div class="card coupon-card" v-for="coupon in coupons" :key="coupon.id">
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
                        <button class="float-end btn btn-outline-secondary m-2" @click="showEditCouponForm(coupon)">
                            Edit <font-awesome-icon :icon="['fas', 'pen-to-square']"
                                class="faa-horizontal animated-hover" />
                        </button>

                        <button class="float-end m-2 btn btn-outline-danger">
                            Delete <font-awesome-icon :icon="['fas', 'trash-can']" class="faa-horizontal animated-hover" />
                        </button>

                    </div>
                </div>
            </div>
        </div>

        <teleport to="#modal-root">
            <CouponForm v-show="isCouponFormShown" :initialData="selectedCoupon" @close="closeCouponForm"
                @coupon-added="handleCouponUpdates" @coupon-edited="handleCouponUpdates" />
        </teleport>
    </div>
</template>

<script>
import { couponMethods } from '@/services/HTTPRequests/couponMethods';
import { onMounted, ref } from 'vue';
import CouponForm from "@/components/widgets/forms/coupon_form.vue";
export default {

    name: "CouponsPage",
    components: {
        CouponForm,
    },
    setup() {
        const coupons = ref([]);
        const fetchAllCoupons = async () => {
            const fetchedCoupons = await couponMethods.fetchAllCoupons();
            coupons.value = fetchedCoupons;
        }

        const selectedCoupon = ref(null);
        const isCouponFormShown = ref(false);
        const showAddCouponForm = () => {
            isCouponFormShown.value = true;
        }
        const showEditCouponForm = (coupon) => {
            selectedCoupon.value = coupon;
            isCouponFormShown.value = true;
        }

        const closeCouponForm = () => {
            selectedCoupon.value = null;
            isCouponFormShown.value = false;
        }

        const handleCouponUpdates = () => {
            selectedCoupon.value = null;
            isCouponFormShown.value = false;
            fetchAllCoupons();
        }

        onMounted(() => {
            fetchAllCoupons();
            document.getElementById("addCouponButton").click()
        })
        return {
            coupons,
            showAddCouponForm,
            showEditCouponForm,
            closeCouponForm,
            isCouponFormShown,
            selectedCoupon,
            handleCouponUpdates,
        }
    }
}
</script>

<style scoped>
.coupons-wrapper {
    padding: 40px 55px 45px 55px;
}

.coupon-card {
    border: none;
    box-shadow: 3px 3px 5px rgba(35, 35, 58, 0.2);
    border-radius: 12px;
    max-width: 540px;
    margin: 10px;
}
</style>