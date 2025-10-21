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

  const [isModalVisible, setIsModalVisible] = useState(false);
  const [costEstimate, setCostEstimate] = useState(null);
  const [currentFormData, setCurrentFormData] = useState(null);

  const handleEstimateAndRun = async (formData) => {
    if (!clientId) {
      message.error("Client ID is not available. Cannot start discovery run.");
      return;
    }
    
    setCurrentFormData(formData); // Store form data to use upon confirmation

    try {
      const params = {
        seed_keywords: formData.runData.seed_keywords,
        discovery_modes: formData.runData.discovery_modes,
        discovery_max_pages: formData.runData.discovery_max_pages || 1,
      };
      const estimate = await estimateActionCost('discovery', null, params);
      setCostEstimate(estimate);
      setIsModalVisible(true);
    } catch (err) {
      message.error(`Failed to estimate cost: ${err.message}. You can still proceed without a confirmed cost.`);
      // Still show the modal but with an error state
      setCostEstimate({ error: true, message: err.message });
      setIsModalVisible(true);
    }
  };

  const handleModalConfirm = () => {
    if (currentFormData) {
      // Add onSuccess callback to the mutation
      startRunMutation.mutate({ clientId, runData: currentFormData.runData }, {
        onSuccess: (data) => {
          const newRun = data.run_summary;
          // On success, navigate to the new run details page
          message.success(`Discovery run #${newRun.id} started successfully!`);
          navigate(`/discovery/run/${newRun.id}`);
        },
        onError: (err) => {
          // Error notification is likely handled in useDiscoveryRuns hook, but can be handled here too
          message.error(`Failed to start discovery run: ${err.message}`);
        }
      });
    }
    setIsModalVisible(false);
    setCostEstimate(null);
    setCurrentFormData(null);
  };

  const handleModalCancel = () => {
    setIsModalVisible(false);
    setCostEstimate(null);
    setCurrentFormData(null);
  };
  
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
        <Title level={2}>Keyword Discovery</Title>
        <Card>
          <DiscoveryForm
            isSubmitting={startRunMutation.isLoading}
            onSubmit={handleEstimateAndRun}
          />
        </Card>

        <Divider />

        <DiscoveryHistory
            runs={runs}
            isLoading={startRunMutation.isLoading || rerunMutation.isLoading} 
            onRerun={handleRerun}
            isRerunning={rerunMutation.isLoading}
        />
      </Content>
      
      <CostConfirmationModal
        open={isModalVisible}
        onCancel={handleModalCancel}
        onConfirm={handleModalConfirm}
        costEstimate={costEstimate}
        actionType="discovery"
      />
    </Layout>
  );
};

export default DiscoveryPage;
