import { defineStore } from "pinia";
import axios from "axios";
import router from "./router";
import { TokenService } from "./tokenService";
import { showSuccessToast, showErrorToast } from "@/static/js/toasts";

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
        TokenService.saveToken(token);

        // extracting user from token
        this.user = JSON.parse(atob(token.split(".")[1])).sub;
        this.isAuthenticated = true;
        showSuccessToast("Welcome " + this.user.name);
        // console.log(toRaw(this.user));
        router.push("/");
      } catch (e) {
        showErrorToast(e.response.data.message);
        console.log(e.response.data.message);
      }
    },

    async registerUser(name, username, password) {
      const data = {
        name,
        username,
        password,
      };
      try {
        const response = await axios.post("/user", data);
        // extracting and saving the token
        TokenService.saveToken(response.data.token);
        // extracting user from token
        this.user = JSON.parse(atob(response.data.token.split(".")[1])).sub;
        this.isAuthenticated = true;
        console.log(this.user);
        showSuccessToast(`Welcome to Grocery Store. ${this.user.name}`);
        router.push("/");
      } catch (e) {
        showErrorToast(e.response.data.message);
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