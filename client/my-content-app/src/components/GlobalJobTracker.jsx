import React from 'react';
import { Alert, Spin } from 'antd';
import { useJobs } from '../context/JobContext';
import { CheckCircleOutlined, CloseCircleOutlined, LoadingOutlined, ClockCircleOutlined } from '@ant-design/icons';

const GlobalJobTracker = () => {
  const { activeJobs } = useJobs();

  if (!activeJobs || activeJobs.length === 0) {
    return null;
  }

  return (
    <div style={{ position: 'fixed', bottom: 24, right: 24, zIndex: 1000, display: 'flex', flexDirection: 'column', gap: '16px' }}>
      {activeJobs.map((job) => {
        const { id, status, result, error, function_name } = job;

        let icon, type, message, description;
        const jobTitle = function_name ? function_name.replace(/_/g, ' ').replace(/_background/g, '').replace('run ', '').trim().toUpperCase() : 'Job';
        
        switch (status) {
          case 'running':
            icon = <Spin />;
            type = 'info';
            message = `${jobTitle} in Progress`;
            description = result?.step || result?.message || 'Processing...';
            break;
          case 'pending':
            icon = <ClockCircleOutlined />;
            type = 'info';
            message = `${jobTitle} is Pending`;
            description = 'The job is queued and will start shortly.';
            break;
          case 'completed':
            return null;
          case 'failed':
            icon = <CloseCircleOutlined />;
            type = 'error';
            message = `${jobTitle} Failed`;
            description = error || 'An unknown error occurred.';
            break;
          default:
            return null;
        }

        return (
          <Alert
            key={id}
            message={message}
            description={description}
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
