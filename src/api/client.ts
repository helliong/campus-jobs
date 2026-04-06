import axios from "axios";

export const api = axios.create({
  baseURL: "http://localhost:8000",
});

api.interceptors.request.use((config) => {
  const lang = localStorage.getItem("lang") || "en";
  config.headers["Accept-Language"] = lang;
  return config;
});