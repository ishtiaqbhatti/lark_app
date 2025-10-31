import React, { createContext, useContext } from 'react';
import { useQuery } from 'react-query';
import { getActiveJobs } from '../services/jobsService';
import { useClient } from './ClientContext';

const JobContext = createContext();

export const useJobs = () => useContext(JobContext);

export const JobProvider = ({ children }) => {
  const { clientId } = useClient();

  const { data: activeJobs = [], isLoading: isLoadingJobs } = useQuery(
    ['activeJobs', clientId],
    getActiveJobs,
    {
      enabled: !!clientId,
      refetchInterval: (data) =>
        data?.some((job) => job.status === 'running' || job.status === 'pending')
          ? 5000 // Poll every 5 seconds if jobs are active
          : false, // Stop polling if all jobs are done
    }
  );

  const value = { activeJobs, isLoadingJobs };

  return (
    <JobContext.Provider value={value}>
      {children}
    </JobContext.Provider>
  );
};
