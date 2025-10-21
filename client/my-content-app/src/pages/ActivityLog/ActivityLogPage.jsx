// This is a new file. Create it with the following content:
import React from 'react';
import { Layout, Typography, Table, Space, Alert, Spin, Button, Tooltip } from 'antd';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { getAllJobs, cancelJob } from '../../services/orchestratorService';
import { formatDistanceToNow, format } from 'date-fns';
import { CloseCircleOutlined } from '@ant-design/icons';
import { useNotifications } from '../../context/NotificationContext';
import JobStatusIndicator from '../../components/JobStatusIndicator'; // NEW

const { Content } = Layout;
const { Title, Text } = Typography;



const ActivityLogPage = () => {
  const queryClient = useQueryClient();
  const { showNotification } = useNotifications();

  const { data: jobs = [], isLoading, isError, error } = useQuery(
    'allJobs',
    getAllJobs,
    {
      refetchInterval: (data) =>
        data?.some((job) => job.status === 'running' || job.status === 'pending') ? 3000 : false, // Refetch every 3s if any job is running
    }
  );

  const { mutate: cancelJobMutation, isLoading: isCancelling } = useMutation(
    (jobId) => cancelJob(jobId),
    {
      onSuccess: () => {
        showNotification('info', 'Job Cancellation', 'Job cancellation request sent.');
        queryClient.invalidateQueries('allJobs'); // Refetch to show updated status
      },
      onError: (err) => {
        showNotification('error', 'Cancellation Failed', err.message || 'An error occurred during cancellation.');
      },
    }
  );

  const columns = [
    {
      title: 'Job ID',
      dataIndex: 'id',
      key: 'id',
      render: (text) => <Text code>{text.substring(0, 8)}...</Text>,
    },
    {
      title: 'Type',
      dataIndex: 'function_name',
      key: 'function_name',
      render: (text) => text ? text.replace(/_background$/, '').replace(/_/g, ' ').replace('run ', '').replace('run', '').trim().toUpperCase() : 'N/A',
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (_, record) => <JobStatusIndicator jobId={record.id} />, // Use the new component
    },
    {
      title: 'Current Step',
      dataIndex: 'result',
      key: 'step',
      render: (result) => result?.step || 'N/A',
    },
    {
      title: 'Started',
      dataIndex: 'started_at',
      key: 'started_at',
      render: (timestamp) => timestamp ? formatDistanceToNow(new Date(timestamp * 1000), { addSuffix: true }) : 'N/A',
    },
    {
      title: 'Finished',
      dataIndex: 'finished_at',
      key: 'finished_at',
      render: (timestamp) => timestamp ? format(new Date(timestamp * 1000), 'MMM d, hh:mm a') : 'N/A',
    },
    {
      title: 'Error',
      dataIndex: 'error',
      key: 'error',
      render: (errorMsg) => errorMsg ? (
        <Tooltip title={errorMsg}>
          <Text type="danger" ellipsis>{errorMsg}</Text>
        </Tooltip>
      ) : 'N/A',
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_, record) => (
        <Space size="small">
          {record.status === 'running' && (
            <Tooltip title="Cancel Job">
              <Button 
                danger 
                icon={<CloseCircleOutlined />} 
                size="small" 
                onClick={() => cancelJobMutation(record.id)} 
                loading={isCancelling} 
              />
            </Tooltip>
          )}
        </Space>
      ),
    },
  ];

  if (isLoading) {
    return <Spin tip="Loading activity log..." style={{ display: 'block', marginTop: '50px' }} />;
  }

  if (isError) {
    return <Alert message="Error" description={error?.message || "Failed to load activity log. Please try again."} type="error" showIcon />;
  }

  return (
    <Layout style={{ padding: '24px' }}>
      <Content>
        <Title level={2}>Activity Log</Title>
        <Table
          columns={columns}
          dataSource={jobs}
          rowKey="id"
          pagination={{ pageSize: 10 }}
          scroll={{ x: 1000 }}
        />
      </Content>
    </Layout>
  );
};

export default ActivityLogPage;
