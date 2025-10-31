import apiClient from './apiClient';

export const getJobStatus = (jobId) => {
  return apiClient.get(`/api/jobs/${jobId}`);
};

export const getActiveJobs = () => {
  return apiClient.get('/api/jobs/active');
};
