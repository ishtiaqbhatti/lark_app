import React from 'react';
import { Card, Typography, List, Tag } from 'antd';

const { Title, Paragraph } = Typography;

const AdditionalInsights = ({ serpOverview }) => {
  return (
    <Card title="Additional Insights">
      {serpOverview?.discussion_snippets?.length > 0 && (
        <>
          <Title level={5}>Discussion Snippets</Title>
          <List
            dataSource={serpOverview.discussion_snippets}
            renderItem={(item) => <List.Item>{item}</List.Item>}
            size="small"
            bordered
            style={{ marginBottom: '24px' }}
          />
        </>
      )}
    </Card>
  );
};

export default AdditionalInsights;
