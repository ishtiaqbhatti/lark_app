import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Table, Tag, Spin, Alert, Typography, Button, Row, Col } from 'antd';
import { ArrowLeftOutlined, CheckCircleOutlined } from '@ant-design/icons';
import { getKeywordsForRun } from '../../../services/discoveryService';
import { overrideDisqualification } from '../../../services/opportunitiesService';
import { useNotifications } from '../../../hooks/useNotifications';

const { Title, Text } = Typography;

const RunDetailsPage = () => {
  const { runId } = useParams();
  const navigate = useNavigate();
  const [keywords, setKeywords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [updatingIds, setUpdatingIds] = useState(new Set());
  const { showNotification } = useNotifications();

  useEffect(() => {
    const fetchKeywords = async () => {
      try {
        setLoading(true);
        const response = await getKeywordsForRun(runId);
        setKeywords(response || []);
      } catch (err) {
        setError('Failed to fetch keyword details for this run.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchKeywords();
  }, [runId]);

  const handleOverride = async (opportunityId) => {
    setUpdatingIds(prev => new Set(prev).add(opportunityId));
    try {
      await overrideDisqualification(opportunityId);
      showNotification('success', 'Keyword Re-qualified', 'The keyword has been moved to the pending queue.');
      // Optimistically update the UI
      setKeywords(prevKeywords => 
        prevKeywords.map(kw => 
          kw.id === opportunityId 
            ? { ...kw, blog_qualification_status: 'passed_manual_override', blog_qualification_reason: 'Manually overridden by user.' }
            : kw
        )
      );
    } catch (err) {
      showNotification('error', 'Override Failed', err.message || 'Could not re-qualify the keyword.');
      console.error(err);
    } finally {
      setUpdatingIds(prev => {
        const newSet = new Set(prev);
        newSet.delete(opportunityId);
        return newSet;
      });
    }
  };

  const columns = [
    {
      title: 'Keyword',
      dataIndex: 'keyword',
      key: 'keyword',
      sorter: (a, b) => a.keyword.localeCompare(b.keyword),
      render: (text, record) => (
        <Space>
          <Text>{text}</Text>
          {record.is_question && <Tooltip title="Question Keyword"><QuestionCircleOutlined style={{ color: '#1890ff' }} /></Tooltip>}
        </Space>
      ),
    },
    {
      title: 'Qualification Status',
      dataIndex: 'blog_qualification_status',
      key: 'blog_qualification_status',
      render: (status) => {
        let color = 'default';
        if (status === 'passed') color = 'success';
        else if (status === 'failed' || status === 'rejected') color = 'error';
        else if (status === 'passed_manual_override') color = 'processing';
        return (
          <Tag color={color}>
            {status ? status.replace(/_/g, ' ').toUpperCase() : 'N/A'}
          </Tag>
        );
      },
      filters: [
        { text: 'Passed', value: 'passed' },
        { text: 'Failed', value: 'failed' },
        { text: 'Override', value: 'passed_manual_override' },
      ],
      onFilter: (value, record) => record.blog_qualification_status === value,
    },
    {
      title: 'Reason',
      dataIndex: 'blog_qualification_reason',
      key: 'blog_qualification_reason',
      render: (reason) => reason || <Text type="secondary">N/A</Text>,
    },
    {
        title: 'Search Volume',
        dataIndex: ['keyword_info', 'search_volume'],
        key: 'search_volume',
        sorter: (a, b) => (a.keyword_info?.search_volume || 0) - (b.keyword_info?.search_volume || 0),
        render: (sv) => sv ? sv.toLocaleString() : 'N/A',
    },
    {
        title: 'Keyword Difficulty',
        dataIndex: ['keyword_properties', 'keyword_difficulty'],
        key: 'keyword_difficulty',
        sorter: (a, b) => (a.keyword_properties?.keyword_difficulty || 0) - (b.keyword_properties?.keyword_difficulty || 0),
        render: (kd) => kd || 'N/A',
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_, record) => {
        const isFailed = record.blog_qualification_status === 'failed' || record.blog_qualification_status === 'rejected';
        if (isFailed) {
          return (
            <Button 
              type="primary" 
              ghost 
              size="small"
              icon={<CheckCircleOutlined />}
              onClick={() => handleOverride(record.id)}
              loading={updatingIds.has(record.id)}
            >
              Re-qualify
            </Button>
          );
        }
        return null;
      },
    },
  ];

  if (loading) {
    return <Spin tip="Loading keywords..." style={{ display: 'block', marginTop: '50px' }} />;
  }

  if (error) {
    return <Alert message="Error" description={error} type="error" showIcon />;
  }

  return (
    <>
      <div style={{ padding: '16px 24px', backgroundColor: '#fff', borderBottom: '1px solid #f0f0f0' }}>
        <Row align="middle" gutter={16}>
          <Col>
            <Button icon={<ArrowLeftOutlined />} onClick={() => navigate(-1)} />
          </Col>
          <Col>
            <Title level={4} style={{ margin: 0 }}>
              Keywords for Discovery Run #{runId}
            </Title>
            <Text type="secondary">{keywords.length.toLocaleString()} keywords found</Text>
          </Col>
        </Row>
      </div>
      <div style={{ padding: '24px' }}>
        <Table
          columns={columns}
          dataSource={keywords}
          rowKey="id"
          loading={loading}
          pagination={{ pageSize: 50 }}
        />
      </div>
    </>
  );
};

export default RunDetailsPage;
