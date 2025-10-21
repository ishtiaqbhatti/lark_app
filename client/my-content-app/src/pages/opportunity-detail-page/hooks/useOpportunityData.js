import { useQuery } from 'react-query';
import { getOpportunityById } from '../../../services/opportunitiesService';

export const useOpportunityData = (opportunityId) => {
  const id = parseInt(opportunityId);
  const { data, isLoading, isError, error, refetch } = useQuery(
    ['opportunity', id],
    () => getOpportunityById(id),
    {
      enabled: !!id,
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
    }
  );

  return { opportunity: data, isLoading, isError, error, refetch };
};
