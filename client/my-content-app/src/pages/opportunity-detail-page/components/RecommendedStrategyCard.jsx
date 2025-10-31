import React from 'react';
import { Card, Typography, Tag } from 'antd';
import { BulbOutlined } from '@ant-design/icons';
import NoData from './NoData';

const { Title, Paragraph } = Typography;

const RecommendedStrategyCard = ({ strategy }) => {
  if (!strategy || !strategy.content_format) {
    return <Card style={{ marginTop: 24 }}><NoData description="Recommended strategy not yet determined." /></Card>;
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
