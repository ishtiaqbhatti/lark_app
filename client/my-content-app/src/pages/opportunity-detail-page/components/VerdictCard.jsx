import React from 'react';
import { Card, Typography, Tag } from 'antd';

const { Title, Paragraph } = Typography;

const VerdictCard = ({ recommendation, confidenceScore }) => {
  if (!recommendation) {
    return null;
  }

  return (
    <Card style={{ marginTop: 24 }}>
      <Title level={5}>The Verdict</Title>
      <Tag color={recommendation === 'Proceed' ? 'success' : 'error'} style={{ fontSize: '1.2rem', padding: '10px' }}>
        {recommendation}
      </Tag>
      <Paragraph style={{ marginTop: '10px' }}>Confidence: {confidenceScore.toFixed(1)}%</Paragraph>
    </Card>
  );
};

export default VerdictCard;
