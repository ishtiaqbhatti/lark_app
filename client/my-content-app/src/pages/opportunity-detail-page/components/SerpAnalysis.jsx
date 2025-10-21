import React from 'react';
import { Card, Table, Tag, List, Typography, Button, Statistic, Row, Col } from 'antd';
import {
  FileTextOutlined,
  VideoCameraOutlined,
  QuestionCircleOutlined,
  CommentOutlined,
  SearchOutlined,
  CopyOutlined,
  RobotOutlined,
  FileDoneOutlined,
  LinkOutlined,
  StarFilled
} from '@ant-design/icons';
import { useNotifications } from '../../../context/NotificationContext';

const { Title, Paragraph, Text } = Typography;

const SerpAnalysis = ({ blueprint }) => {
  const { showNotification } = useNotifications();

  if (!blueprint || !blueprint.serp_overview) {
    return <Card><Paragraph type="secondary">No SERP analysis available.</Paragraph></Card>;
  }

  const { top_organic_results, people_also_ask, related_searches, top_organic_sitelinks, serp_has_ai_overview, dominant_content_format } = blueprint.serp_overview;
  const { serp_item_types, se_results_count } = blueprint.winning_keyword.serp_info;

  const getSerpFeatureIcon = (item) => {
    if (item.includes('video')) return <VideoCameraOutlined />;
    if (item.includes('people_also_ask')) return <QuestionCircleOutlined />;
    if (item.includes('perspectives')) return <CommentOutlined />;
    if (item.includes('related_searches')) return <SearchOutlined />;
    return <FileTextOutlined />;
  };

  const handleCopyPaA = () => {
    navigator.clipboard.writeText(people_also_ask.join('\n'));
    showNotification('success', 'Copied to Clipboard', 'People Also Ask questions have been copied.');
  };

  const columns = [
    { title: 'Rank', dataIndex: 'rank', key: 'rank' },
    { title: 'Title', dataIndex: 'title', key: 'title', render: (text, record) => <a href={record.url} target="_blank" rel="noopener noreferrer">{text}</a> },
    { title: 'Domain', dataIndex: 'domain', key: 'domain' },
    { title: 'Page Type', dataIndex: 'page_type', key: 'page_type', render: (type) => <Tag>{type}</Tag> },
    { 
      title: 'Rating', 
      dataIndex: 'rating', 
      key: 'rating', 
      render: (rating) => rating ? <span><StarFilled style={{ color: '#fadb14' }} /> {rating.value} ({rating.votes_count})</span> : null 
    },
  ];

  const handleRelatedSearchClick = (term) => {
    // In a real app, you would likely navigate to the discovery page with this term
    console.log(`Starting a new discovery run for: ${term}`);
    showNotification('info', 'Discovery Run Started', `A new discovery run has been initiated for "${term}".`);
  };

  return (
    <Card title="SERP Analysis">
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={8}>
          <Statistic title="Total Search Results" value={se_results_count} />
        </Col>
        <Col span={8}>
          <Statistic title="AI Overview in SERP" value={serp_has_ai_overview ? 'Yes' : 'No'} prefix={<RobotOutlined />} />
        </Col>
        <Col span={8}>
           <Statistic title="Dominant Content Format" value={dominant_content_format} prefix={<FileDoneOutlined />} />
        </Col>
      </Row>

      <Title level={5}>SERP Features Present</Title>
      <List
        dataSource={serp_item_types}
        renderItem={(item) => <List.Item><Tag icon={getSerpFeatureIcon(item)}>{item.replace(/_/g, ' ')}</Tag></List.Item>}
        grid={{ gutter: 16, column: 4 }}
        style={{ marginBottom: 24 }}
      />

      <Title level={5}>People Also Ask</Title>
      <Button icon={<CopyOutlined />} onClick={handleCopyPaA} style={{ float: 'right' }}>Copy</Button>
      <List dataSource={people_also_ask} renderItem={(item) => <List.Item>{item}</List.Item>} style={{ marginBottom: 24 }} />

      <Title level={5}>Related Searches</Title>
      <div style={{ marginBottom: 24 }}>
        {related_searches.map(term => (
          <Tag 
            icon={<SearchOutlined />} 
            key={term} 
            style={{ margin: 4, cursor: 'pointer' }}
            onClick={() => handleRelatedSearchClick(term)}
          >
            {term}
          </Tag>
        ))}
      </div>
      
      {top_organic_sitelinks?.length > 0 && <>
        <Title level={5}>Top Organic Sitelinks</Title>
        <List dataSource={top_organic_sitelinks} renderItem={(item) => <List.Item><LinkOutlined /> {item}</List.Item>} style={{ marginBottom: 24 }} />
      </>}

      <Title level={5}>Top 10 Organic Results</Title>
      <Table columns={columns} dataSource={top_organic_results} rowKey="url" pagination={false} size="small" />
    </Card>
  );
};

export default SerpAnalysis;
