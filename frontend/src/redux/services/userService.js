// Config
import { baseUrl, requestConfig } from "../../config/config";
import axios from "axios";

const getUserData = async (userId) => {
  // const config = requestConfig(`${baseUrl}/users/${userId}`, "GET", null);
  const config = requestConfig(`${baseUrl}/users/`, "GET", null);
  try {
    const res = await axios(config);
    console.log('3', res)
    return res.data;
  } catch (error) {
    console.log(error)
    if(error.response.status=401) {
        try {
          let config = requestConfig(`${baseUrl}/token/refresh`, "POST", null);
          let res = await axios(config);
          console.log('1', res)
          try {
            config = requestConfig(`${baseUrl}/users/`, "GET", null);
            res = await axios(config);
            console.log('2', res)

            return res.data;
          } catch (error) {
              return error.response.data;
          }
      }catch (error) {
        return error.response.data;
      }
    } else {
      return error.response.data;
    }
  }
};

const userService = { getUserData };

export default userService;
