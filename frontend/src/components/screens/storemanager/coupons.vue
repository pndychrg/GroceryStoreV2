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
            <div class="card coupon-card" v-for="coupon in  coupons " :key="coupon.id"
                :class="{ expiredCoupon: coupon.hasExpired == 1 }">
                <CouponCard :coupon="coupon" @edit-coupon="showEditCouponForm(coupon)"
                    @delete-coupon="showDeleteConfirmation(coupon)" />
            </div>
        </div>

        <teleport to="#modal-root">
            <ConfirmationModal v-show="isDeleteModalShown" deleteElement="Coupon" :element="selectedCoupon"
                @close="hideDeleteModal" @confirm="deleteCoupon" />

            <CouponForm v-show="isCouponFormShown" :initialData="selectedCoupon" @close="closeCouponForm"
                @coupon-added="handleCouponUpdates" @coupon-edited="handleCouponUpdates" />
        </teleport>
    </div>
</template>

<script>
import { couponMethods } from '@/services/HTTPRequests/couponMethods';
import { onMounted, ref } from 'vue';
import CouponForm from "@/components/widgets/forms/coupon_form.vue";
import ConfirmationModal from "@/components/widgets/confirmation.vue"
import CouponCard from "@/components/widgets/cards/coupon_card.vue"

export default {

    name: "CouponsPage",
    components: {
        CouponForm,
        ConfirmationModal,
        CouponCard,
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


        const isDeleteModalShown = ref(false);
        const showDeleteConfirmation = (coupon) => {
            selectedCoupon.value = coupon;
            isDeleteModalShown.value = true;
        }

        const hideDeleteModal = () => {
            selectedCoupon.value = null;
            isDeleteModalShown.value = false;
        }

        const deleteCoupon = async () => {
            const response = await couponMethods.deleteCoupon(
                selectedCoupon.value.id
            );
            if (response) {
                fetchAllCoupons();
            }
        }

        onMounted(() => {
            fetchAllCoupons();
            // document.getElementById("addCouponButton").click()
        })
        return {
            coupons,
            showAddCouponForm,
            showEditCouponForm,
            closeCouponForm,
            isCouponFormShown,
            selectedCoupon,
            handleCouponUpdates,
            showDeleteConfirmation,
            hideDeleteModal,
            isDeleteModalShown,
            deleteCoupon
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

.expiredCoupon {
    box-shadow: 3px 3px 5px rgba(255, 25, 25, 0.2);
}
</style>