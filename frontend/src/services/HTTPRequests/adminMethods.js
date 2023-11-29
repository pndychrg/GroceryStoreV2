import { httpGetRequest } from "../axios";
import { showSuccessToast } from "@/static/js/toasts";

export const adminMethods = {
  async sendReportToAllUser() {
    const response = await httpGetRequest("/admin/user/report");
    if (response) {
      showSuccessToast("Report Sent to all Users");
    }

    return response;
  },

  async sendRemainderToUser() {
    const response = await httpGetRequest("/admin/user/unvisited");
    if (response) {
      showSuccessToast("Remainder sent to all Users");
    }
    return response;
  },
};
