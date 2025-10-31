import React from 'react';
import { Card, Button, Space, Alert, Modal } from 'antd';
import { CheckOutlined, ExperimentOutlined, RocketOutlined, DeleteOutlined, ExclamationCircleOutlined } from '@ant-design/icons';
import { useNotifications } from '../../../context/NotificationContext';
import { useMutation, useQueryClient } from 'react-query';
import { approveAnalysis, startFullContentGeneration, startFullWorkflow, rejectOpportunity, runAnalysis } from '../../../services/orchestratorService';

const { confirm } = Modal;

const ActionCenter = ({ status, opportunityId, overrides, refetch }) => {
  const { showNotification } = useNotifications();
  const queryClient = useQueryClient();

  const { mutate: approveAnalysisMutation, isLoading: isApproving } = useMutation(
    () => approveAnalysis(opportunityId, overrides),
    {
      onSuccess: () => {
        showNotification('success', 'Analysis Approved', 'The content generation process has been initiated.');
        refetch();
        queryClient.invalidateQueries('opportunities');
        queryClient.invalidateQueries('dashboardStats');
      },
      onError: (error) => showNotification('error', 'Approval Failed', error.message),
    }
  );

  const { mutate: generateContentMutation, isLoading: isGenerating } = useMutation(
    (variables) => startFullContentGeneration(variables.opportunityId, variables.modelOverride, variables.temperature),
    {
      onSuccess: () => {
        showNotification('success', 'Content Generation Started', 'The AI is now generating the content.');
        refetch();
        queryClient.invalidateQueries('opportunities');
        queryClient.invalidateQueries('dashboardStats');
      },
      onError: (error) => showNotification('error', 'Generation Failed', error.message),
    }
  );

  const { mutate: startWorkflowMutation, isLoading: isStartingWorkflow } = useMutation(
    () => startFullWorkflow(opportunityId, ['failed', 'rejected'].includes(status)),
    {
      onSuccess: (data) => {
        showNotification('success', 'Workflow Started', `Job has been queued. Job ID: ${data.job_id}`);
        refetch();
        queryClient.invalidateQueries('opportunities');
        queryClient.invalidateQueries('dashboardStats');
      },
      onError: (err) => showNotification('error', 'Workflow Failed', err.message),
    }
  );

  const { mutate: rejectOpportunityMutation, isLoading: isRejecting } = useMutation(
    () => rejectOpportunity(opportunityId),
    {
      onSuccess: () => {
        showNotification('success', 'Opportunity Rejected', 'The opportunity has been marked as rejected.');
        refetch();
        queryClient.invalidateQueries('opportunities');
        queryClient.invalidateQueries('dashboardStats');
      },
      onError: (err) => showNotification('error', 'Rejection Failed', err.message),
    }
  );

  const { mutate: startAnalysisMutation, isLoading: isStartingAnalysis } = useMutation(
    () => runAnalysis(opportunityId, null),
    {
      onSuccess: (data) => {
        showNotification('success', 'Analysis Started', `Analysis job queued. Job ID: ${data.job_id}`);
        refetch();
        queryClient.invalidateQueries('opportunities');
        queryClient.invalidateQueries('dashboardStats');
      },
      onError: (error) => showNotification('error', 'Analysis Failed', error.message),
    }
  );

  const showRejectConfirm = () => {
    confirm({
      title: 'Are you sure you want to reject this opportunity?',
      icon: <ExclamationCircleOutlined />,
      content: 'This action cannot be undone.',
      okText: 'Yes, Reject',
      okType: 'danger',
      cancelText: 'No',
      onOk: () => rejectOpportunityMutation(),
    });
  };

  const renderActions = () => {
    const isLoading = isApproving || isGenerating || isStartingWorkflow || isRejecting || isStartingAnalysis;

    switch (status) {
      case 'review':
        return (
          <Space>
            <Button type="primary" icon={<RocketOutlined />} onClick={() => startWorkflowMutation()} loading={isStartingWorkflow} disabled={isLoading}>
              Start Full Workflow
            </Button>
            <Button type="danger" icon={<DeleteOutlined />} onClick={showRejectConfirm} loading={isRejecting} disabled={isLoading}>
              Reject
            </Button>
          </Space>
        );
      case 'validated':
        return (
          <Button type="primary" icon={<ExperimentOutlined />} onClick={() => startAnalysisMutation()} loading={isStartingAnalysis} disabled={isLoading}>
            Run Full Analysis
          </Button>
        );
      case 'analyzed':
        return (
          <Button type="primary" icon={<ExperimentOutlined />} onClick={() => generateContentMutation({ opportunityId, modelOverride: null, temperature: null })} loading={isGenerating} disabled={isLoading}>
            Generate Content Package
          </Button>
        );
      case 'paused_for_approval':
        return (
          <Button type="primary" icon={<CheckOutlined />} onClick={() => approveAnalysisMutation()} loading={isApproving} disabled={isLoading}>
            Approve & Generate Content
          </Button>
        );
      case 'failed':
      case 'rejected':
        return (
          <Button type="primary" icon={<RocketOutlined />} onClick={() => startWorkflowMutation()} loading={isStartingWorkflow} disabled={isLoading}>
            Rerun Full Workflow
          </Button>
        );
      default:
        return <Alert message="No actions available for the current status." type="info" showIcon />;
    }
  };

  return (
    <Card>
      <Space direction="vertical" style={{ width: '100%' }}>
        <Alert
          message="Next Step"
          description="This is the primary action to move this opportunity forward in the workflow."
          type="info"
          showIcon
        />
        {renderActions()}
      </Space>
    </Card>
  );
};

export default ActionCenter;
