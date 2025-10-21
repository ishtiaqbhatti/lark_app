import { useQuery } from 'react-query';
import { useState, useMemo, useEffect } from 'react';
import { getOpportunities, getDashboardStats } from '../../../services/opportunitiesService';
import { useClient } from '../../../hooks/useClient';

export const useOpportunities = () => {
  const { clientId } = useClient();
  const [pagination, setPagination] = useState({ current: 1, pageSize: 20, total: 0 });
  const [activeStatus, setActiveStatus] = useState('review');
  const [sorter, setSorter] = useState({ field: 'strategic_score', order: 'descend' });
  const [statusCounts, setStatusCounts] = useState({});

  const { data: statsData, isLoading: isLoadingStats } = useQuery(
    ['dashboardStats', clientId],
    () => getDashboardStats(clientId),
    {
      enabled: !!clientId,
      onSuccess: (data) => {
        if (data.status_counts) {
          setStatusCounts(data.status_counts);
          if (!activeStatus && Object.keys(data.status_counts).length > 0) {
            setActiveStatus(Object.keys(data.status_counts)[0]);
          }
        }
      },
    }
  );
  
  const { data: opportunitiesData, isLoading, isError, error, refetch } = useQuery(
    ['opportunities', clientId, pagination.current, pagination.pageSize, sorter, activeStatus],
    () => getOpportunities(clientId, { 
      page: pagination.current, 
      limit: pagination.pageSize, 
      sort_by: sorter.field, 
      sort_direction: sorter.order === 'ascend' ? 'asc' : 'desc',
      status: activeStatus 
    }),
    {
      enabled: !!clientId,
      staleTime: 60 * 1000,
      onSuccess: (data) => {
        setPagination(prev => ({ ...prev, total: data.total_count || 0 }));
      }
    }
  );

  const opportunities = useMemo(() => opportunitiesData?.items || [], [opportunitiesData]);

  const handleTableChange = (newPagination, newFilters, newSorter) => {
    setPagination(prev => ({ ...prev, current: newPagination.current, pageSize: newPagination.pageSize }));
    
    const effectiveSorter = Array.isArray(newSorter) ? newSorter[0] : newSorter;
    if (effectiveSorter?.field) {
        setSorter({ field: effectiveSorter.field, order: effectiveSorter.order });
    } else {
        setSorter({ field: 'strategic_score', order: 'descend' });
    }
    refetch();
  };

  return {
    opportunities,
    isLoading: isLoading || isLoadingStats,
    isError, error,
    pagination,
    handleTableChange,
    activeStatus, setActiveStatus,
    statusCounts,
    refetchOpportunities: refetch
  };
};