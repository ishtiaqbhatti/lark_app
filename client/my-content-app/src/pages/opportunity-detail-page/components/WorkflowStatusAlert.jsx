import React from 'react';
import { Alert } from 'antd';
import { InfoCircleOutlined } from '@ant-design/icons';

const WorkflowStatusAlert = ({ status, message }) => {
  // Only show for specific, non-error statuses that have a message
  if (status !== 'paused_for_approval' || !message) {
    return null;
  }

  // Don't show if the message looks like an error
  if (message.toLowerCase().includes('error') || message.toLowerCase().includes('failed')) {
      return null;
  }

  return (
    <Alert
      message="Current Status"
      description={message}
      type="info"
      showIcon
      icon={<InfoCircleOutlined />}
    />
  );
};

export default WorkflowStatusAlert;
