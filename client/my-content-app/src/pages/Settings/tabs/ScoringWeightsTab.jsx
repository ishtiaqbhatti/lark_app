// This is a new file. Create it with the following content:
import React from 'react';
import { Form, Slider, InputNumber, Typography, Row, Col, Divider, Tooltip, Space, Alert } from 'antd';
import { InfoCircleOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;

const ScoringWeightsTab = ({ settings, form }) => {
  const allWeights = Form.useWatch([
    'ease_of_ranking_weight',
    'traffic_potential_weight',
    'commercial_intent_weight',
    'serp_features_weight',
    'growth_trend_weight',
    'serp_freshness_weight',
    'serp_volatility_weight',
    'competitor_weakness_weight'
  ], form);

  const totalWeight = Object.values(allWeights || {}).reduce((sum, current) => sum + (current || 0), 0);

  const renderWeightInput = (name, label, tooltip) => (
    <Col span={24}>
      <Form.Item 
        name={name} 
        label={
          <Space>
            {label}
            {tooltip && <Tooltip title={tooltip}><InfoCircleOutlined /></Tooltip>}
          </Space>
        }
        rules={[{ required: true, message: 'Weight is required' }]}
        style={{ marginBottom: 0 }}
      >
        <Row>
          <Col span={18}>
            <Slider min={0} max={100} step={1} style={{ margin: '0 8px' }} />
          </Col>
          <Col span={4}>
            <InputNumber min={0} max={100} step={1} style={{ width: '100%' }} />
          </Col>
        </Row>
      </Form.Item>
    </Col>
  );

  return (
    <>
      <Title level={5}>Strategic Scoring Weights (Sum to {totalWeight}%)</Title>
      {totalWeight !== 100 && (
        <Alert
          message="Warning: Total weight is not 100%"
          description="The sum of all weights should ideally be 100% for proper normalization. Consider adjusting your weights."
          type="warning"
          showIcon
          style={{ marginBottom: '16px' }}
        />
      )}
      <Row gutter={16}>
        {renderWeightInput('ease_of_ranking_weight', 'Ease of Ranking', 'How easy it is to rank (based on KD, backlinks).')}
        {renderWeightInput('traffic_potential_weight', 'Traffic Potential', 'How much traffic the keyword can bring (based on Search Volume).')}
        {renderWeightInput('commercial_intent_weight', 'Commercial Intent', 'How likely the keyword is to lead to a conversion (based on CPC, intent type).')}
        {renderWeightInput('serp_features_weight', 'SERP Features', 'Impact of rich SERP features (Featured Snippets, AI Overviews).')}
        {renderWeightInput('growth_trend_weight', 'Growth Trend', 'How quickly the search volume is growing or declining.')}
        {renderWeightInput('serp_freshness_weight', 'SERP Freshness', 'How recently the SERP was updated (opportunity if stale).')}
        {renderWeightInput('serp_volatility_weight', 'SERP Volatility', 'How often the SERP changes (opportunity if stable).')}
        {renderWeightInput('competitor_weakness_weight', 'Competitor Weakness', 'Exploitable technical or content flaws of top competitors.')}
      </Row>

      <Divider />

      <Title level={5}>Scoring Normalization Values</Title>
      <Row gutter={16}>
        <Col span={12}>
          <Form.Item name="max_cpc_for_scoring" label="Max CPC for Scoring">
            <InputNumber min={0.0} step={1.0} style={{ width: '100%' }} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="max_sv_for_scoring" label="Max Search Volume for Scoring">
            <InputNumber min={0} step={1000} style={{ width: '100%' }} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="max_domain_rank_for_scoring" label="Max Domain Rank for Scoring">
            <InputNumber min={0} step={100} style={{ width: '100%' }} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="max_referring_domains_for_scoring" label="Max Referring Domains for Scoring">
            <InputNumber min={0} step={50} style={{ width: '100%' }} />
          </Form.Item>
        </Col>
      </Row>
    </>
  );
};

export default ScoringWeightsTab;