import React, { useState, useEffect } from 'react';
import { Modal, Typography, Descriptions, Tag, Row, Col, Alert, Space, Spin, Popover, Progress } from 'antd';
import {
  BarChartOutlined, FireOutlined, ThunderboltOutlined, CalendarOutlined, GlobalOutlined, SmileOutlined,
  BuildOutlined, StarOutlined, UsergroupAddOutlined, ApartmentOutlined, WarningOutlined, RiseOutlined,
  DashboardOutlined, BulbOutlined, InfoCircleOutlined
} from '@ant-design/icons';
import { getScoreNarrative } from '../../../services/orchestratorService';

const { Title, Text, Paragraph } = Typography;

const factorExplanations = {
  ease_of_ranking: "How hard it is to rank on the first page of Google for this keyword. It looks at competitor strength and keyword difficulty.",
  traffic_potential: "An estimate of the traffic you could get if you rank for this keyword, based on search volume and click-through rates.",
  commercial_intent: "How likely a user searching for this keyword is to make a purchase or take a commercial action.",
  growth_trend: "Whether this keyword is becoming more or less popular over time.",
  serp_features: "Measures the presence of special search results like Featured Snippets or People Also Ask boxes, which can affect click-through rates.",
  serp_volatility: "How often the search results for this keyword change. High volatility can mean it's easier to break in, but also harder to hold a position.",
  competitor_weakness: "Analyzes the weaknesses of the top-ranking competitors, such as their backlink profiles and domain authority.",
  serp_crowding: "How many non-traditional results (like ads, images, videos) are on the page, which can push organic results down.",
  keyword_structure: "Analyzes the keyword itself, like its length. Longer keywords are often more specific and easier to rank for.",
  serp_threat: "Identifies major, authoritative domains (like Wikipedia, government sites) that are very difficult to outrank.",
  volume_volatility: "How much the search volume fluctuates month-to-month. High volatility can indicate seasonality.",
  serp_freshness: "How recently the search results have been updated. Older results can be easier to displace.",
  competitor_performance: "A technical analysis of competitor websites, looking at things like page load speed and mobile-friendliness.",
};


const ScoreBreakdownModal = ({ open, onCancel, opportunity }) => {
  const [narrative, setNarrative] = useState('');
  const [isLoadingNarrative, setIsLoadingNarrative] = useState(false);

  useEffect(() => {
    if (open && opportunity?.id) {
      setIsLoadingNarrative(true);
      getScoreNarrative(opportunity.id)
        .then(response => {
          setNarrative(response.data.narrative);
        })
        .catch(err => {
          console.error("Failed to fetch score narrative:", err);
          setNarrative("Could not load the strategic summary.");
        })
        .finally(() => {
          setIsLoadingNarrative(false);
        });
    } else {
      setNarrative('');
    }
  }, [open, opportunity]);

  const keyword = opportunity?.keyword;
  const scoreBreakdown = opportunity?.score_breakdown;

  if (!scoreBreakdown) {
    return <Modal title="Score Breakdown" open={open} onCancel={onCancel} footer={null}><Alert message="No score breakdown available for this opportunity." type="info" showIcon /></Modal>;
  }

  const getScoreColor = (score) => {
    if (score >= 80) return 'success';
    if (score >= 60) return 'processing';
    if (score >= 40) return 'warning';
    return 'error';
  };

  const renderFactor = (factorKey, icon) => {
    const factor = scoreBreakdown[factorKey];
    if (!factor) return null;

    const mainExplanation = factorExplanations[factorKey] || "No explanation available.";

    return (
      <Col span={24} style={{ marginBottom: 16 }}>
        <div style={{ background: '#fafafa', padding: '12px 16px', borderRadius: '8px' }}>
          <Row align="middle" justify="space-between">
            <Col>
              <Space align="center">
                {icon}
                <Title level={5} style={{ margin: 0 }}>{factor.name}</Title>
                <Popover content={<Paragraph style={{ maxWidth: 300 }}>{mainExplanation}</Paragraph>} trigger="hover">
                  <InfoCircleOutlined style={{ color: 'rgba(0, 0, 0, 0.45)', cursor: 'pointer' }} />
                </Popover>
              </Space>
            </Col>
            <Col>
              <Space>
                <Text type="secondary" style={{ fontSize: '0.9em' }}>Weight: {factor.weight || 0}%</Text>
                <Progress type="circle" percent={factor.score} width={40} format={percent => `${percent}`} status={getScoreColor(factor.score)} />
              </Space>
            </Col>
          </Row>
          <Descriptions column={1} size="small" style={{ marginTop: 12 }}>
            {Object.entries(factor.breakdown || {}).map(([subFactorKey, subFactor]) => (
              <Descriptions.Item key={subFactorKey} label={<Text strong>{subFactorKey}</Text>}>
                <Row justify="space-between" align="top">
                  <Col span={16}>
                    <Space direction="vertical" size={0}>
                      <Text>{subFactor.value}</Text>
                      {subFactor.explanation && <Paragraph type="secondary" style={{ margin: 0, fontSize: '0.85em' }}>{subFactor.explanation}</Paragraph>}
                    </Space>
                  </Col>
                  <Col span={4} style={{ textAlign: 'right' }}>
                    {subFactor.score !== undefined && <Tag color={getScoreColor(subFactor.score)}>{subFactor.score?.toFixed(0)}</Tag>}
                  </Col>
                </Row>
              </Descriptions.Item>
            ))}
             {factor.breakdown?.message && <Alert message={factor.breakdown.message} type="warning" showIcon style={{width: '100%'}}/>}
          </Descriptions>
        </div>
      </Col>
    );
  };

  return (
    <Modal
      title={<Title level={4} style={{ margin: 0 }}>Strategic Score Breakdown: &quot;{keyword}&quot;</Title>}
      open={open}
      onCancel={onCancel}
      footer={null}
      width={800}
    >
      {isLoadingNarrative ? (
        <Spin tip="Loading AI-powered summary..." />
      ) : (
        narrative && <Alert message="Strategic Summary" description={<Paragraph style={{ whiteSpace: 'pre-wrap' }}>{narrative}</Paragraph>} type="info" showIcon icon={<BulbOutlined />} style={{ marginBottom: '24px' }} />
      )}
      <Row gutter={[16, 16]}>
        {renderFactor('ease_of_ranking', <BarChartOutlined />)}
        {renderFactor('traffic_potential', <FireOutlined />)}
        {renderFactor('commercial_intent', <ThunderboltOutlined />)}
        {renderFactor('growth_trend', <RiseOutlined />)}
        {renderFactor('serp_features', <StarOutlined />)}
        {renderFactor('competitor_weakness', <BuildOutlined />)}
        {renderFactor('serp_volatility', <SmileOutlined />)}
        {renderFactor('serp_crowding', <UsergroupAddOutlined />)}
        {renderFactor('keyword_structure', <ApartmentOutlined />)}
        {renderFactor('serp_threat', <WarningOutlined />)}
        {renderFactor('volume_volatility', <CalendarOutlined />)}
        {renderFactor('serp_freshness', <GlobalOutlined />)}
        {renderFactor('competitor_performance', <DashboardOutlined />)}
      </Row>
    </Modal>
  );
};

export default ScoreBreakdownModal;
