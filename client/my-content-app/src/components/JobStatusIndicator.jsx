import React from 'react';
import { useQuery } from 'react-query';
import { getJobStatus } from '../services/orchestratorService'; // This service function needs to be created
import { Progress, Tag, Tooltip } from 'antd';
import { LoadingOutlined, CheckCircleOutlined, CloseCircleOutlined, ClockCircleOutlined, PauseCircleOutlined } from '@ant-design/icons'; // ADD PauseCircleOutlined

const JobStatusIndicator = ({ jobId }) => {
  const { data: job, isLoading } = useQuery(
    ['jobStatus', jobId],
    () => getJobStatus(jobId),
    {
      refetchInterval: (data) => (data?.status === 'running' || data?.status === 'pending' || data?.status === 'paused' ? 3000 : false), // Refetch for paused jobs too
      enabled: !!jobId,
    }
  );

  if (isLoading && !job) return <Tag icon={<LoadingOutlined spin />}>Loading...</Tag>;
  if (!job) return <Tag>Unknown</Tag>;

  const statusConfig = {
    pending: { icon: <LoadingOutlined />, color: 'default', text: 'Pending' },
    running: { icon: <LoadingOutlined spin />, color: 'processing', text: job.result?.step || 'Running...' },
    completed: { icon: <CheckCircleOutlined />, color: 'success', text: 'Completed' },
    failed: { icon: <CloseCircleOutlined />, color: 'error', text: 'Failed' },
    paused: { icon: <PauseCircleOutlined />, color: 'warning', text: 'Paused (Awaiting Approval)' }, // NEW text
  };
  
  const config = statusConfig[job.status] || { icon: <ClockCircleOutlined />, color: 'default', text: 'Queued' };

  return (
    <Tooltip title={job.error || job.result?.message || job.status_message}> {/* Include job.status_message */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
        <Tag icon={config.icon} color={config.color}>{config.text}</Tag>
        {(job.status === 'running' || job.status === 'paused') && ( // Show progress for paused as well
          <Progress percent={job.progress} size="small" status="active" showInfo={false} style={{ width: '100px', margin: 0 }} />
        )}
      </div>
    </Tooltip>
  );
};
export default JobStatusIndicator;
