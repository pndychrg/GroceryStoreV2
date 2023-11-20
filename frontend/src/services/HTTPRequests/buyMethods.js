import { showSuccessToast } from "@/static/js/toasts";
import { httpPostRequest, httpGetAllRequest } from "../axios";

export const buyMethods = {
  async buyAllCartItems(coupon_id) {
    // console.log(coupon_id);
    const response = await httpPostRequest(
      `/buy${coupon_id ? "/" + coupon_id : ""}`
    );
    if (response) {
      showSuccessToast("All Items are bought successfully");
    }
    return response;
  },

  async getAllBills() {
    const response = await httpGetAllRequest("/buy");
    if (response) {
      return response;
    } else {
      return [];
    }
  },
};
