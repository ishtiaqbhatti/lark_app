import React, { useEffect, useState } from 'react';
import { Card, Steps, Spin, Alert, Button } from 'antd';
import { useQuery, useQueryClient } from 'react-query';
import { useNavigate } from 'react-router-dom';
import { getJobStatus } from '../../../services/jobsService';
import { CheckCircleOutlined } from '@ant-design/icons';

const { Step } = Steps;

const IN_PROGRESS_STATUSES = ['processing', 'running', 'in_progress', 'pending', 'refresh_started'];

const WorkflowTracker = ({ opportunity }) => {
  const { latest_job_id, status, error_message } = opportunity;
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: jobStatus, isLoading: isLoadingStatus } = useQuery(
    ['jobStatus', latest_job_id],
    () => getJobStatus(latest_job_id),
    {
      enabled: !!latest_job_id && (!jobStatus || (jobStatus.status !== 'completed' && jobStatus.status !== 'failed')),
      refetchInterval: 3000, // Poll every 3 seconds for faster updates
      onSuccess: (data) => {
        if (data?.status === 'completed' || data?.status === 'failed' || data?.status === 'paused') {
          // Invalidate queries to refetch the main opportunity data for the page
          queryClient.invalidateQueries(['opportunity', opportunity.id]);
        }
        
        if (data?.status === 'completed' && data.result?.redirect_url) {
          setTimeout(() => {
            navigate(data.result.redirect_url);
          }, 1500); // Delay for user to see the final success state
        }
      },
    }
  );

  const progressLog = jobStatus?.progress_log || [];
  const currentStepIndex = progressLog.length > 0 ? progressLog.length - 1 : 0;

  // Don't render anything if there's no job or the workflow is in a non-terminal, non-processing state
  if (!latest_job_id || (!IN_PROGRESS_STATUSES.includes(status) && status !== 'failed' && jobStatus?.status !== 'completed')) {
    return null;
  }

  const isJobRunning = jobStatus?.status === 'running' || jobStatus?.status === 'pending';

  return (
    <Card title="Workflow Status" style={{ marginTop: 24 }}>
      {isLoadingStatus && !jobStatus && <Spin tip="Initializing workflow status..." />}
      
      {progressLog.length > 0 && (
        <Steps direction="vertical" current={currentStepIndex}>
          {progressLog.map((log, index) => (
            <Step 
              key={index} 
              title={log.step} 
              description={log.message} 
              icon={isJobRunning && index === currentStepIndex ? <Spin /> : null}
            />
          ))}
        </Steps>
      )}

      {jobStatus?.status === 'completed' && (
        <Alert
          message="Workflow Completed"
          description={jobStatus.result?.message || 'The workflow finished successfully.'}
          type="success"
          showIcon
          icon={<CheckCircleOutlined />}
          action={
            jobStatus.result?.redirect_url && (
              <Button size="small" type="primary" onClick={() => navigate(jobStatus.result.redirect_url)}>
                Go to Results
              </Button>
            )
          }
        />
      )}

      {jobStatus?.status === 'failed' && (
        <Alert
          message="Workflow Failed"
          description={jobStatus.error || error_message || 'An unknown error occurred.'}
          type="error"
          showIcon
        />
      )}
    </Card>
  );
};

export default WorkflowTracker;
