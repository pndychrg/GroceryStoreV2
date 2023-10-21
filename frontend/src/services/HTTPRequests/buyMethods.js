import { showSuccessToast } from "@/static/js/toasts";
import { httpPostRequest } from "../axios";

export const buyMethods = {
  async buyAllCartItems() {
    const response = await httpPostRequest("/buy", null);
    if (response) {
      showSuccessToast("All Items are bought successfully");
    }
    return response;
  },
};
