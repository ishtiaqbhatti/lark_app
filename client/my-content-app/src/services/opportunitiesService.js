import apiClient from './apiClient';

export const getOpportunities = (clientId, params) => {
  return apiClient.get(`/api/clients/${clientId}/opportunities/summary`, { params });
};

export const getDashboardStats = (clientId) => {
  return apiClient.get(`/api/clients/${clientId}/dashboard`);
};

export const getOpportunityById = (id) => {
  return apiClient.get(`/api/opportunities/${id}`);
};

export const updateOpportunityStatus = (opportunityId, status) => {
  return apiClient.put(`/api/opportunities/${opportunityId}/status?status=${status}`);
};

export const bulkAction = (action, opportunityIds) => {
  return apiClient.post('/api/opportunities/bulk-action', { action, opportunity_ids: opportunityIds });
};

export const compareOpportunities = (opportunityIds) => {
  return apiClient.post('/api/opportunities/compare', { opportunity_ids: opportunityIds });
};

export const updateOpportunityAiContent = (id, updatedContent) => {
  return apiClient.put(`/api/opportunities/${id}/ai-content`, updatedContent);
};

export const generateImage = (id, prompt) => {
  return apiClient.post(`/api/opportunities/${id}/generate-image`, { prompt });
};

export const updateOpportunityImages = (id, images) => {
  return apiClient.put(`/api/opportunities/${id}/images`, images);
};

export const generateSocialPosts = (id, platforms) => {
  return apiClient.post(`/api/opportunities/${id}/generate-social-posts`, { platforms });
};

export const updateOpportunitySocialPosts = (id, posts) => {
  return apiClient.put(`/api/opportunities/${id}/social-posts`, { social_media_posts: posts });
};

export const getContentHistory = (opportunityId) => {
  return apiClient.get(`/api/opportunities/${opportunityId}/content-history`);
};

export const restoreContentVersion = (opportunityId, versionTimestamp) => {
  return apiClient.post(`/api/opportunities/${opportunityId}/restore-content`, { version_timestamp: versionTimestamp });
};

export const submitContentFeedback = (opportunityId, feedbackData) => {
  return apiClient.post(`/api/opportunities/${opportunityId}/feedback`, feedbackData);
};

export const overrideDisqualification = (opportunityId) => {
  return apiClient.post(`/api/opportunities/${opportunityId}/override-disqualification`);
};

export const updateOpportunityContent = (opportunityId, newContentPayload) => {
  return apiClient.put(`/api/opportunities/${opportunityId}/content`, newContentPayload);
};

export const approveAnalysis = (opportunityId, overrides) => {
  return apiClient.post(`/api/orchestrator/approve-analysis/${opportunityId}`, overrides);
};