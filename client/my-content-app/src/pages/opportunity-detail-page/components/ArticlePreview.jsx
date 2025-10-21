import React from 'react';
import { Card, Typography, Image, Alert } from 'antd';
import NoData from './NoData';

const { Title, Paragraph } = Typography;

const ArticlePreview = ({ aiContent, featuredImagePath }) => {
  if (!aiContent) {
    return <NoData description="No article content has been generated yet." />;
  }

  const { article_title, article_body_html } = aiContent;

  return (
    <Card>
      <Title level={2}>{article_title}</Title>
      {featuredImagePath ? (
        <div style={{ textAlign: 'center', marginBottom: '24px' }}>
          <Image
            width="50%"
            src={`/api/images/${featuredImagePath.split('/').pop()}`}
            alt={article_title}
          />
        </div>
      ) : (
        <NoData description="No featured image has been generated yet." />
      )}
      <div dangerouslySetInnerHTML={{ __html: article_body_html }} />
    </Card>
  );
};

export default ArticlePreview;
