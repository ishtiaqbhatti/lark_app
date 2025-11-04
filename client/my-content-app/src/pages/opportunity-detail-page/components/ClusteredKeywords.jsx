import React from 'react';
import { Card, Typography, List, Tag } from 'antd';
import { FolderOpenOutlined } from '@ant-design/icons';
import NoData from './NoData';

const { Title, Text } = Typography;

const ClusteredKeywords = ({ clusters }) => {
  if (!clusters || clusters.length === 0) {
    return (
      <Card title="AI-Generated Topic Clusters" style={{ marginTop: 24 }}>
        <NoData description="No topic clusters were generated for this opportunity." />
      </Card>
    );
  }

  return (
    <Card title="AI-Generated Topic Clusters" style={{ marginTop: 24 }}>
      <Text type="secondary" style={{ marginBottom: 16, display: 'block' }}>
        The AI has grouped relevant keywords into these core topics, suggesting a structure for a single, comprehensive article.
      </Text>
      <List
        dataSource={clusters}
        renderItem={(cluster) => (
          <List.Item>
            <List.Item.Meta
              avatar={<FolderOpenOutlined style={{ fontSize: '24px', color: '#1890ff' }} />}
              title={<Title level={5} style={{ margin: 0 }}>{cluster.topic_name}</Title>}
              description={
                <div>
                  {cluster.keywords.map((keyword) => (
                    <Tag key={keyword} style={{ margin: '2px' }}>{keyword}</Tag>
                  ))}
                </div>
              }
            />
          </List.Item>
        )}
      />
    </Card>
  );
};

export default ClusteredKeywords;