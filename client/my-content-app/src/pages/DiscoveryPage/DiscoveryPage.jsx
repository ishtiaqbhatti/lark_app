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

const DiscoveryPage = () => {
  const { runs, isLoading, isError, error, startRunMutation, rerunMutation } = useDiscoveryRuns();
  const { clientId } = useClient();
  const navigate = useNavigate(); // Initialize navigate

  const handleRerun = (runId) => {
      rerunMutation.mutate(runId);
  }

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
    <Layout style={{ padding: '24px' }}>
      <Content>
        <Spin spinning={startRunMutation.isLoading} tip="Starting discovery run..." size="large">
          <Title level={2}>Keyword Discovery</Title>
          <Card>
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
              isLoading={startRunMutation.isLoading || rerunMutation.isLoading}
              onRerun={handleRerun}
              isRerunning={rerunMutation.isLoading}
          />
        </Spin>
      </Content>
    </Layout>
  );
};

export default DiscoveryPage;
