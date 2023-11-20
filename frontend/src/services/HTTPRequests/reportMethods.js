import { downloadItem } from "../axios";
import { showSuccessToast } from "@/static/js/toasts";

export const reportMethods = {
  async downloadReportCSV() {
    const response = await downloadItem(
      "/report/exportCSVReports",
      "Download Reports Zip File"
    );
    if (response) {
      showSuccessToast("Report Fetched Successfully");
    }
    return response;
  },
};
