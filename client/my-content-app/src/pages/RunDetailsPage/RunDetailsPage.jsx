import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery } from 'react-query';
import { Layout, Spin, Alert, Typography, Progress, Card, Descriptions, Tag, Button } from 'antd';
import { ArrowLeftOutlined } from '@ant-design/icons';
import { getDiscoveryRunById } from '../../services/discoveryService'; // Adjust import path as needed
// import OpportunityTable from '../../components/OpportunityTable'; // Assuming a reusable table component exists

const { Content } = Layout;
const { Title, Paragraph } = Typography;

const RunDetailsPage = () => {
  const { runId } = useParams();

  const { data: run, isLoading, isError, error } = useQuery(
    ['discoveryRun', runId],
    () => getDiscoveryRunById(runId),
    {
      // Poll for updates every 5 seconds if the run is still in progress
      refetchInterval: (data) => {
        const inProgress = data?.status === 'PENDING' || data?.status === 'IN_PROGRESS';
        return inProgress ? 5000 : false;
      },
      refetchOnWindowFocus: false,
    }
  );

  if (isLoading) {
    return <Spin tip="Loading run details..." style={{ display: 'block', marginTop: '50px' }} />;
  }

  if (isError) {
    return <Alert message="Error" description={error.message} type="error" showIcon />;
  }

  const getStatusTag = (status) => {
    switch (status) {
      case 'COMPLETED': return <Tag color="success">Completed</Tag>;
      case 'FAILED': return <Tag color="error">Failed</Tag>;
      case 'IN_PROGRESS': return <Tag color="processing">In Progress</Tag>;
      case 'PENDING': return <Tag color="gold">Pending</Tag>;
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
            <Descriptions.Item label="Created At">{new Date(run.created_at).toLocaleString()}</Descriptions.Item>
          </Descriptions>
          {run.status === 'IN_PROGRESS' && (
            <div style={{ marginTop: '16px' }}>
              <Paragraph>{run.progress_message || 'Processing...'}</Paragraph>
              <Progress percent={run.progress_percent || 0} />
            </div>
          )}
        </Card>

        {run.status === 'COMPLETED' && (
          <Card title="Discovered Opportunities">
            {/* Assuming you have a component to display opportunities */}
            {/* <OpportunityTable opportunities={run.opportunities} /> */}
          </Card>
        )}

        {run.status === 'FAILED' && (
          <Alert message="Run Failed" description={run.error_message || 'An unknown error occurred.'} type="error" showIcon />
        )}
      </Content>
    </Layout>
  );
};

export default RunDetailsPage;
