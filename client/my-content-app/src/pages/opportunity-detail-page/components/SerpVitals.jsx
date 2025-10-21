import React from 'react';
import { Card, Row, Col, Statistic, Tooltip } from 'antd';
import { CloudSyncOutlined, AlertOutlined } from '@ant-design/icons';

const SerpVitals = ({ scoreBreakdown }) => {
  const volatility = scoreBreakdown?.serp_volatility;
  const crowding = scoreBreakdown?.serp_crowding;

  if (!volatility && !crowding) {
    return null;
  }

  return (
    <Card title="SERP Vitals">
      <Row gutter={16}>
        {volatility && (
          <Col span={12}>
            <Tooltip title={volatility.breakdown['SERP Stability'].explanation}>
              <Statistic 
                title="SERP Stability" 
                value={volatility.breakdown['SERP Stability'].value} 
                prefix={<CloudSyncOutlined />} 
              />
            </Tooltip>
          </Col>
        )}
        {crowding && (
          <Col span={12}>
            <Tooltip title={crowding.breakdown['SERP Crowding'].explanation}>
              <Statistic 
                title="SERP Crowding" 
                value={`${crowding.breakdown['SERP Crowding'].value} Features`}
                prefix={<AlertOutlined />} 
              />
            </Tooltip>
          </Col>
        )}
      </Row>
    </Card>
  );
};

export default SerpVitals;
