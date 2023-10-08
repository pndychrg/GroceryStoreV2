import { showSuccessToast } from "@/static/js/toasts";
import {
  // httpDeleteRequest,
  httpGetAllRequest,
  httpPostRequest,
  // httpPostRequest,
} from "../axios";

export const unapprovedManagersMethods = {
  async fetchAllUnapprovedManagers() {
    try {
      const data = await httpGetAllRequest("/unapproved");
      return data;
    } catch (e) {
      console.log(e);
    }
  },

  async approveManager(manager_id) {
    try {
      const response = await httpPostRequest("/unapproved", {
        manager_id,
      });
      if (response) {
        showSuccessToast(response.message);
      }
      return response;
    } catch (e) {
      console.log(e);
    }
  },
};
