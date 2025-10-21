// This is a new file. Create it with the following content:
import apiClient from './apiClient';

/**
 * Fetches a list of all clients.
 * @returns {Promise<Array>} A promise that resolves to an array of client objects.
 */
export const getClients = () => {
  return apiClient.get('/api/clients');
};

/**
 * Fetches dashboard statistics for a specific client.
 * @param {string} clientId - The ID of the client.
 * @returns {Promise<Object>} A promise that resolves to the dashboard stats object.
 */
export const getDashboardStats = (clientId) => {
  return apiClient.get(`/api/clients/${clientId}/dashboard-stats`);
};

/**
 * Adds a new client to the system.
 * @param {Object} clientData - The data for the new client (client_id, client_name).
 * @returns {Promise<Object>} A promise that resolves to the new client's data.
 */
export const addClient = (clientData) => {
  return apiClient.post('/api/clients', clientData);
};


/**
 * Searches across all client-specific assets (opportunities, runs, etc.).
 * @param {string} clientId - The ID of the client.
 * @param {string} query - The search query.
 * @returns {Promise<Array>} A promise that resolves to an array of search results.
 */
export const searchAllAssets = (clientId, query) => {
  return apiClient.get(`/api/clients/${clientId}/search-all-assets?query=${encodeURIComponent(query)}`);
};

/**
 * Fetches aggregated data for the main dashboard.
 * @param {string} clientId - The ID of the client.
 * @returns {Promise<Object>} A promise that resolves to the dashboard data object.
 */
export const getDashboardData = (clientId) => {
  return apiClient.get(`/api/clients/${clientId}/dashboard`);
};