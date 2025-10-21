import { useQuery } from 'react-query';
import apiClient from '../../../services/apiClient';

const fetchDiscoveryFilters = async () => {
  const data = await apiClient.get('/api/discovery/available-filters');
  return data;
};

export const useDiscoveryFilters = () => {
  const { data, isLoading, isError } = useQuery('discoveryFilters', fetchDiscoveryFilters, {
    staleTime: Infinity, // This data is static, so we can cache it indefinitely
    cacheTime: Infinity,
  });

  return {
    filtersData: data,
    isLoading,
    isError,
  };
};
