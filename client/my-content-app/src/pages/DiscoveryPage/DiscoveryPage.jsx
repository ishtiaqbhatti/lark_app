import React, { useState } from 'react';
import { Layout, Typography, Spin, Alert, Card, Divider, message } from 'antd';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import { useDiscoveryRuns } from './hooks/useDiscoveryRuns';
import DiscoveryForm from './components/DiscoveryForm';
import DiscoveryHistory from './components/DiscoveryHistory';
import { useClient } from '../../hooks/useClient';
import CostConfirmationModal from '../../components/CostConfirmationModal';
import { estimateActionCost } from '../../services/orchestratorService';

const { Content } = Layout;
const { Title } = Typography;

import useDebounce from '../../hooks/useDebounce'; // Add this import

const DiscoveryPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [dateRange, setDateRange] = useState(null);
  const debouncedSearchQuery = useDebounce(searchQuery, 500);

  const { runs, totalRuns, page, setPage, isLoading, isError, error, startRunMutation, rerunMutation } = useDiscoveryRuns(debouncedSearchQuery, dateRange);
  const { clientId } = useClient();
  const navigate = useNavigate(); // Initialize navigate

  const handleRerun = (runId) => {
      rerunMutation.mutate(runId);
  }

  const handleSearchChange = (query) => {
    setSearchQuery(query);
    setPage(1); // Reset to first page on new search
  };

  const handleDateChange = (dates) => {
    setDateRange(dates);
    setPage(1); // Reset to first page on date change
  };

  if (isLoading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <Spin size="large" tip="Loading Discovery Hub..." />
      </div>
    );
  }

  if (isError) {
    return (
        <Alert
            message="Error"
            description={error.message || "Failed to load discovery run history. Please try again."}
            type="error"
            showIcon
            style={{ margin: '16px' }}
        />
    );
  }

  return (
    <Layout style={{ padding: '24px', background: '#f0f2f5' }}>
      <Content style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <Spin spinning={startRunMutation.isLoading} tip="Starting discovery run..." size="large">
          <Title level={2} style={{ marginBottom: '24px' }}>Discovery Hub</Title>
          <Card style={{ marginBottom: '32px', boxShadow: '0 4px 12px rgba(0, 0, 0, 0.05)' }}>
            <DiscoveryForm
              isSubmitting={startRunMutation.isLoading}
              onSubmit={({ runData }) => {
                startRunMutation.mutate({ clientId, runData });
              }}
            />
          </Card>

          <Divider />

          <DiscoveryHistory
              runs={runs}
              totalRuns={totalRuns}
              page={page}
              setPage={setPage}
              isLoading={isLoading || startRunMutation.isLoading || rerunMutation.isLoading}
              onRerun={handleRerun}
              isRerunning={rerunMutation.isLoading}
              searchQuery={searchQuery}
              setSearchQuery={handleSearchChange}
              setDateRange={handleDateChange}
          />
        </Spin>
      </Content>
    </Layout>
  );
};

export default DiscoveryPage;
