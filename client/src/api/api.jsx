import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:5000", // ✅ Must match the Flask host now
  withCredentials: true             // ✅ Required to send cookies
});

export default API;
