// This is a new file. Create it with the following content:
import React from 'react';
import { Modal, Typography, Spin, Alert, List } from 'antd';
import { useQuery } from 'react-query';
import { estimateActionCost } from '../services/orchestratorService'; // NEW

const { Title, Text, Paragraph } = Typography;

const CostConfirmationModal = ({ open, onCancel, onConfirm, opportunityId, actionType }) => {
  const { data: costEstimate, isLoading, isError, error } = useQuery(
    ['costEstimate', opportunityId, actionType],
    () => estimateActionCost(opportunityId, actionType),
    {
      enabled: open && !!opportunityId && !!actionType, // Only fetch when modal is open
      staleTime: 5 * 60 * 1000, // Cost estimates don't change frequently
    }
  );

  const getActionTitle = (type) => {
    switch (type) {
      case 'analyze': return 'Run Deep-Dive Analysis';
      case 'generate': return 'Generate Full Content Package';
      case 'refresh': return 'Refresh Content (Analysis & Generation)';
      case 'validate': return 'Run Live SERP Validation';
      default: return 'Perform Action';
    }
  };

  return (
    <Modal
      title={getActionTitle(actionType)}
      open={open}
      onCancel={onCancel}
      onOk={onConfirm}
      confirmLoading={isLoading}
      okText="Confirm & Proceed"
      cancelText="Cancel"
    >
      {isLoading ? (
        <Spin tip="Estimating API costs..." />
      ) : isError ? (
        <Alert
          message="Error Estimating Cost"
          description={error?.message || 'Could not fetch cost estimation. Proceed with caution.'}
          type="error"
          showIcon
        />
      ) : (
        <>
          <Paragraph>
            This action will incur API costs. Please review the estimate below before proceeding.
          </Paragraph>
          <List
            size="small"
            bordered
            dataSource={costEstimate?.breakdown || []}
            renderItem={item => (
    <List.Item
        actions={[
            <Text key="cost" strong>
                {item.cost ? `$${item.cost.toFixed(4)}` : item.cost === 0 ? '$0.0000' : 'N/A'}
            </Text>
        ]}
    >
        <List.Item.Meta
            title={item.service}
            description={item.details}
        />
    </List.Item>
)}
footer={
    <Paragraph strong style={{ fontSize: '1.2em' }}>Estimated Total: <Text code>${costEstimate?.total_cost?.toFixed(4) || '0.0000'}</Text> USD</Paragraph>
}
/>
<Alert
            message="This is an estimate. Actual costs may vary."
            type="info"
            showIcon
            style={{ marginTop: '16px' }}
          />
        </>
      )}
    </Modal>
  );
};

export default CostConfirmationModal;