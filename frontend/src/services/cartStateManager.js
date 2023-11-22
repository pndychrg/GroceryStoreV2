import { defineStore } from "pinia";
import { cartMethods } from "./HTTPRequests/cartMethods";
// import { computed } from "vue";
// import { userStateStore } from "./stateManager";

// const userStore = userStateStore();
export const CartStateStore = defineStore("cart-store", {
  state: () => {
    const cart = null;
    const sum = null;

    return {
      cart,
      sum,
    };
  },
  actions: {
    async fetchCartForUser() {
      const cartData = await cartMethods.fetchAllCartProducts();
      if (cartData != null) {
        this.cart = cartData.cart;
        this.sum = cartData.sum;
      }
    },

    async addProductToCart(dataObject) {
      const response = await cartMethods.addToCart(dataObject);
      return response;
    },

    async removeCartItem(cartItem) {
      const response = await cartMethods.deleteCartProduct(cartItem);
      //   updating the cart again
      this.fetchCartForUser();
      return response;
    },
  },
});
