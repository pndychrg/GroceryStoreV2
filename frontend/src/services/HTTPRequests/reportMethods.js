import { downloadItem, httpGetImageRequest } from "../axios";
import { showSuccessToast } from "@/static/js/toasts";

export const reportMethods = {
  async downloadReportCSV() {
    const response = await downloadItem(
      "/report/exportCSVReports",
      "Download Reports Zip File"
    );
    console.log(response);
    if (response) {
      showSuccessToast("Report Fetched Successfully");
    }
    return response;
  },

  async getCouponGraph() {
    const response = await httpGetImageRequest("/report/coupon");
    return response;
  },

  async getFavProductGraph() {
    const response = await httpGetImageRequest("/report/product/favourite");
    return response;
  },

  async getBoughtProductGraph() {
    const response = await httpGetImageRequest("/report/product/buy");
    return response;
  },
};
