import React from 'react';
import { Card, Typography, Tag } from 'antd';
import { CheckSquareOutlined } from '@ant-design/icons';

const { Text } = Typography;

const QualificationInfo = ({ status, reason }) => {
  if (!status) {
    return null;
  }

  return (
    <Card title="Initial Qualification">
      <Text strong>Status: </Text>
      <Tag color={status === 'review' ? 'orange' : 'default'}>{status.toUpperCase()}</Tag>
      <Text type="secondary" style={{ marginTop: '16px', display: 'block' }}>
        {reason}
      </Text>
    </Card>
  );
};

export default QualificationInfo;
