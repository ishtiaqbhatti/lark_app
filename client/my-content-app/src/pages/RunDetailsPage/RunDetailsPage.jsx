import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery } from 'react-query';
import { Layout, Spin, Alert, Typography, Progress, Card, Descriptions, Tag, Button } from 'antd';
import { ArrowLeftOutlined } from '@ant-design/icons';
import { getDiscoveryRunById, getKeywordsForRun } from '../../services/discoveryService';
import OpportunityTable from '../../components/OpportunityTable';

const { Content } = Layout;
const { Title } = Typography;

const RunDetailsPage = () => {
  const { runId } = useParams();

  const { data: run, isLoading: isLoadingRun, isError, error } = useQuery(
    ['discoveryRun', runId],
    () => getDiscoveryRunById(runId),
    {
      refetchInterval: (data) => data?.status === 'running' ? 5000 : false,
      refetchOnWindowFocus: false,
    }
  );

  const { data: opportunities, isLoading: isLoadingOpportunities } = useQuery(
    ['discoveryRunOpportunities', runId],
    () => getKeywordsForRun(runId),
    {
      enabled: !!run && run.status === 'completed',
    }
  );

  if (isLoadingRun) {
    return <Spin tip="Loading run details..." style={{ display: 'block', marginTop: '50px' }} />;
  }

  if (isError) {
    return <Alert message="Error" description={error.message} type="error" showIcon />;
  }

  const getStatusTag = (status) => {
    switch (status) {
      case 'completed': return <Tag color="success">Completed</Tag>;
      case 'failed': return <Tag color="error">Failed</Tag>;
      case 'running': return <Tag color="processing">In Progress</Tag>;
      default: return <Tag>{status}</Tag>;
    }
  };

  return (
    <Layout style={{ padding: '24px' }}>
      <Content>
        <Button type="link" icon={<ArrowLeftOutlined />} style={{ marginBottom: '16px', paddingLeft: 0 }}>
          <Link to="/discovery">Back to Discovery Hub</Link>
        </Button>
        <Title level={2}>Discovery Run Details</Title>
        <Card style={{ marginBottom: '24px' }}>
          <Descriptions title="Run Summary" bordered>
            <Descriptions.Item label="Run ID">{run.id}</Descriptions.Item>
            <Descriptions.Item label="Status">{getStatusTag(run.status)}</Descriptions.Item>
            <Descriptions.Item label="Seed Keyword">{run.parameters?.seed_keywords?.join(', ')}</Descriptions.Item>
            <Descriptions.Item label="Created At">{new Date(run.start_time).toLocaleString()}</Descriptions.Item>
          </Descriptions>
        </Card>

        {run.status === 'completed' && (
          <Card title="Discovered Opportunities">
            <OpportunityTable opportunities={opportunities} isLoading={isLoadingOpportunities} />
          </Card>
        )}

        {run.status === 'failed' && (
          <Alert message="Run Failed" description={run.error_message || 'An unknown error occurred.'} type="error" showIcon />
        )}
      </Content>
    </Layout>
  );
};

export default RunDetailsPage;
