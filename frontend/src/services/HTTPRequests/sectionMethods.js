import { httpGetRequest, httpPostRequest } from "../axios";
import { showSuccessToast } from "@/static/js/toasts";

export const sectionMethods = {
  async fetchAllSections() {
    try {
      const data = await httpGetRequest("/sections");
      return data;
    } catch (e) {
      console.log(e.response);
    }
  },

  async addSection(data) {
    try {
      const response = await httpPostRequest("/section", data);
      showSuccessToast("Section Added Successfully");
      return response;
    } catch (e) {
      console.log(e);
    }
  },
};
