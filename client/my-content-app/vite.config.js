import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000, // Frontend will run on port 3000
    proxy: {
      // Proxy API requests to the FastAPI backend
      '/api': {
        target: process.env.VITE_API_URL || 'http://localhost:8000', // Backend address
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''), // Strip /api prefix
      },
    },
  },
});
