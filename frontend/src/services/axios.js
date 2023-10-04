import { showErrorToast } from "@/static/js/toasts";
import axios from "axios";
import { TokenService } from "./tokenService";

axios.defaults.baseURL = "http://127.0.0.1:5000";
axios.defaults.headers.common["Authorization"] =
  "Bearer " + TokenService.getToken();

export const httpGetAllRequest = async (path) => {
  try {
    const response = await axios.get(path);
    return response.data;
  } catch (e) {
    console.log(e);
    showErrorToast(e.response.data.message);
    throw new Error(e.response.data.message);
  }
};

export const httpPostRequest = async (path, data) => {
  try {
    const response = await axios.post(path, data);
    return response.data;
  } catch (e) {
    console.log(e.response.data.message);
    showErrorToast(e.response.data.message);
    return null;
  }
};

export const httpDeleteRequest = async (path, params) => {
  try {
    const response = await axios.delete(path, {
      params: params,
    });
    return response.data;
  } catch (e) {
    console.log(e.response.data.message);
    showErrorToast(e.response.data.message);
    throw new Error(e.response.data.message);
  }
};
