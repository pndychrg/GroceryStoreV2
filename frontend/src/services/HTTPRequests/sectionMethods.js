import {
  httpDeleteRequest,
  httpGetAllRequest,
  httpPostRequest,
} from "../axios";
import { showSuccessToast } from "@/static/js/toasts";

export const sectionMethods = {
  async fetchAllSections() {
    try {
      const data = await httpGetAllRequest("/sections");
      return data;
    } catch (e) {
      console.log(e);
    }
  },

  async addSection(data) {
    const response = await httpPostRequest("/section", data);
    if (response) {
      showSuccessToast("Section Added Successfully");
    }
    return response;
  },

  async deleteSection(section_id) {
    try {
      const response = await httpDeleteRequest("/section", {
        section_id: section_id,
      });
      if (response == true) {
        showSuccessToast("Section deleted Successfully ");
      }
      return response;
    } catch (e) {
      console.log(e);
    }
  },
};
