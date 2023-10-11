import { showInfoToast } from "@/static/js/toasts";
import {
  httpDeleteRequest,
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
      return null;
    }
  },

  async approveManager(manager_id) {
    try {
      const response = await httpPostRequest("/unapproved", {
        manager_id,
      });
      if (response) {
        showInfoToast(response.msg);
      }
      return response;
    } catch (e) {
      console.log(e);
    }
  },

  async rejectManager(manager_id) {
    try {
      const response = await httpDeleteRequest("/unapproved", {
        manager_id: manager_id,
      });
      if (response) {
        showInfoToast(response.message);
      }
      return response;
    } catch (e) {
      console.log(e);
    }
  },
};
