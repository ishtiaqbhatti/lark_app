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

export const useDiscoveryRuns = (searchQuery, dateRange) => { // Accept filters
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
  } = useQuery(
    // Add filters to the query key to trigger re-fetching on change
    ['discoveryRuns', clientId, page, searchQuery, dateRange],
    () => getDiscoveryRuns(clientId, page, { searchQuery, dateRange }), // Pass filters to API call
    {
      enabled: !!clientId,
      keepPreviousData: true,
      refetchInterval: (data) => {
        const isAnyJobRunning = data?.items?.some(run => run.status === 'running' || run.status === 'pending');
        return isAnyJobRunning ? 8000 : false;
      },
    }
  );

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
