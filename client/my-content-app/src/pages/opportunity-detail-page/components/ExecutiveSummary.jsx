import React from 'react';
import { Card, Typography } from 'antd';
import NoData from './NoData';

const { Title, Paragraph } = Typography;

const ExecutiveSummary = ({ summary }) => {
  if (!summary) {
    return <Card style={{ marginTop: 24 }}><NoData description="Executive Summary not yet available." /></Card>;
  }

  return (
    <Card style={{ marginTop: 24 }}>
      <Title level={4}>Executive Summary</Title>
      <Paragraph>{summary}</Paragraph>
    </Card>
  );
};

export default ExecutiveSummary;