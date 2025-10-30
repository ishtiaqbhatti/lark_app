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
    isLoading,
    isError,
    error,
    refetch, // Get the refetch function
  } = useQuery(
    ['discoveryRuns', clientId, page],
    () => getDiscoveryRuns(clientId, page),
    {
      enabled: !!clientId,
      keepPreviousData: true,
    }
  );

  // Poll for updates on running jobs
  useEffect(() => {
    let intervalId;

    const checkRunningJobs = async () => {
      const currentRuns = queryClient.getQueryData(['discoveryRuns', clientId, page]);
      const runningRuns = currentRuns?.items?.filter(run => run.status === 'running' && run.job_id);

      if (!runningRuns || runningRuns.length === 0) {
        clearInterval(intervalId);
        intervalId = null;
        return;
      }

      let shouldRefetch = false;
      const statusChecks = runningRuns.map(run => getJobStatus(run.job_id));

      try {
        const jobStatuses = await Promise.all(statusChecks);
        if (jobStatuses.some(job => job.status === 'completed' || job.status === 'failed')) {
          shouldRefetch = true;
        }
      } catch (error) {
        console.error("Error polling job statuses:", error);
      }

      if (shouldRefetch) {
        queryClient.invalidateQueries(['discoveryRuns', clientId]);
      }
    };

    // Start polling only if there are running jobs initially
    const initialRunningRuns = data?.items?.filter(run => run.status === 'running' && run.job_id);
    if (initialRunningRuns && initialRunningRuns.length > 0 && !intervalId) {
      intervalId = setInterval(checkRunningJobs, 8000); // Poll every 8 seconds
    }

    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }, [data, clientId, queryClient, page]); // Add 'page' to dependencies

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
