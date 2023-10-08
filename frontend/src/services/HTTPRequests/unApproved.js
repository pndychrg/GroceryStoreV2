import {
  // httpDeleteRequest,
  httpGetAllRequest,
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
};
