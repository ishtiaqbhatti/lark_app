import React from 'react';
import { Card, Typography, List, Row, Col } from 'antd';
import { CheckCircleOutlined, CloseCircleOutlined } from '@ant-design/icons';
import NoData from './NoData';

const { Title } = Typography;

const FactorsCard = ({ positiveFactors, negativeFactors }) => {
  return (
    <Card style={{ marginTop: 24 }}>
      <Row gutter={16}>
        <Col span={12}>
          <Title level={5}>Positive Factors</Title>
          <List
            dataSource={positiveFactors}
            renderItem={(item) => (
              <List.Item>
                <CheckCircleOutlined style={{ color: 'green', marginRight: '8px' }} /> {item}
              </List.Item>
            )}
          />
        </Col>
        <Col span={12}>
          <Title level={5}>Negative Factors</Title>
          {negativeFactors && negativeFactors.length > 0 ? (
            <List
              dataSource={negativeFactors}
              renderItem={(item) => (
                <List.Item>
                  <CloseCircleOutlined style={{ color: 'red', marginRight: '8px' }} /> {item}
                </List.Item>
              )}
            />
          ) : (
            <NoData description="No negative factors identified." />
          )}
        </Col>
      </Row>
    </Card>
  );
};

export default FactorsCard;
