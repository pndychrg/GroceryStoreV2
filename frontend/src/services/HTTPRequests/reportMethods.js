import { downloadItem } from "../axios";
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
};
