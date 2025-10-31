import React from 'react';
import { Card, Typography, Tag } from 'antd';
import NoData from './NoData';

const { Title, Paragraph } = Typography;

const VerdictCard = ({ recommendation, confidenceScore }) => {
  if (!recommendation) {
    return <Card style={{ marginTop: 24 }}><NoData description="Qualification verdict not yet available." /></Card>;
  }
    
  return (
    <Card style={{ marginTop: 24 }}>
      <Title level={5}>The Verdict</Title>
      <Tag color={recommendation.includes('Proceed') ? 'success' : 'error'} style={{ fontSize: '1.2rem', padding: '10px' }}>
        {recommendation}
      </Tag>
      <Paragraph style={{ marginTop: '10px' }}>Confidence: {confidenceScore ? `${confidenceScore.toFixed(1)}%` : 'N/A'}</Paragraph>
    </Card>
  );
};

export default VerdictCard;
