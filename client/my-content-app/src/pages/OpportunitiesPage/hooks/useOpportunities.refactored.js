import { useQuery } from 'react-query';
import { useState } from 'react';
import { getOpportunities } from '../../../services/opportunitiesService';
import { useClient } from '../../../hooks/useClient';

export const useOpportunities = () => {
  const { clientId } = useClient();
  const [pagination, setPagination] = useState({ current: 1, pageSize: 20, total: 0 });
  const [activeStatus, setActiveStatus] = useState('review');
  const [sorter, setSorter] = useState({ field: 'strategic_score', order: 'descend' });
  const [keyword, setKeyword] = useState('');

  const { data, isLoading, isError, error, refetch } = useQuery(
    ['opportunities', clientId, pagination.current, pagination.pageSize, activeStatus, sorter, keyword],
    () => getOpportunities(clientId, {
      page: pagination.current,
      limit: pagination.pageSize,
      status: activeStatus,
      sort_by: sorter.field,
      sort_direction: sorter.order === 'ascend' ? 'asc' : 'desc',
      keyword: keyword,
    }),
    {
      enabled: !!clientId,
      staleTime: 60 * 1000, // Keep data fresh for 1 minute
      onSuccess: (response) => {
        setPagination(prev => ({ ...prev, total: response.total_items || 0 }));
      }
    }
  );

  const handleTableChange = (newPagination, newFilters, newSorter) => {
    setPagination(prev => ({ ...prev, current: newPagination.current, pageSize: newPagination.pageSize }));

    const effectiveSorter = Array.isArray(newSorter) ? newSorter[0] : newSorter;
    if (effectiveSorter?.field) {
        setSorter({ field: effectiveSorter.field, order: effectiveSorter.order });
    } else {
        // Reset to default sort if no specific column is sorted
        setSorter({ field: 'strategic_score', order: 'descend' });
    }
  };

  const handleSearch = (newKeyword) => {
    setKeyword(newKeyword);
  };

  return {
    opportunities: data?.items || [],
    isLoading,
    isError,
    error,
    pagination,
    handleTableChange,
    activeStatus,
    setActiveStatus,
    handleSearch,
    refetchOpportunities: refetch,
  };
};
