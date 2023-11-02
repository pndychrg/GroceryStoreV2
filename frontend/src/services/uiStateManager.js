import { defineStore } from "pinia";

export const UIStateStore = defineStore("ui-store", {
  state: () => {
    const isModalShown = false;
    return {
      isModalShown,
    };
  },
  actions: {
    toggleModal() {
      console.log("toggleModal");
      this.isModalShown = !this.isModalShown;

      const bodyTag = document.getElementById("body");
      if (this.isModalShown) {
        bodyTag.style.overflow = "hidden";
      } else {
        bodyTag.style.removeProperty("overflow");
      }
      window.scrollTo(0, 0);
    },
  },
});
