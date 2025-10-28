import axios from 'axios';
import { ClientContext } from '../context/ClientContext'; // Import ClientContext

// Create an Axios instance for API communication
const apiClient = axios.create({
  baseURL: '', // Force relative paths
  // The base URL is handled by the Vite proxy, so we can use relative paths like /api
  headers: {
    'Content-Type': 'application/json', // Default content type for requests
  },
  // You could add a timeout here if desired
  // timeout: 10000, 
});

// Below the `axios.create` block, add the request interceptor:
apiClient.interceptors.request.use(
  (config) => {
    // Dynamically get the current client ID from localStorage
    const currentClientId = localStorage.getItem('currentClientId');
    if (currentClientId) {
      config.headers['X-Client-ID'] = currentClientId;
    }
    const token = localStorage.getItem('authToken');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor to handle successful responses
apiClient.interceptors.response.use(
  (response) => {
    // Axios wraps the actual data in a `data` property. We return just the data.
    return response.data;
  },
  (error) => {
    // Centralized error handling for all API calls
    console.error('API Error:', error.response || error.message);

    // Optionally, you could check for specific status codes (e.g., 401 for unauthorized)
    // and trigger global actions like showing a notification or redirecting to login.
    // if (error.response && error.response.status === 401) {
    //   // handle unauthorized
    // }

    // If the error is an AbortError from AbortController, do not treat it as a critical failure
    if (axios.isCancel(error) || error.code === 'ERR_CANCELED') {
        // Propagate as a cancelled error for specific handling in components
        const cancelledError = new Error('Request was cancelled');
        cancelledError.name = 'CanceledError';
        return Promise.reject(cancelledError);
    }

    return Promise.reject(error); // Re-throw the error for component-specific handling
  }
);

export default apiClient;
