import axios from "axios";

const baseURL = import.meta.env.VITE_API_URL;
if (!baseURL && import.meta.env.PROD) {
  throw new Error("VITE_API_URL must be set in production builds");
}

export const api = axios.create({
  baseURL: baseURL ?? "http://localhost:8000",
});
