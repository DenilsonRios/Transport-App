import axios from './axios'


export const registerRequest =  (user) => axios.post(`/create_account/`, user);
export const loginRequest = (user) => axios.post(`/login/`, user);