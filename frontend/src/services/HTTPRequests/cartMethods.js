import {
  httpDeleteRequest,
  httpGetAllRequest,
  httpPostRequest,
  htttpPutRequest,
} from "../axios";

import { showSuccessToast } from "@/static/js/toasts";

export const cartMethods = {
  async fetchAllCartProducts() {
    const data = await httpGetAllRequest("/cart");
    return data;
  },
  async addToCart(data) {
    const response = await httpPostRequest("/cart", data);

    if (response) {
      showSuccessToast("Product added to card successfully");
    }
    return response;
  },

  async updateCartProductAmount(data) {
    const response = await htttpPutRequest("/cart", data);
    if (response) {
      showSuccessToast("Product Updated Successfully");
      return response;
    }
  },

  async deleteCartProduct(cart) {
    const response = await httpDeleteRequest("/cart", {
      product_id: cart.product.id,
    });
    if (response) {
      showSuccessToast("Product Deleted");
    }
    return response;
  },
};
