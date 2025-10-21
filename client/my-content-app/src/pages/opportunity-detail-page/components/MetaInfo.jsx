import React from 'react';
import { Card, Descriptions, Tag } from 'antd';
import { InfoCircleOutlined, DollarCircleOutlined, HistoryOutlined } from '@ant-design/icons';
import { format } from 'date-fns';

const MetaInfo = ({ blueprint, lastWorkflowStep, dateProcessed }) => {
  const metadata = blueprint?.metadata;

  return (
    <Card title="Process Metadata" icon={<InfoCircleOutlined />}>
      <Descriptions column={1} size="small" variant="outlined">
        {metadata?.blueprint_version && (
          <Descriptions.Item label="Blueprint Version">
            <Tag>{metadata.blueprint_version}</Tag>
          </Descriptions.Item>
        )}
        {lastWorkflowStep && (
          <Descriptions.Item label="Last Workflow Step">
            <Tag color="blue">{lastWorkflowStep.replace(/_/g, ' ')}</Tag>
          </Descriptions.Item>
        )}
        {dateProcessed && (
          <Descriptions.Item label="Date Processed">
            <HistoryOutlined /> {format(new Date(dateProcessed), 'MMM d, yyyy HH:mm')}
          </Descriptions.Item>
        )}
        {metadata?.total_api_cost && (
          <Descriptions.Item label="Analysis API Cost">
            <DollarCircleOutlined /> ${metadata.total_api_cost.toFixed(4)}
          </Descriptions.Item>
        )}
      </Descriptions>
    </Card>
  );
};

export default MetaInfo;
