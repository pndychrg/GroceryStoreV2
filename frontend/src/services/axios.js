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
    // throw new Error(e.response.data.msg);
    return null;
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
    showErrorToast(e?.response?.data.msg ?? "Error Occured");
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
    console.log(e.response.data.msg);
    showErrorToast(e.response.data.msg);
    // throw new Error(e.response.data.msg);
    return null;
  }
};

export const httpPostImageRequest = async (path, formData) => {
  try {
    const response = await axios.post(path, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  } catch (e) {
    console.log(e.response.data.msg);
    showErrorToast(e.response.data.msg);
    return null;
  }
};

export const updateToken = () => {
  updateAuthHeader();
};

export const downloadItem = async (path, label) => {
  try {
    const response = await axios.get(path, { responseType: "blob" });
    if (response) {
      const blob = new Blob([response.data]);
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = label;
      link.click();
      URL.revokeObjectURL(link.href);
      return true;
    }
  } catch (e) {
    console.log(e);
    return false;
  }
};
export const httpDownloadRequest = async (path) => {
  try {
    const response = await axios.get(path, { responseType: "blob" });
    const blob = new Blob([response.data], {
      type: response.headers["Content-Type"],
    });
    return blob;
  } catch (error) {
    console.log(error);
    return null;
  }
};

export default axios;
