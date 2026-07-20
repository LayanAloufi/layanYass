import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// The API base URL is injected at build time via VITE_API_URL.
// During local dev, requests to /api are proxied to the Flask backend.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      "/api": "http://localhost:5000",
    },
  },
});
