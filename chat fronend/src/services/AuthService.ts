import axios from "axios";
import { UserModel } from "../models/User";


class AuthService {
  setUserInLocalStorage(data: UserModel) {
    localStorage.setItem("user", JSON.stringify(data));
  }

  async login(email: string, password: string): Promise<UserModel> {
    const response = await axios.post("http://127.0.0.1:8000/auth/signin/", { email, password });
    if (!response.data.access) {
      return response.data;
    }
    const userResponse = await axios.get("http://127.0.0.1:8000/users/me/", { headers: { Authorization: 'Bearer ' + response.data.access } });
    let user = {
      id: userResponse.data.id,
      first_name: userResponse.data.first_name,
      token: response.data.access
    }
    this.setUserInLocalStorage(user);
    console.log(user);
    return user;
  }

  logout() {
    localStorage.removeItem("user");
  }

  getCurrentUser() {
    const user = localStorage.getItem("user")!;
    return JSON.parse(user);
  }
}

export default new AuthService();
