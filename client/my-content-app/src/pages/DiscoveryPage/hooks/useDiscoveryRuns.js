import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import {
  getDiscoveryRuns,
  startDiscoveryRun,
  rerunDiscoveryRun,
  getJobStatus,
} from '../../../services/discoveryService';
import { useClient } from '../../../hooks/useClient';
import { useNotifications } from '../../../context/NotificationContext';

export const useDiscoveryRuns = () => {
  const queryClient = useQueryClient();
  const { clientId } = useClient();
  const { showNotification } = useNotifications();
  const [page, setPage] = useState(1);

  // Query to fetch discovery run history
  const {
    data,
    isLoading, // True on initial fetch
    isError, // True if query failed
    error, // Error object
  } = useQuery(
    ['discoveryRuns', clientId, page], // Unique query key, depends on clientId and page
    () => getDiscoveryRuns(clientId, page), // Function to fetch data
    {
      enabled: !!clientId, // Only run query if clientId is available
      keepPreviousData: true, // Keep previous data while fetching new page
    }
  );

  // Poll for updates on running jobs
  useEffect(() => {
    const runningJobs = data?.items?.filter(run => run.status === 'running' && run.job_id);
    if (runningJobs && runningJobs.length > 0) {
      const interval = setInterval(() => {
        runningJobs.forEach(run => {
          getJobStatus(run.job_id).then(job => {
            if (job.status === 'completed' || job.status === 'failed') {
              queryClient.invalidateQueries(['discoveryRuns', clientId]);
            }
          });
        });
      }, 5000); // Poll every 5s

      return () => clearInterval(interval);
    }
  }, [data, clientId, queryClient]);

  // Mutation for starting a new discovery run
  const startRunMutation = useMutation(startDiscoveryRun, {
    // Optimistic update logic
    onMutate: async (newRunRequest) => {
      await queryClient.cancelQueries(['discoveryRuns', clientId]); // Cancel any outgoing refetches

      const previousRuns = queryClient.getQueryData(['discoveryRuns', clientId, page]); // Snapshot previous state

      // Optimistically add a temporary 'running' job to the cache
      queryClient.setQueryData(['discoveryRuns', clientId, 1], (old) => ({
        ...old,
        items: [
          {
            id: `temp-${Date.now()}`, // Temporary ID for optimistic update
            start_time: new Date().toISOString(),
            status: 'running',
            parameters: { seed_keywords: newRunRequest.runData.seed_keywords },
            results_summary: { progress: 0 }, // Initial progress
            error_message: null,
          },
          ...(old?.items || []),
        ]
      }));
      setPage(1); // Go to the first page to see the new run

      return { previousRuns }; // Return context for rollback
    },
    onError: (err, newRun, context) => {
      queryClient.setQueryData(['discoveryRuns', clientId, page], context.previousRuns); // Rollback on error
      showNotification('error', 'Failed to start discovery run', err.message);
    },
    onSuccess: (data) => {
       showNotification('success', 'Discovery run started successfully!', `Job ID: ${data.job_id}`);
    },
    onSettled: () => {
      queryClient.invalidateQueries(['discoveryRuns', clientId]); // Refetch to get actual server state
    },
  });
  
  // Mutation for re-running an existing discovery job
  const rerunMutation = useMutation(rerunDiscoveryRun, {
    onSuccess: (data) => {
      showNotification('success', 'Re-run started successfully!', `Job ID: ${data.job_id}`);
      queryClient.invalidateQueries(['discoveryRuns', clientId]); // Refetch history to show new job
    },
    onError: (err) => {
      showNotification('error', 'Failed to start re-run', err.message);
    },
  });

  return {
    runs: data?.items || [],
    totalRuns: data?.total_items || 0,
    page,
    setPage,
    isLoading,
    isError,
    error,
    startRunMutation,
    rerunMutation,
  };
};
