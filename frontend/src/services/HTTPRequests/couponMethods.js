import {
  httpGetAllRequest,
  httpPostRequest,
  htttpPutRequest,
  httpDeleteRequest,
  httpGetRequest,
} from "../axios";

import { showSuccessToast } from "@/static/js/toasts";

export const couponMethods = {
  async fetchAllCoupons() {
    const data = await httpGetAllRequest("/coupon");
    return data;
  },
  async fetchAllUnexpiredCoupons() {
    const data = await httpGetAllRequest("/coupons");
    return data;
  },
  async fetchCouponFromCouponCode(coupon_code = null) {
    // console.log(coupon_code);
    const coupon_data = await httpGetRequest(`/coupons/${coupon_code}`);
    if (coupon_data) {
      showSuccessToast("Coupon Found");
    }
    return coupon_data;
  },
  async createCoupon(data) {
    const response = await httpPostRequest("/coupon", data);
    if (response) {
      showSuccessToast("Coupon Created Successfully");
    }
    return response;
  },

  async updateCoupon(coupon_id, data) {
    const response = await htttpPutRequest(`/coupon/${coupon_id}`, data);
    if (response) {
      showSuccessToast("Coupon Updated");
    }
    return response;
  },

  async deleteCoupon(coupon_id) {
    const response = await httpDeleteRequest(`/coupon/${coupon_id}`);

    if (response) {
      showSuccessToast("Coupon deleted successfully");
    }
    return response;
  },
};
