import React from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from 'react-query';
import { getOpportunityById } from '../../services/opportunitiesService';
import { Layout, Typography, Spin, Alert, Result, Button, Avatar, Space } from 'antd';
import { UserOutlined } from '@ant-design/icons';
import { Link } from 'react-router-dom';
import './BlogPage.css';

const { Content } = Layout;
const { Title, Text } = Typography;

const BlogPage = () => {
  const { opportunityId } = useParams();
  const { data: opportunity, isLoading, isError, error } = useQuery(
    ['opportunity', opportunityId],
    () => getOpportunityById(opportunityId)
  );

  if (isLoading) {
    return (
      <div className="loading-container">
        <Spin size="large" tip="Loading article..." />
      </div>
    );
  }

  if (isError) {
    return <Alert message="Error" description={error.message} type="error" showIcon />;
  }

  const {
    keyword,
    final_package_json,
    author_name = 'AI Assistant',
    publication_date = new Date().toLocaleDateString(),
  } = opportunity || {};

  if (!final_package_json || !final_package_json.article_html_final) {
    return (
      <Result
        status="404"
        title="Content Not Found"
        subTitle="The final content package for this opportunity has not been generated yet."
        extra={<Button type="primary"><Link to={`/opportunities/${opportunityId}`}>Go Back</Link></Button>}
      />
    );
  }

  return (
    <Layout className="blog-layout">
      <Content className="blog-content">
        <div className="blog-post-container">
          <Title level={1} className="blog-title">{final_package_json.meta_title || keyword}</Title>
          <div className="author-info">
            <Avatar icon={<UserOutlined />} />
            <Space direction="vertical" size={0}>
              <Text strong>{author_name}</Text>
              <Text type="secondary">Published on {publication_date}</Text>
            </Space>
          </div>

          {final_package_json.featured_image_relative_path && (
            <img src={final_package_json.featured_image_relative_path} alt={keyword} className="featured-image" />
          )}

          <div
            className="blog-body"
            dangerouslySetInnerHTML={{ __html: final_package_json.article_html_final }}
          />
        </div>
      </Content>
    </Layout>
  );
};

export default BlogPage;
