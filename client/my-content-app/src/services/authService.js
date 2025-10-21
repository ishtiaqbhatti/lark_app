// This is a new file. Create it with the following content:
import apiClient from './apiClient';

/**
 * Sends login request to the backend.
 * @param {string} password - The user's password.
 * @returns {Promise<object>} A promise that resolves to the login response (user and token).
 */
export const login = (password) => {
  return apiClient.post('/api/auth/login', { password });
};

/**
 * Sends logout request to the backend.
 * @returns {Promise<object>} A promise that resolves to the logout message.
 */
export const logout = () => {
  return apiClient.post('/api/auth/logout');
};
