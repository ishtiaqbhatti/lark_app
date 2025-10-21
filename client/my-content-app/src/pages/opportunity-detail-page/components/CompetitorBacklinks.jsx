import React from 'react';
import { Card, Statistic, Row, Col, Tooltip } from 'antd';
import { LinkOutlined, TeamOutlined, RiseOutlined } from '@ant-design/icons';

const CompetitorBacklinks = ({ avgBacklinksInfo }) => {
  if (!avgBacklinksInfo) {
    return <Card title="Competitor Backlink Analysis">No data available.</Card>;
  }

  const { backlinks, referring_domains, main_domain_rank } = avgBacklinksInfo;

  return (
    <Card title="Competitor Backlink Analysis">
      <Row gutter={16}>
        <Col span={8}>
          <Tooltip title="The average number of backlinks for the top-ranking pages.">
            <Statistic title="Avg. Backlinks" value={backlinks} prefix={<LinkOutlined />} />
          </Tooltip>
        </Col>
        <Col span={8}>
          <Tooltip title="The average number of unique domains linking to the top-ranking pages.">
            <Statistic title="Avg. Referring Domains" value={referring_domains} prefix={<TeamOutlined />} />
          </Tooltip>
        </Col>
        <Col span={8}>
          <Tooltip title="The average Domain Rank (a measure of a website's authority) of the top-ranking pages.">
            <Statistic title="Avg. Domain Rank" value={main_domain_rank} prefix={<RiseOutlined />} />
          </Tooltip>
        </Col>
      </Row>
    </Card>
  );
};

export default CompetitorBacklinks;
