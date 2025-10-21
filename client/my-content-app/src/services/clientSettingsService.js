// my-content-app/src/services/clientSettingsService.js
// NEW FILE
import apiClient from './apiClient';

export const getClientSettings = (clientId) => {
  return apiClient.get(`/api/settings/${clientId}`);
};

export const updateClientSettings = (clientId, settings) => {
  return apiClient.put(`/api/settings/${clientId}`, settings);
};
