import {
  httpGetAllRequest,
  httpPostRequest,
  httpDeleteRequest,
} from "../axios";

import { showErrorToast, showSuccessToast } from "@/static/js/toasts";

export const favouriteMethods = {
  async fetchAllFavouriteForUser() {
    const data = await httpGetAllRequest("/product/favourite");
    return data;
  },

  async addToFavourite(product_id) {
    const response = await httpPostRequest(`/product/favourite/${product_id}`);

    if (response) {
      showSuccessToast("Product added to favourites");
    }
  },

  async removeFromFavourite(product_id) {
    const response = await httpDeleteRequest(
      `/product/favourite/${product_id}`
    );

    if (response) {
      showErrorToast("Product removed from favourites");
    }
  },
};
