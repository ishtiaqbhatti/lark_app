import apiClient from './apiClient';

export const startDiscoveryRun = ({ clientId, runData }) => {
  return apiClient.post(`/api/clients/${clientId}/discovery-runs-async`, runData);
};

export const getDiscoveryRuns = (clientId, page = 1, filters = {}) => {
  const params = {
    page,
    search_query: filters.searchQuery || undefined,
    date_range_start: filters.dateRange ? filters.dateRange[0] : undefined,
    date_range_end: filters.dateRange ? filters.dateRange[1] : undefined,
  };
  return apiClient.get(`/api/clients/${clientId}/discovery-runs`, { params });
};

export const estimateCost = ({ clientId, seed_keywords, signal }) => {
  return apiClient.post(`/api/discovery/estimate-cost`, { seed_keywords }, { signal });
};

export const preCheckKeywords = ({ clientId, seed_keywords, signal }) => {
  return apiClient.post(`/api/discovery/pre-check`, { seed_keywords }, { signal });
};

export const rerunDiscoveryRun = (runId) => {
  return apiClient.post(`/api/discovery-runs/rerun/${runId}`);
};

export const getKeywordsForRun = (runId) => {
  return apiClient.get(`/api/discovery-runs/${runId}/keywords`);
};

export const getDisqualifiedKeywords = (runId, reason) => {
    return apiClient.get(`/api/discovery-runs/${runId}/keywords/${reason}`);
};

export const getDisqualificationReasons = (runId) => {
  return apiClient.get(`/api/discovery-runs/${runId}/disqualification-reasons`);
};

export const getJobStatus = (jobId) => {
  return apiClient.get(`/api/jobs/${jobId}`);
};

export const getOpportunities = (clientId, { page = 1, limit = 50, status = 'qualified', sort_by = 'strategic_score', sort_direction = 'desc' }) => {
  return apiClient.get(`/api/clients/${clientId}/opportunities`, { 
    params: { page, limit, status, sort_by, sort_direction } 
  });
};

export const getDiscoveryRunById = async (runId) => {
  const response = await apiClient.get(`/api/discovery-runs/${runId}`);
  return response;
};

// NEW: Add this function
export const getDiscoveryGoalsAndDefaults = () => {
  return apiClient.get('/api/discovery/goals-and-defaults');
};