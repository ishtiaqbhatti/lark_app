import React from 'react';
import { Card, Typography, Tag } from 'antd';
import { BulbOutlined } from '@ant-design/icons';

const { Title, Paragraph } = Typography;

const RecommendedStrategyCard = ({ strategy }) => {
  if (!strategy) {
    return null;
  }

  return (
    <Card style={{ marginTop: 24 }}>
      <Title level={5}><BulbOutlined /> Recommended Strategy</Title>
      <Paragraph strong>Content Format: <Tag color="purple">{strategy.content_format}</Tag></Paragraph>
      <Paragraph>{strategy.strategic_goal}</Paragraph>
    </Card>
  );
};

export default RecommendedStrategyCard;
