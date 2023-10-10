import {
  httpDeleteRequest,
  httpGetAllRequest,
  httpPostRequest,
  htttpPutRequest,
} from "../axios";
import { showSuccessToast } from "@/static/js/toasts";
import { userStateStore } from "../stateManager";

export const sectionMethods = {
  async fetchAllSections() {
    try {
      const data = await httpGetAllRequest("/sections");
      return data;
    } catch (e) {
      console.log(e);
    }
  },
  async fetchAllSectionRequests() {
    try {
      const data = await httpGetAllRequest("/section/request");
      return data;
    } catch (e) {
      console.log(e);
    }
  },
  async addSection(data) {
    const store = userStateStore();
    // if the logged in user is admin
    if (store.user.role == "admin") {
      const response = await httpPostRequest("/section", data);
      if (response) {
        showSuccessToast("Section Added Successfully");
      }
      return response;
    } else {
      // the user is store manager so
      const response = await httpPostRequest("/section/request", data);
      if (response) {
        showSuccessToast("Section Request Added");
      }
      return response;
    }
  },

  async deleteSection(section) {
    const store = userStateStore();
    // if the registered user is admin
    if (store.user.role == "admin") {
      try {
        const response = await httpDeleteRequest("/section", {
          section_id: section.id,
        });
        if (response == true) {
          showSuccessToast("Section deleted Successfully ");
        }
        return response;
      } catch (e) {
        console.log(e);
      }
    } else {
      // send a post request to section requests with delete as request
      try {
        const data = {
          name: section.name,
          unit: section.unit,
          request: "delete",
          reg_section_id: section.id,
        };
        const response = await httpPostRequest("/section/request", data);
        if (response) {
          showSuccessToast("Section delete request added");
        }
        return response;
      } catch (e) {
        console.log(e);
      }
    }
  },

  async updateSection(section_id, data) {
    try {
      const response = await htttpPutRequest("/section", data, {
        section_id: section_id,
      });
      if (response) {
        showSuccessToast("Section Updated");
      }
      return response;
    } catch (e) {
      console.log(e);
      return null;
    }
  },
};
