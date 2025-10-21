import React from 'react';
import { Card, Statistic, Tooltip } from 'antd';
import { RiseOutlined } from '@ant-design/icons';

const GrowthTrend = ({ scoreBreakdown }) => {
  const growthTrend = scoreBreakdown?.growth_trend;

  if (!growthTrend) {
    return null;
  }

  return (
    <Card>
      <Tooltip title={growthTrend.breakdown['Growth Trend'].explanation}>
        <Statistic
          title="Year-over-Year Growth"
          value={growthTrend.breakdown['Growth Trend'].value}
          prefix={<RiseOutlined />}
          valueStyle={{ color: '#3f8600' }}
        />
      </Tooltip>
    </Card>
  );
};

export default GrowthTrend;
