import React from 'react';
import { Card, Statistic, Row, Col, Tooltip, Tag } from 'antd';
import { BarChartOutlined, DollarCircleOutlined, ThunderboltOutlined, InfoCircleOutlined } from '@ant-design/icons';
import { Line } from '@ant-design/plots';

const KeywordMetrics = ({ keywordInfo, keywordProperties }) => {
  if (!keywordInfo || !keywordProperties) {
    return <Card title="Keyword Metrics">No data available.</Card>;
  }

  const { search_volume, cpc, competition, monthly_searches, competition_level, low_top_of_page_bid, high_top_of_page_bid } = keywordInfo;
  const { keyword_difficulty } = keywordProperties;

  const chartData = monthly_searches?.map(item => ({
    date: `${item.year}-${item.month}`,
    volume: item.search_volume,
  }));

  const chartConfig = {
    data: chartData,
    xField: 'date',
    yField: 'volume',
    height: 200,
    point: {
      size: 5,
      shape: 'diamond',
    },
    tooltip: {
      formatter: (datum) => {
        return { name: 'Search Volume', value: datum.volume.toLocaleString() };
      },
    },
  };

  return (
    <Card title="Keyword Metrics">
      <Row gutter={[16, 24]}>
        <Col span={12}>
          <Tooltip title="The average number of times this keyword is searched for per month.">
            <Statistic title="Search Volume" value={search_volume} prefix={<BarChartOutlined />} />
          </Tooltip>
        </Col>
        <Col span={12}>
          <Tooltip title="The average cost per click for this keyword in paid search campaigns.">
            <Statistic title="CPC" value={cpc} prefix={<DollarCircleOutlined />} precision={2} />
          </Tooltip>
        </Col>
        <Col span={12}>
          <Tooltip title="The level of competition for this keyword in paid search campaigns, on a scale of 0 to 1.">
            <div>
              <Statistic title="Competition" value={competition} precision={2} />
              <Tag color={competition_level === 'LOW' ? 'green' : competition_level === 'MEDIUM' ? 'orange' : 'red'}>{competition_level}</Tag>
            </div>
          </Tooltip>
        </Col>
        <Col span={12}>
          <Tooltip title="An estimate of how difficult it would be to rank organically for this keyword, on a scale of 0 to 100.">
            <Statistic title="Keyword Difficulty" value={keyword_difficulty} prefix={<ThunderboltOutlined />} />
          </Tooltip>
        </Col>
        <Col span={12}>
          <Tooltip title="The lower range of what advertisers have historically paid for a top-of-page bid.">
            <Statistic title="Low Top of Page Bid" value={low_top_of_page_bid} precision={2} prefix="$" />
          </Tooltip>
        </Col>
        <Col span={12}>
          <Tooltip title="The higher range of what advertisers have historically paid for a top-of-page bid.">
            <Statistic title="High Top of Page Bid" value={high_top_of_page_bid} precision={2} prefix="$" />
          </Tooltip>
        </Col>
      </Row>
      <div style={{ marginTop: '24px' }}>
        {chartData && chartData.length > 0 ? (
          <Line {...chartConfig} />
        ) : (
          <div style={{ textAlign: 'center', padding: '20px' }}>
            <InfoCircleOutlined style={{ marginRight: '8px' }} />
            No monthly search volume data available to display a chart.
          </div>
        )}
      </div>
    </Card>
  );
};

export default KeywordMetrics;
