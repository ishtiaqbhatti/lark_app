import React from 'react';
import { Card, Typography } from 'antd';

const { Title, Paragraph } = Typography;

const ExecutiveSummary = ({ summary }) => {
  if (!summary) {
    return null;
  }

  return (
    <Card style={{ marginTop: 24 }}>
      <Title level={4}>Executive Summary</Title>
      <Paragraph>{summary}</Paragraph>
    </Card>
  );
};

export default ExecutiveSummary;