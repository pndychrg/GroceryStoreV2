import {
  // httpDeleteRequest,
  httpGetAllRequest,
  // httpPostRequest,
} from "../axios";

export const unapprovedManagersMethods = {
  async fetchAllUnapprovedManagers() {
    try {
      const data = await httpGetAllRequest("/notapproved");
      return data;
    } catch (e) {
      console.log(e);
    }
  },
};
