<template>
    <div class="modal-overlay" @click="closeCouponForm($event)">
        <div class="modal-content text-start">
            <div class="modal-header">
                <h4 class="modal-title">
                    {{ formTexts.title }}
                </h4>
            </div>
            <form class="modal-body" @submit.prevent="handleSubmit">
                <div class="form-group">
                    <label for="couponCode">Coupon Code</label>
                    <input type="text" v-model="formData.coupon_code" id="couponCode" class="form-control mb-2" required>
                </div>
                <div class="form-group">
                    <label for="discount">Discount</label>
                    <input type="number" v-model.number="formData.discount" class="form-control mb-2" required min="0"
                        max="100">
                </div>
                <div class="form-group">
                    <label for="expiryDate">Expiry Date</label>
                    <input type="date" v-model="formData.expiryDate" class="form-control mb-2" :min="today" id="expirDate">
                </div>
                <div class="form-actions modal-footer">
                    <button type="button" @click="closeCouponForm(null)" class="btn btn-outline-danger ms-2">
                        Cancel
                    </button>
                    <button type="submit" class="btn btn-outline-success ms-2">
                        {{ formTexts.buttonText }}
                    </button>

                </div>
            </form>
        </div>
    </div>
</template>

<script>
import { couponMethods } from '@/services/HTTPRequests/couponMethods';
import { computed, reactive, watch } from 'vue';


export default {
    name: "CouponForm",
    props: {
        initialData: Object,
    },
    setup(props, { emit }) {
        const today = new Date().toISOString().split('T')[0];

        const formData = reactive({
            coupon_code: "",
            discount: null,
            expiryDate: null,
        });

        const clearForm = () => {
            Object.assign(formData, {
                coupon_code: "",
                discount: null,
                expiryDate: null,
            })
        }
        const closeCouponForm = ($event = null) => {
            if ($event === null) {
                clearForm();
                emit('close');
            } else {
                if ($event.target.classList.contains('modal-overlay')) {
                    clearForm();
                    emit('close');
                }
            }
        }
        // const handleCancel = () => {
        //     clearForm()
        //     emit('close');
        // }

        const formTexts = computed(() => {
            if (props.initialData == null) {
                return {
                    title: "Add Coupon",
                    buttonText: "Submit",
                }
            } else {
                return {
                    title: "Edit Coupon",
                    buttonText: "Update"
                }
            }
        });

        const handleSubmit = async () => {
            // console.log(props.initialData);
            const dataObject = {
                "coupon_code": formData.coupon_code,
                "discount": formData.discount,
                "expiryDate": formData.expiryDate,
            };
            if (props.initialData == null) {
                const response = await couponMethods.createCoupon(
                    dataObject
                );
                if (response) {
                    clearForm();
                    emit('coupon-added');
                }
            } else {
                const response = await couponMethods.updateCoupon(
                    props.initialData.id,
                    dataObject
                );
                if (response) {
                    clearForm();
                    emit('coupon-edited');
                }
            }
        }

        watch(() => props.initialData, (newData) => {
            if (newData) {
                formData.coupon_code = newData.coupon_code;
                formData.expiryDate = newData.expiryDate;
                formData.discount = newData.discount;
            }
        })

        return {
            formData,
            formTexts,
            handleSubmit,
            today,
            closeCouponForm
        }
    }
}
</script>

<style scoped>
@import "@/static/css/modal.css";


.modal-content {
    max-width: 90% !important;
}
</style>