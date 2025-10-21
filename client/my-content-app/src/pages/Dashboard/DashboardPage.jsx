import React from 'react';
import { useQuery } from 'react-query';
import { Layout, Typography, Spin, Alert, Row, Col, Card, Statistic, Table, Tag } from 'antd';
import { 
  FileTextOutlined, 
  CheckCircleOutlined, 
  DollarCircleOutlined, 
  ExperimentOutlined,
  ClockCircleOutlined,
  WarningOutlined,
  ArrowRightOutlined,
  ReadOutlined
} from '@ant-design/icons';
import { useClient } from '../../hooks/useClient';
import { getDashboardData } from '../../services/clientService';
import { format } from 'date-fns';
import { useNavigate } from 'react-router-dom';
import FunnelChart from '../DiscoveryPage/components/FunnelChart';

const { Content } = Layout;
const { Title, Text, Link } = Typography;

const KpiCard = ({ icon, title, value, prefix, precision = 0 }) => (
  <Card>
    <Statistic 
      title={title} 
      value={value} 
      precision={precision} 
      prefix={icon ? React.createElement(icon, { style: { marginRight: 8 } }) : prefix} 
    />
  </Card>
);

const DashboardPage = () => {
  const { clientId } = useClient();
  const navigate = useNavigate();

  const { data, isLoading, isError, error } = useQuery(
    ['dashboardData', clientId],
    () => getDashboardData(clientId),
    {
      enabled: !!clientId,
    }
  );

  if (isLoading) {
    return <Spin tip="Loading dashboard..." style={{ display: 'block', marginTop: '50px' }} />;
  }

  if (isError) {
    return <Alert message="Error" description={error.message} type="error" showIcon />;
  }

  const { kpis, funnelData, actionItems, recent_items } = data;

  const actionColumns = [
    {
      title: 'Keyword',
      dataIndex: 'keyword',
      key: 'keyword',
      render: (text, record) => <Link onClick={() => navigate(`/opportunities/${record.id}`)}>{text}</Link>,
    },
    {
      title: 'Score',
      dataIndex: 'strategic_score',
      key: 'strategic_score',
      render: (score) => (
        <Tag color="blue">
          {typeof score === 'number' ? score.toFixed(1) : 'N/A'}
        </Tag>
      ),
    },
    {
      title: 'Updated',
      dataIndex: 'updated_at',
      key: 'updated_at',
      render: (ts) => ts ? format(new Date(ts), 'yyyy-MM-dd') : 'N/A',
    },
    {
      title: 'Action',
      key: 'action',
      render: (_, record) => <Link onClick={() => navigate(`/opportunities/${record.id}`)}>Review <ArrowRightOutlined /></Link>,
    },
  ];

  const failedColumns = [
    {
      title: 'Keyword',
      dataIndex: 'keyword',
      key: 'keyword',
      render: (text, record) => <Link onClick={() => navigate(`/opportunities/${record.id}`)}>{text}</Link>,
    },
    {
      title: 'Error',
      dataIndex: 'error_message',
      key: 'error_message',
      render: (msg) => <Text type="danger" ellipsis={{ tooltip: msg }}>{msg || 'No details'}</Text>,
    },
    {
      title: 'Action',
      key: 'action',
      render: (_, record) => <Link onClick={() => navigate(`/opportunities/${record.id}`)}>Details <ArrowRightOutlined /></Link>,
    },
  ];
  
  const recentActivityColumns = [
    {
      title: 'Keyword',
      dataIndex: 'keyword',
      key: 'keyword',
      render: (text, record) => <Link onClick={() => navigate(`/opportunities/${record.id}`)}>{text}</Link>,
    },
    {
      title: 'Generated On',
      dataIndex: 'date_processed',
      key: 'date_processed',
      render: (ts) => ts ? format(new Date(ts), 'yyyy-MM-dd HH:mm') : 'N/A',
    },
    {
        title: 'Action',
        key: 'action',
        render: (_, record) => <Link onClick={() => navigate(`/opportunities/${record.id}?tab=Article`)}>View Article <ReadOutlined /></Link>,
    },
  ];

  // Safely extract funnel data
  const getFunnelCount = (stage) => funnelData?.find(d => d.stage === stage)?.count || 0;

  return (
    <Layout>
      <Content style={{ padding: '24px' }}>
        <Title level={2}>Dashboard for {clientId}</Title>
        
        <Row gutter={[24, 24]} style={{ marginBottom: '24px' }}>
          <Col xs={24} sm={12} md={6}><KpiCard icon={FileTextOutlined} title="Total Opportunities" value={kpis.totalOpportunities} /></Col>
          <Col xs={24} sm={12} md={6}><KpiCard icon={CheckCircleOutlined} title="Content Generated" value={kpis.contentGenerated} /></Col>
          <Col xs={24} sm={12} md={6}><KpiCard icon={DollarCircleOutlined} title="Est. Monthly Traffic Value" value={kpis.totalTrafficValue} prefix="$" precision={2} /></Col>
          <Col xs={24} sm={12} md={6}><KpiCard icon={ExperimentOutlined} title="Total API Cost" value={kpis.totalApiCost} prefix="$" precision={2} /></Col>
        </Row>

        <Row gutter={[24, 24]}>
          {/* Left Column */}
          <Col xs={24} lg={16}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
              {actionItems?.awaitingApproval?.length > 0 && (
                <Card title={<><ClockCircleOutlined style={{marginRight: 8}} /> Awaiting Your Approval</>}>
                  <Table
                    dataSource={actionItems.awaitingApproval}
                    columns={actionColumns}
                    rowKey="id"
                    pagination={{ pageSize: 5 }}
                    size="small"
                  />
                </Card>
              )}
              {actionItems?.failed?.length > 0 && (
                <Card title={<><WarningOutlined style={{marginRight: 8}} /> Failed Workflows</>}>
                  <Table
                    dataSource={actionItems.failed}
                    columns={failedColumns}
                    rowKey="id"
                    pagination={{ pageSize: 5 }}
                    size="small"
                  />
                </Card>
              )}
            </div>
          </Col>

          {/* Right Column */}
          <Col xs={24} lg={8}>
             <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                <Card title="Recent Activity">
                    <Table
                        dataSource={recent_items}
                        columns={recentActivityColumns}
                        rowKey="id"
                        pagination={{ pageSize: 10 }}
                        size="small"
                        locale={{ emptyText: 'No recent activity' }}
                    />
                </Card>
                <Card title="Content Pipeline Funnel">
                  <FunnelChart 
                    totalRaw={getFunnelCount('Total')}
                    unique={getFunnelCount('Validated')}
                    qualified={getFunnelCount('Analyzed')}
                    disqualified={getFunnelCount('Disqualified')}
                    addedToDB={getFunnelCount('Generated')}
                  />
                </Card>
             </div>
          </Col>
        </Row>
      </Content>
    </Layout>
  );
};

export default DashboardPage;