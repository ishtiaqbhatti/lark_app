import apiClient from './apiClient';

export const runAnalysis = (opportunityId, selectedUrls) => {
  return apiClient.post(`/api/orchestrator/${opportunityId}/run-analysis-async`, { selected_competitor_urls: selectedUrls });
};

export const startFullContentGeneration = (opportunityId, modelOverride = null, temperature = null) => {
  return apiClient.post(`/api/orchestrator/${opportunityId}/run-generation-async`, { model_override: modelOverride, temperature: temperature });
};

export const approveAnalysis = (opportunityId, overrides = null) => {
  const payload = {
    overrides: {
      additional_instructions: JSON.stringify(overrides),
    },
  };
  return apiClient.post(`/api/orchestrator/approve-analysis/${opportunityId}`, payload);
};

export const refreshContentWorkflow = (opportunityId) => {
  return apiClient.post(`/api/orchestrator/${opportunityId}/refresh-content-async`);
};

export const startFullAnalysis = (opportunityId, modelOverride) => {
    return apiClient.post(`/api/orchestrator/run-full-analysis/${opportunityId}`, { model_override: modelOverride });
};

export const getJobStatus = (jobId) => {
    return apiClient.get(`/api/jobs/${jobId}/status`);
};

export const estimateActionCost = (actionType, opportunityId = null, discoveryParams = null) => {
  const url = opportunityId 
    ? `/api/orchestrator/estimate-cost/${opportunityId}` 
    : '/api/orchestrator/estimate-cost';
  
  const payload = {
    action_type: actionType,
    discovery_params: discoveryParams,
  };
  
  return apiClient.post(url, payload);
};

export const getSerpDataLive = (opportunityId) => {
    return apiClient.get(`/api/orchestrator/${opportunityId}/serp-preview`);
};

export const refreshSerpData = (opportunityId) => {
            return apiClient.post(`/api/orchestrator/${opportunityId}/rerun-analysis-async`);
        };
export const getAllJobs = () => {
    return apiClient.get('/api/jobs');
};

export const cancelJob = (jobId) => {
    return apiClient.post(`/api/jobs/${jobId}/cancel`);
};

// Update startFullWorkflow to accept overrideValidation
export const startFullWorkflow = (opportunityId, overrideValidation = false) => {
  return apiClient.post(`/api/orchestrator/${opportunityId}/run-full-auto-async`, {
    override_validation: overrideValidation
  });
};

// Add refineContent to call the backend refinement endpoint
export const refineContent = (opportunityId, htmlContent, command) => {
  return apiClient.post(`/api/orchestrator/${opportunityId}/refine-content`, {
    html_content: htmlContent,
    command: command
  });
};

export const generateContentOverride = (opportunityId) => {
  return apiClient.post(`/api/orchestrator/${opportunityId}/generate-content-override`);
};

// New service function to reject an opportunity
export const rejectOpportunity = (opportunityId) => {
  return apiClient.post(`/api/orchestrator/reject-opportunity/${opportunityId}`);
};

export const updateSocialMediaPostsStatus = (opportunityId, newStatus) => {
  return apiClient.post(`/api/orchestrator/${opportunityId}/social-media-status`, { new_status: newStatus });
};

 // Add this new function

 export const startFullAutomationWorkflow = (opportunityId, overrideValidation = false) => {

   return apiClient.post(`/api/orchestrator/${opportunityId}/run-full-automation-async`, {

     override_validation: overrideValidation

   });

 };



 export const getFullPrompt = (opportunityId) => {



   return apiClient.get(`/api/orchestrator/${opportunityId}/full-prompt`);



 };



 



 export const getScoreNarrative = (opportunityId) => {



   return apiClient.get(`/api/orchestrator/${opportunityId}/score-narrative`);



 };


