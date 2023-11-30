import { downloadItem, httpDownloadRequest, httpGetRequest } from "../axios";
import { showSuccessToast } from "@/static/js/toasts";

export const reportMethods = {
  async downloadReportCSV() {
    const response = await downloadItem(
      "/report/exportCSVReports",
      "reports.zip"
    );
    console.log(response);
    if (response) {
      showSuccessToast("Report Fetched Successfully");
    }
    return response;
  },

  async getCouponGraph() {
    const response = await httpDownloadRequest("/report/coupon");
    return response;
  },

  async getFavProductGraph() {
    const response = await httpDownloadRequest("/report/product/favourite");
    return response;
  },

  async getBoughtProductGraph() {
    const response = await httpDownloadRequest("/report/product/buy");
    return response;
  },

  async getManagementData() {
    const response = await httpGetRequest("/report/data");
    return response;
  },

  async downloadPDFReport() {
    const response = await downloadItem("/report/user/pdf", "report.pdf");
    return response;
  },
};
