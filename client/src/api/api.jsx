// src/api/api.jsx
import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:5000", // your Flask backend
  withCredentials: true,           // to send cookies/session
});

export default API;
