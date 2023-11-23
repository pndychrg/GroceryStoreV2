import {
  httpDeleteRequest,
  httpGetAllRequest,
  httpPostRequest,
  htttpPutRequest,
  httpPostImageRequest,
  httpGetRequest,
} from "../axios";

import { showSuccessToast } from "@/static/js/toasts";
// import { userStateStore } from "../stateManager";

export const productMethods = {
  async fetchAllProducts() {
    const data = await httpGetAllRequest("/product");
    return data;
  },

  async fetchRecentProducts(limit) {
    const data = await httpGetAllRequest(`/product/${limit}`);
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

  async deleteProduct(product) {
    const response = await httpDeleteRequest("/product", {
      product_id: product.id,
    });
    if (response) {
      showSuccessToast("Product Deleted");
    }
    return response;
  },

  async addProductImage(product, image) {
    const formData = new FormData();
    formData.append("image", image);
    const response = await httpPostImageRequest(
      `/product/img?product_id=${product.id}`,
      formData
    );
    if (response) {
      showSuccessToast("Image Updated Successfully");
    }
    return response;
  },

  async searchForProduct(data) {
    console.log("searchMethod");
    console.log(data.section_id);
    const response = await httpGetRequest("/product/search", data);
    return response;
  },
};
