import { showErrorToast } from "@/static/js/toasts";
import axios from "axios";
import { TokenService } from "./tokenService";

axios.defaults.baseURL = "http://127.0.0.1:5000";

// Function to update the auth header with the token
const updateAuthHeader = () => {
  axios.defaults.headers.common["Authorization"] =
    "Bearer " + TokenService.getToken();
};
updateAuthHeader();
export const httpGetAllRequest = async (path) => {
  try {
    const response = await axios.get(path);
    return response.data;
  } catch (e) {
    console.log(e);
    showErrorToast(e.response.data.msg);
    throw new Error(e.response.data.msg);
  }
};

export const httpGetRequest = async (path, params) => {
  try {
    const response = await axios.get(path, {
      params: params,
    });
    return response.data;
  } catch (e) {
    console.log(e);
    showErrorToast(e.response.data.msg);
    return null;
  }
};

export const httpPostRequest = async (path, data) => {
  try {
    const response = await axios.post(path, data);
    return response.data;
  } catch (e) {
    console.log(e.response);
    showErrorToast(e.response.data.msg);
    return null;
  }
};

export const htttpPutRequest = async (path, data, params) => {
  try {
    const response = await axios.put(path, data, {
      params: params,
    });
    return response.data;
  } catch (e) {
    console.log(e.response.data.msg);
    showErrorToast(e.response.data.msg);
    throw new Error(e.response.data.msg);
  }
};

export const httpDeleteRequest = async (path, params) => {
  try {
    const response = await axios.delete(path, {
      params: params,
    });
    return response.data;
  } catch (e) {
    console.log(e.response.data.msg);
    showErrorToast(e.response.data.msg);
    throw new Error(e.response.data.msg);
  }
};

export const updateToken = () => {
  updateAuthHeader();
};
