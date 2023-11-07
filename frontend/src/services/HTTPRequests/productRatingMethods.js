import { httpGetRequest, httpPostRequest, httpDeleteRequest } from "../axios";

import { showSuccessToast } from "@/static/js/toasts";

export const productRatingMethods = {
  async rateProduct(product_id, rating, comment) {
    const response = await httpPostRequest("/product/rating", {
      product_id: product_id,
      rating: rating,
      comment: comment,
    });

    if (response) {
      // TODO try to show the rating in the message
      showSuccessToast("Product rated ");
    }
    return response;
  },

  async getProductRating(product) {
    const response = await httpGetRequest(`/product/rating/${product.id}`);

    return response;
  },

  async removeProductRating(product) {
    const response = await httpDeleteRequest(`/product/rating/${product.id}`);

    if (response) {
      // TODO try to show the rating in the message
      showSuccessToast("Product Rating Deleted");
    }

    return response;
  },
};
