import { renderHook, act } from '@testing-library/react-hooks';
import { useOpportunities } from './useOpportunities';
import { QueryClient, QueryClientProvider } from 'react-query';

// Mock dependencies
jest.mock('../services/opportunitiesService');
import { getOpportunities } from '../services/opportunitiesService';

const createWrapper = () => {
  const queryClient = new QueryClient();
  return ({ children }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
};

test('should update keyword state on handleSearch', async () => {
  getOpportunities.mockResolvedValue({ items: [], total_items: 0 });
  const { result } = renderHook(() => useOpportunities(), { wrapper: createWrapper() });

  await act(async () => {
    result.current.handleSearch('test keyword');
  });

  // Assert that the hook's internal state for the keyword was updated
  // Accessing internal state is complex; this test verifies the search term is passed to the API
  expect(getOpportunities).toHaveBeenCalledWith(expect.any(String), expect.objectContaining({
    keyword: 'test keyword'
  }));
});
