import { showSuccessToast } from "@/static/js/toasts";
import { httpDeleteRequest, httpGetRequest } from "../axios";

export const sectionRequestMethodsForAdmin = {
  async approveSectionRequest(section_id) {
    const response = await httpGetRequest("/section/approve", {
      section_id: section_id,
    });
    if (response) {
      showSuccessToast("Section Request Approved");
    }
    return response;
  },

  async rejectSectionRequest(section_id) {
    const response = await httpDeleteRequest("/section/approve", {
      section_id: section_id,
    });
    if (response) {
      showSuccessToast("Section Request Rejected");
    }
    return response;
  },
};
