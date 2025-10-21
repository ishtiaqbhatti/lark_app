import React from 'react';
import { Card, Typography } from 'antd';
import { TrophyOutlined } from '@ant-design/icons';

const { Title, Paragraph } = Typography;

const FeaturedSnippetCard = ({ blueprint }) => {
  const featuredSnippet = blueprint?.serp_overview?.featured_snippet_content;

  if (!featuredSnippet) {
    return null; // Don't render the card if there's no snippet
  }

  return (
    <Card
      title={<span><TrophyOutlined style={{ marginRight: 8 }} /> Featured Snippet Opportunity</span>}
      bordered={false}
      style={{ backgroundColor: '#e6f7ff' }}
    >
      <Paragraph>
        The following content currently holds the featured snippet position. Your goal is to provide a better, more direct answer.
      </Paragraph>
      <Paragraph blockquote="true" style={{ fontStyle: 'italic' }}>
        {featuredSnippet}
      </Paragraph>
    </Card>
  );
};

export default FeaturedSnippetCard;
