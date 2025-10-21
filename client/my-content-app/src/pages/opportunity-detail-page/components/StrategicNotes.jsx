import React from 'react';
import { Alert } from 'antd';
import { BulbOutlined } from '@ant-design/icons';

const StrategicNotes = ({ notes }) => {
  if (!notes) {
    return null;
  }

  return (
    <Alert
      message="Strategic Note from AI Analysis"
      description={notes}
      type="warning"
      showIcon
      icon={<BulbOutlined />}
    />
  );
};

export default StrategicNotes;
