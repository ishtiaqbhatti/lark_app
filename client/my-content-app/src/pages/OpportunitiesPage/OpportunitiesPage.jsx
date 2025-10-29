import React, { useState } from 'react';
import { Layout, Typography, Table, Tag, Button, Space, Tooltip, Modal, Card, Tabs } from 'antd';
import { RocketOutlined, EditOutlined, DeleteOutlined, ExclamationCircleOutlined, LineChartOutlined } from '@ant-design/icons';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer } from 'recharts';
import { useOpportunities } from './hooks/useOpportunities';
import { useNotifications } from '../../context/NotificationContext';
import { useMutation, useQueryClient } from 'react-query';
import { startFullWorkflow, rejectOpportunity } from '../../services/orchestratorService';
import JobStatusIndicator from '../../components/JobStatusIndicator';
import { useJobs } from '../../context/JobContext';
import { getJobStatus } from '../../services/jobsService';
import { useNavigate } from 'react-router-dom';
import './OpportunitiesPage.css';

const { Content } = Layout;
const { Title, Text } = Typography;
const { confirm } = Modal;
const { TabPane } = Tabs;

const MAIN_STATUSES = [
  'review', 
  'paused_for_approval', 
  'generated', 
  'rejected', 
  'failed'
];

const statusColors = {
  review: 'blue',
  paused_for_approval: 'orange',
  generated: 'green',
  rejected: 'default',
  failed: 'red',
};

const OpportunitiesPage = () => {
  const { 
    opportunities, isLoading, pagination, 
    handleTableChange, activeStatus, setActiveStatus, statusCounts
  } = useOpportunities();
  const [isTrendModalVisible, setIsTrendModalVisible] = useState(false);
  const [selectedOpportunity, setSelectedOpportunity] = useState(null);
  const { showNotification } = useNotifications();
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const { startJob, updateJob, completeJob } = useJobs();

  const { mutate: startWorkflowMutation, isLoading: isStartingWorkflow } = useMutation(
    ({ opportunityId, override, opportunityKeyword }) => startFullWorkflow(opportunityId, override),
    {
      onSuccess: (data, variables) => {
        const { job_id } = data;
        const { opportunityKeyword } = variables;
        startJob(job_id, `Workflow started for "${opportunityKeyword}".`);

        const poll = setInterval(async () => {
          try {
            const statusData = await getJobStatus(job_id);
            if (statusData.status === 'completed' || statusData.status === 'failed') {
              updateJob(job_id, statusData.status, statusData.error || `Workflow for "${opportunityKeyword}" finished.`);
              completeJob(job_id);
              clearInterval(poll);
              queryClient.invalidateQueries('opportunities');
            } else {
              const lastLog = statusData.progress_log?.[statusData.progress_log.length - 1];
              updateJob(job_id, 'running', lastLog?.message || 'Processing...');
            }
          } catch (error) {
            updateJob(job_id, 'failed', 'Failed to get job status.');
            completeJob(job_id);
            clearInterval(poll);
          }
        }, 5000);
      },
      onError: (err, variables) => {
        const { opportunityKeyword } = variables;
        showNotification('error', `Workflow Failed for "${opportunityKeyword}"`, err.message)
      },
    }
  );

  const showTrendModal = (opportunity) => {
    setSelectedOpportunity(opportunity);
    setIsTrendModalVisible(true);
  };

  const handleTrendModalCancel = () => {
    setIsTrendModalVisible(false);
    setSelectedOpportunity(null);
  };

  const { mutate: rejectOpportunityMutation, isLoading: isRejecting } = useMutation(
    (opportunityId) => rejectOpportunity(opportunityId),
    {
      onSuccess: () => {
        showNotification('success', 'Opportunity Rejected', 'The opportunity has been marked as rejected.');
        queryClient.invalidateQueries('opportunities');
      },
      onError: (err) => showNotification('error', 'Rejection Failed', err.message),
    }
  );

  const showRejectConfirm = (opportunityId) => {
    confirm({
      title: 'Are you sure you want to reject this opportunity?',
      icon: <ExclamationCircleOutlined />,
      content: 'This action cannot be undone.',
      okText: 'Yes, Reject',
      okType: 'danger',
      cancelText: 'No',
      onOk() {
        rejectOpportunityMutation(opportunityId);
      },
    });
  };

  const renderActions = (_, record) => {
    const isFailed = ['failed', 'rejected'].includes(record.status);
    const isLoading = isStartingWorkflow || isRejecting;

    const buttons = [];

    switch (activeStatus) {
      case 'review':
        buttons.push(
          <Tooltip title="Run Workflow" key="run">
            <Button
              type="primary"
              icon={<RocketOutlined />}
              onClick={(e) => { 
                e.stopPropagation(); 
                console.log('Starting workflow for opportunity:', record.id, 'with override:', isFailed);
                startWorkflowMutation({ opportunityId: record.id, override: isFailed, opportunityKeyword: record.keyword }); 
              }}
              loading={isStartingWorkflow}
              disabled={isLoading}
            />
          </Tooltip>,
          <Tooltip title="Reject Opportunity" key="reject">
            <Button
              danger
              icon={<DeleteOutlined />}
              onClick={(e) => { e.stopPropagation(); showRejectConfirm(record.id); }}
              loading={isRejecting}
              disabled={isLoading}
            />
          </Tooltip>
        );
        break;
      case 'rejected':
      case 'failed':
        buttons.push(
          <Tooltip title="Run Workflow" key="run-failed">
            <Button
              type="primary"
              icon={<RocketOutlined />}
              onClick={(e) => { e.stopPropagation(); startWorkflowMutation({ opportunityId: record.id, override: true }); }}
              loading={isStartingWorkflow}
              disabled={isLoading}
            />
          </Tooltip>
        );
        break;
      default:
        break;
    }

    buttons.push(
      <Tooltip title="View Details" key="view">
        <Button 
          icon={<EditOutlined />} 
          onClick={(e) => { e.stopPropagation(); navigate(`/opportunities/${record.id}`)}} 
        />
      </Tooltip>
    );

    return <Space>{buttons}</Space>;
  };

  const baseColumns = [
    { title: 'Keyword', dataIndex: 'keyword', key: 'keyword', sorter: true, render: (text, record) => <a onClick={(e) => { e.stopPropagation(); navigate(`/opportunities/${record.id}`)}}>{text}</a> },
    { title: 'Search Volume', dataIndex: 'search_volume', key: 'search_volume', sorter: true, render: (sv) => sv ? sv.toLocaleString() : 'N/A' },
    { title: 'KD', dataIndex: 'keyword_difficulty', key: 'keyword_difficulty', sorter: true, render: (kd) => kd != null ? kd : 'N/A' },
    {
      title: 'Trend',
      key: 'trend',
      render: (_, record) => (
        <Button icon={<LineChartOutlined />} onClick={(e) => { e.stopPropagation(); showTrendModal(record); }} />
      ),
    },
  ];

  const rejectedColumns = [
    ...baseColumns,
    { 
      title: 'Rejection Reason', 
      dataIndex: 'blog_qualification_reason', 
      key: 'blog_qualification_reason',
      render: (reason) => reason || <Text type="secondary">No reason provided</Text>
    },
    { title: 'Actions', key: 'actions', fixed: 'right', render: renderActions },
  ];

  const defaultColumns = [
    ...baseColumns,
    { title: 'Strategic Score', dataIndex: 'strategic_score', key: 'strategic_score', sorter: true, render: (score) => score ? <strong>{score.toFixed(1)}</strong> : 'N/A' },
    { title: 'CPC', dataIndex: 'cpc', key: 'cpc', sorter: true, render: (cpc) => cpc ? `$${cpc.toFixed(2)}` : 'N/A' },
    { title: 'Actions', key: 'actions', fixed: 'right', render: renderActions },
  ];

  const columns = activeStatus === 'rejected' ? rejectedColumns : defaultColumns;

  return (
    <Layout style={{ padding: '24px' }}><Content>
      <Title level={2}>Content Opportunities</Title>
      <Card>
        <div className="custom-tabs">
          <Tabs activeKey={activeStatus} onChange={setActiveStatus}>
            {MAIN_STATUSES.map(status => (
              <TabPane 
                tab={
                  <span>
                    {status.replace(/_/g, ' ').toUpperCase()}
                    <Tag color={statusColors[status]} style={{ marginLeft: 8 }}>
                      {statusCounts[status] || 0}
                    </Tag>
                  </span>
                }
                key={status} 
              />
            ))}
          </Tabs>
        </div>
        <Table
          columns={columns}
          dataSource={opportunities}
          rowKey="id"
          loading={isLoading}
          pagination={pagination}
          onChange={handleTableChange}
          onRow={(record) => ({
            onClick: () => navigate(`/opportunities/${record.id}`),
            style: { cursor: 'pointer' },
          })}
          rowClassName="table-row-hover"
        />
      </Card>
      <Modal
        title={`Search Volume Trend for "${selectedOpportunity?.keyword}"`}
        visible={isTrendModalVisible}
        onCancel={handleTrendModalCancel}
        footer={null}
        width={800}
      >
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={selectedOpportunity?.monthly_searches?.map(monthly => ({ month: `${monthly.year}-${String(monthly.month).padStart(2, '0')}`, search_volume: monthly.search_volume }))}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <RechartsTooltip />
            <Legend />
            <Line type="monotone" dataKey="search_volume" stroke="#8884d8" />
          </LineChart>
        </ResponsiveContainer>
      </Modal>
    </Content></Layout>
  );
};

export default OpportunitiesPage;
