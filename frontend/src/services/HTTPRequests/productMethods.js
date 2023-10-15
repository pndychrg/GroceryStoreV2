import {
  httpDeleteRequest,
  httpGetAllRequest,
  httpPostRequest,
  htttpPutRequest,
} from "../axios";

import { showSuccessToast } from "@/static/js/toasts";
// import { userStateStore } from "../stateManager";

export const productMethods = {
  async fetchAllProducts() {
    const data = await httpGetAllRequest("/product");
    return data;
  },
  async addProduct(data) {
    // const store = userStateStore();
    const response = await httpPostRequest("/product", data);
    if (response) {
      showSuccessToast("Product Added Successfully");
    }
    return response;
  },

  async updateProduct(product_id, data) {
    const response = await htttpPutRequest("/product", data, {
      product_id: product_id,
    });
    if (response) {
      showSuccessToast("Product Updated");
    }
    return response;
  },

  async deleteProduct(product_id) {
    const response = await httpDeleteRequest("/product", {
      product_id: product_id,
    });
    if (response) {
      showSuccessToast("Product Deleted");
    }
    return response;
  },
};
