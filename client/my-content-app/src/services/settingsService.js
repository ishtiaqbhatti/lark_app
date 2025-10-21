import apiClient from './apiClient';

export const getDiscoveryStrategies = async () => {
  // This is a placeholder. In a real app, you might fetch this from the backend.
  return ["Keyword Ideas", "Keyword Suggestions", "Related Keywords"];
};

export const getAvailableDiscoveryFilters = async () => {
  return apiClient.get('/api/discovery/available-filters');
};