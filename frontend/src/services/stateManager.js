import { defineStore } from "pinia";
import axios from "axios";
import router from "./router";
import { TokenService } from "./tokenService";
import { showSuccessToast, showErrorToast } from "@/static/js/toasts";
import { toRaw } from "vue";
import { httpGetRequest, httpPostImageRequest, updateToken } from "./axios";

export const userStateStore = defineStore("store", {
  state: () => {
    const user = null;
    const profile_img = null;
    const isAuthenticated = false;
    return {
      user,
      isAuthenticated,
      profile_img,
    };
  },

  actions: {
    async checkTokenOnAppStart() {
      const token = TokenService.getToken();
      if (token) {
        this.user = JSON.parse(atob(token.split(".")[1])).sub;
        this.isAuthenticated = true;
      }
    },

    async loginUser(username, password) {
      const data = {
        username,
        password,
      };
      // try and catch block
      try {
        // post request with axios
        const response = await axios.get("/user", {
          params: data,
        });

        const token = response.data.token;
        //saving the token in localStorage
        // extracting user from token
        this.user = JSON.parse(atob(token.split(".")[1])).sub;
        TokenService.saveToken(token);
        this.isAuthenticated = true;
        updateToken();
        console.log(toRaw(this.user));
        await this.getUserImage();
        // different route for notApproved store manager
        if (this.user.role == "notApproved") {
          showSuccessToast("Your application is not still approved");
          router.push("/notApproved");
        } else {
          showSuccessToast("Welcome " + this.user.name);
          // console.log(toRaw(this.user));
          router.push("/");
        }
      } catch (e) {
        console.log(e);
        showErrorToast(e.response.data.msg);
        console.log(e.response.data.msg);
      }
    },

    async registerUser(name, username, email, password, role = "user") {
      const data = {
        name,
        username,
        email,
        password,
        role,
      };
      try {
        const response = await axios.post("/user", data);
        // extracting and saving the token
        TokenService.saveToken(response.data.token);
        // extracting user from token
        this.user = JSON.parse(atob(response.data.token.split(".")[1])).sub;
        console.log(this.user);
        this.isAuthenticated = true;
        console.log(this.user);
        // updating the user image
        await this.getUserImage();
        // till above is fine but now changing the toast and router for notApproved Store Manager
        if (role == "storeManager") {
          showSuccessToast(`Your application is submitted. ${this.user.name}`);
          // push to not approved screen
          router.push("/notApproved");
        } else {
          showSuccessToast(`Welcome to Grocery Store. ${this.user.name}`);
          router.push("/");
        }
      } catch (e) {
        showErrorToast(e.response.data.msg);
      }
    },

    async logoutUser() {
      // deleting the token from storage
      TokenService.removeToken();
      // updating the user state
      this.user = null;
      this.isAuthenticated = false;
      router.push("/login");
    },

    async setUserImage(image) {
      const formData = new FormData();
      formData.append("image", image);
      const response = await httpPostImageRequest("/user/img", formData);
      // if (response) {
      //   showSuccessToast("Profile Image Updated");
      // }
      this.profile_img = response.img;
      // return response;
    },

    async getUserImage() {
      const response = await httpGetRequest("user/img");
      this.profile_img = response.img;
      // console.log(this.image);
    },

    async updateUser(formData) {
      try {
        const response = await axios.put("/user", formData);
        // this response will update the user data
        TokenService.saveToken(response.data.token);
        // extracting user from token
        this.user = JSON.parse(atob(response.data.token.split(".")[1])).sub;
        console.log(this.user);
        return true;
      } catch (e) {
        console.log(e);
        showErrorToast(e.response.data.msg);
      }
    },

    async updateUserPassword(data) {
      try {
        const response = await axios.put("/user/password", data);
        if (response) {
          showSuccessToast("Password Updated Successfully");
        }
        return response;
      } catch (e) {
        console.log(e);
        showErrorToast(e.response.data.msg);
        return false;
      }
    },

    async forgotPassword() {
      try {
        const response = await axios.post("/user/password");
        if (response) {
          showSuccessToast("Password sent to mail");
        }
        return response;
      } catch (e) {
        console.log(e);
        showErrorToast("Error Occured");
      }
    },
  },
});
