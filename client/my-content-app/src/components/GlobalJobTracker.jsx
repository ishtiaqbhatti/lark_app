import React from 'react';
import { Alert, Spin } from 'antd';
import { useJobs } from '../context/JobContext';
import { CheckCircleOutlined, CloseCircleOutlined } from '@ant-design/icons';

const GlobalJobTracker = () => {
  const { activeJobs } = useJobs();

  if (Object.keys(activeJobs).length === 0) {
    return null;
  }

  return (
    <div style={{ position: 'fixed', bottom: 24, right: 24, zIndex: 1000, display: 'flex', flexDirection: 'column', gap: '16px' }}>
      {Object.entries(activeJobs).map(([jobId, job]) => {
        let icon, type;
        switch (job.status) {
          case 'running':
            icon = <Spin />;
            type = 'info';
            break;
          case 'completed':
            icon = <CheckCircleOutlined />;
            type = 'success';
            break;
          case 'failed':
            icon = <CloseCircleOutlined />;
            type = 'error';
            break;
          default:
            icon = <Spin />;
            type = 'info';
        }

        return (
          <Alert
            key={jobId}
            message={`Job Status: ${job.status.charAt(0).toUpperCase() + job.status.slice(1)}`}
            description={job.message}
            type={type}
            showIcon
            icon={icon}
            style={{ boxShadow: '0 2px 8px rgba(0,0,0,0.15)' }}
          />
        );
      })}
    </div>
  );
};

export default GlobalJobTracker;
