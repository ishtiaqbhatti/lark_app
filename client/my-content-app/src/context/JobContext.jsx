import React, { createContext, useState, useContext } from 'react';

const JobContext = createContext();

export const useJobs = () => useContext(JobContext);

export const JobProvider = ({ children }) => {
  const [activeJobs, setActiveJobs] = useState({});

  const startJob = (jobId, message) => {
    setActiveJobs(prev => ({ ...prev, [jobId]: { status: 'running', message } }));
  };

  const updateJob = (jobId, status, message) => {
    setActiveJobs(prev => {
      if (!prev[jobId]) return prev;
      return { ...prev, [jobId]: { ...prev[jobId], status, message } };
    });
  };

  const completeJob = (jobId) => {
    setTimeout(() => {
      setActiveJobs(prev => {
        const newJobs = { ...prev };
        delete newJobs[jobId];
        return newJobs;
      });
    }, 5000); // Remove after 5 seconds
  };

  return (
    <JobContext.Provider value={{ activeJobs, startJob, updateJob, completeJob }}>
      {children}
    </JobContext.Provider>
  );
};
