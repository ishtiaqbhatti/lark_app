import React from 'react';
import { Card, Typography, List, Button, Tooltip } from 'antd';
import { CopyOutlined } from '@ant-design/icons';
import { useNotifications } from '../../../context/NotificationContext';

const { Title, Paragraph } = Typography;

const SocialMediaTab = ({ socialMediaPosts }) => {
  const { showNotification } = useNotifications();

  if (!socialMediaPosts || socialMediaPosts.length === 0) {
    return <Card><Paragraph>No social media posts have been generated yet.</Paragraph></Card>;
  }

  const handleCopy = (text) => {
    navigator.clipboard.writeText(text);
    showNotification('success', 'Copied to Clipboard', 'The post content has been copied.');
  };

  return (
    <List
      grid={{ gutter: 16, column: 2 }}
      dataSource={socialMediaPosts}
      renderItem={(post) => (
        <List.Item>
          <Card title={post.platform}>
            <Paragraph>{post.content}</Paragraph>
            <Tooltip title="Copy Post">
              <Button
                icon={<CopyOutlined />}
                onClick={() => handleCopy(post.content)}
              />
            </Tooltip>
          </Card>
        </List.Item>
      )}
    />
  );
};

export default SocialMediaTab;
