import axios from "axios";

export const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

api.interceptors.request.use((config) => {
  const lang = localStorage.getItem("lang") || "en";
  config.headers["Accept-Language"] = lang;
  return config;
});