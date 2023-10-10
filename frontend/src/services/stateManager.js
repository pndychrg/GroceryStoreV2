import { defineStore } from "pinia";
import axios from "axios";
import router from "./router";
import { TokenService } from "./tokenService";
import { showSuccessToast, showErrorToast } from "@/static/js/toasts";
import { toRaw } from "vue";
import { updateToken } from "./axios";

export const userStateStore = defineStore("store", {
  state: () => {
    const user = null;
    const isAuthenticated = false;
    return {
      user,
      isAuthenticated,
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
        showErrorToast(e.response.data.msg);
        console.log(e.response.data.msg);
      }
    },

    async registerUser(name, username, password, role = "user") {
      const data = {
        name,
        username,
        password,
        role,
      };
      try {
        const response = await axios.post("/user", data);
        // extracting and saving the token
        TokenService.saveToken(response.data.token);
        // extracting user from token
        this.user = JSON.parse(atob(response.data.token.split(".")[1])).sub;
        this.isAuthenticated = true;
        console.log(this.user);

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
  },
});
