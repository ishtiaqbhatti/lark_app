import React from 'react';
import { Card, Tag, Statistic, Row, Col, Typography, Progress } from 'antd';
import { format } from 'date-fns';

const { Title, Text } = Typography;

const getStatusColor = (status) => {
  if (status.includes('approved') || status === 'validated') return 'success';
  if (status.includes('paused')) return 'warning';
  if (status.includes('failed')) return 'error';
  return 'processing';
};

const OpportunityHeader = ({ keyword, strategicScore, status, dateAdded, recommendation }) => {
  return (
    <Card style={{ borderRadius: '8px' }}>
      <Row align="middle" justify="space-between">
        <Col>
          <Title level={2} style={{ margin: 0 }}>{keyword}</Title>
          <Tag color={getStatusColor(status)} style={{ marginTop: 8 }}>
            {status.replace(/_/g, ' ').toUpperCase()}
          </Tag>
        </Col>
        <Col>
          <Row align="middle" gutter={32}>
            <Col>
              <Statistic title="Date Added" value={format(new Date(dateAdded), 'MMM d, yyyy')} />
            </Col>
            {recommendation && (
              <Col>
                <Tag color={recommendation === 'Proceed' ? 'success' : 'error'} style={{ fontSize: '1.2rem', padding: '10px' }}>
                  {recommendation}
                </Tag>
              </Col>
            )}
            <Col style={{ textAlign: 'center' }}>
              {typeof strategicScore === 'number' && (
                <>
                  <Progress
                    type="circle"
                    percent={strategicScore}
                    format={(percent) => `${percent.toFixed(1)}`}
                    strokeColor={{
                      '0%': '#B8E1FF',
                      '100%': '#3D76DD',
                    }}
                    size={80}
                  />
                  <Text style={{ display: 'block', marginTop: 8 }}>Strategic Score</Text>
                </>
              )}
            </Col>
          </Row>
        </Col>
      </Row>
    </Card>
  );
};

export default OpportunityHeader;