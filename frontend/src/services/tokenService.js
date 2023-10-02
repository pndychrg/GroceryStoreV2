export const TokenService = {
  // key for storing the token in local storage
  TOKEN_KEY: "jwt_token",

  // get the jwt token
  getToken() {
    return localStorage.getItem(this.TOKEN_KEY);
  },

  // setting the jwt token
  saveToken(token) {
    localStorage.setItem(this.TOKEN_KEY, token);
  },

  // remove the token
  removeToken() {
    localStorage.removeItem(this.TOKEN_KEY);
  },
};
