import React from 'react';
import { Alert } from 'antd';

const ErrorMessage = ({ message }) => {
  if (!message || !(message.toLowerCase().includes('error') || message.toLowerCase().includes('failed'))) {
    return null;
  }

  return (
    <Alert
      message="Workflow Error"
      description={message}
      type="error"
      showIcon
      closable
    />
  );
};

export default ErrorMessage;
