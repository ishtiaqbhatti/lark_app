import React, { useState } from 'react';
import { Layout, Typography, Table, Tag, Button, Space, Tooltip, Modal, Card, Tabs, Input } from 'antd';
import { RocketOutlined, EditOutlined, DeleteOutlined, ExclamationCircleOutlined, SearchOutlined } from '@ant-design/icons';
import { useOpportunities } from './hooks/useOpportunities';
import { useNotifications } from '../../context/NotificationContext';
import { useMutation, useQueryClient } from 'react-query';
import { startFullWorkflow, rejectOpportunity } from '../../services/orchestratorService';
import JobStatusIndicator from '../../components/JobStatusIndicator';
import { useJobs } from '../../context/JobContext';
import { useNavigate } from 'react-router-dom';
import { formatNumber, formatCurrency } from '../../utils/formatters';
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
    handleTableChange, activeStatus, setActiveStatus, statusCounts = {}, handleSearch
  } = useOpportunities();
  const { showNotification } = useNotifications();
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const { activeJobs } = useJobs();
  const [selectedRowKeys, setSelectedRowKeys] = useState([]);

  const { mutate: startWorkflowMutation, isLoading: isStartingWorkflow } = useMutation(
    ({ opportunityId, override, opportunityKeyword }) => startFullWorkflow(opportunityId, override),
    {
      onSuccess: (data, variables) => {
            const { opportunityKeyword } = variables;
            showNotification('success', 'Workflow Started', `A new workflow has been queued for "${opportunityKeyword}".`);
            queryClient.invalidateQueries('opportunities');
            queryClient.invalidateQueries('activeJobs');
          },
      onError: (err, variables) => {
        const { opportunityKeyword } = variables;
        showNotification('error', `Workflow Failed for "${opportunityKeyword}"`, err.message)
      },
    }
  );

  const { mutate: rejectOpportunityMutation, isLoading: isRejecting } = useMutation(
    (opportunityId) => rejectOpportunity(opportunityId),
    {
      onSuccess: () => {
        showNotification('success', 'Opportunity Rejected', 'The opportunity has been marked as rejected.');
        queryClient.invalidateQueries('opportunities');
        queryClient.invalidateQueries('dashboardStats');
      },
      onError: (err) => showNotification('error', 'Rejection Failed', err.message),
    }
  );

  const { mutate: bulkRejectMutation, isLoading: isBulkRejecting } = useMutation(
    (ids) => Promise.all(ids.map(id => rejectOpportunity(id))), // Assuming rejectOpportunity takes one ID
    {
      onSuccess: () => {
        showNotification('success', 'Bulk Action', `${selectedRowKeys.length} opportunities have been rejected.`);
        setSelectedRowKeys([]);
        queryClient.invalidateQueries('opportunities');
        queryClient.invalidateQueries('dashboardStats');
      },
      onError: (err) => showNotification('error', 'Bulk Rejection Failed', err.message),
    }
  );

  const handleBulkReject = () => {
    confirm({
      title: `Are you sure you want to reject these ${selectedRowKeys.length} opportunities?`,
      icon: <ExclamationCircleOutlined />,
      content: 'This action cannot be undone.',
      okText: 'Yes, Reject All',
      okType: 'danger',
      cancelText: 'No',
      onOk() {
        bulkRejectMutation(selectedRowKeys);
      },
    });
  };

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
        const isLoading = isStartingWorkflow || isRejecting || isBulkRejecting;
    
        const buttons = [];
    
        switch (record.status) { // Changed to check record.status
          case 'review':
          case 'validated': // Can start workflow from validated too
            buttons.push(
              <Tooltip title="Start Full Workflow" key="run">
                <Button
                  type="primary"
                  aria-label="Start Full Workflow"
                  icon={<RocketOutlined />}
                  onClick={(e) => { 
                    e.stopPropagation(); 
                    startWorkflowMutation({ opportunityId: record.id, override: false, opportunityKeyword: record.keyword }); 
                  }}
                  loading={isStartingWorkflow}
                  disabled={isLoading}
                />
              </Tooltip>,
              <Tooltip title="Reject Opportunity" key="reject">
                <Button
                  danger
                  aria-label="Reject Opportunity"
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
              <Tooltip title="Rerun Workflow" key="run-failed">
                <Button
                  type="primary"
                  aria-label="Rerun Workflow"
                  icon={<RocketOutlined />}
                  onClick={(e) => { e.stopPropagation(); startWorkflowMutation({ opportunityId: record.id, override: true, opportunityKeyword: record.keyword }); }}
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
              aria-label="View Details"
              icon={<EditOutlined />} 
              onClick={(e) => { e.stopPropagation(); navigate(`/opportunities/${record.id}`)}} 
            />
          </Tooltip>
        );
    
        return <Space>{buttons}</Space>;
      };
    
      const columns = [
        { title: 'Keyword', dataIndex: 'keyword', key: 'keyword', sorter: true, render: (text, record) => <a onClick={(e) => { e.stopPropagation(); navigate(`/opportunities/${record.id}`)}}>{text}</a> },
        { title: 'Search Volume', dataIndex: 'search_volume', key: 'search_volume', sorter: true, render: (sv) => formatNumber(sv) },
        { title: 'KD', dataIndex: 'keyword_difficulty', key: 'keyword_difficulty', sorter: true, render: (kd) => kd != null ? kd : 'N/A' },
        { 
          title: 'Intent', 
          dataIndex: 'main_intent', 
          key: 'main_intent', 
          render: (intent) => intent ? <Tag>{intent.toUpperCase()}</Tag> : 'N/A',
          hidden: activeStatus === 'rejected',
        },
        { 
          title: 'Strategic Score', 
          dataIndex: 'strategic_score', 
          key: 'strategic_score', 
          sorter: true, 
          render: (score) => score ? <strong>{score.toFixed(1)}</strong> : 'N/A',
          hidden: activeStatus === 'rejected',
        },
        { title: 'CPC', dataIndex: 'cpc', key: 'cpc', sorter: true, render: (cpc) => formatCurrency(cpc) },
        { 
          title: 'Rejection Reason', 
          dataIndex: 'blog_qualification_reason', 
          key: 'blog_qualification_reason',
          render: (reason) => reason || <Text type="secondary">No reason provided</Text>,
          hidden: activeStatus !== 'rejected',
        },
        {
          title: 'Actions',
          key: 'actions',
          fixed: 'right',
          width: 120,
          render: (_, record) => {
            const activeJob = activeJobs.find(job => job.id === record.latest_job_id);
            
            if (activeJob) {
              return <JobStatusIndicator jobId={activeJob.id} />;
            }
            
            return renderActions(_, record);
          }
        },
      ].filter(col => !col.hidden);

  return (
    <Layout style={{ padding: '24px' }}><Content>
      <Title level={2}>Content Opportunities</Title>
      <Input
        placeholder="Search keywords..."
        prefix={<SearchOutlined />}
        allowClear
        onChange={(e) => handleSearch(e.target.value)}
        style={{ width: 300, marginBottom: 16 }}
      />
      <Space style={{ marginBottom: 16 }}>
          <Button
            danger
            onClick={handleBulkReject}
            disabled={selectedRowKeys.length === 0}
            loading={isBulkRejecting}
            icon={<DeleteOutlined />}
          >
            Reject Selected ({selectedRowKeys.length})
          </Button>
      </Space>
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
          rowSelection={{
            selectedRowKeys,
            onChange: setSelectedRowKeys,
          }}
          onRow={(record) => ({
            // The click is now handled exclusively by the `<a>` tag on the keyword.
            style: { 
              opacity: isBulkRejecting && selectedRowKeys.includes(record.id) ? 0.5 : 1,
              transition: 'opacity 0.2s',
            },
          })}
          rowClassName="table-row-hover"
        />
      </Card>
    </Content></Layout>
  );
};

export default OpportunitiesPage;
