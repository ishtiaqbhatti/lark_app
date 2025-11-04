import React from 'react';
import { Modal, Tag, Row, Col, Descriptions, Statistic, Steps, Card, Typography } from 'antd';
import { formatDistanceStrict } from 'date-fns';
import PieChartCard from './PieChartCard';
import DiscoveryStatsBreakdown from './DiscoveryStatsBreakdown'; 

const { Title, Text } = Typography;
const { Step } = Steps;

const STATUS_CONFIG = {
  completed: { color: 'success', text: 'Completed' },
  failed: { color: 'error', text: 'Failed' },
  running: { color: 'processing', text: 'Running' },
  pending: { color: 'default', text: 'Pending' },
};

const RunDetailsModal = ({ run, open, onCancel }) => {
  if (!run) return null;

  const {
    id,
    start_time,
    end_time,
    status,
    parameters = {},
    results_summary = {},
  } = run;

  const {
    total_cost = 0,
    source_counts = {},
    total_raw_count = 0,
    total_unique_count = 0,
    final_qualified_count = 0,
    duplicates_removed = 0,
    final_added_to_db = 0,
    disqualification_reasons = {},
  } = results_summary;

  const statusInfo = STATUS_CONFIG[status] || STATUS_CONFIG.pending;

  const expandedRowRender = (record) => {
    if (!record.results_summary) {
      return <Text type="secondary">No detailed summary available for this run.</Text>;
    }
    return <DiscoveryStatsBreakdown summary={record.results_summary} runId={record.id} />;
  };

  return (
    <Modal
      title={
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <Title level={4} style={{ margin: 0 }}>Discovery Run #{id}</Title>
          <Tag color={statusInfo.color} style={{ marginLeft: '12px' }}>{statusInfo.text}</Tag>
        </div>
      }
      open={open}
      onCancel={onCancel}
      footer={null}
      width="80vw"
      style={{ top: 20 }}
    >
      {/* Key Metrics */}
      <Row gutter={[32, 16]} style={{ marginBottom: '24px' }}>
        <Col><Statistic title="Total Cost" prefix="$" value={total_cost.toFixed(2)} /></Col>
        <Col><Statistic title="Run Duration" value={end_time ? formatDistanceStrict(new Date(end_time), new Date(start_time)) : 'N/A'} /></Col>
        <Col><Statistic title="Keywords Found" value={total_unique_count} /></Col>
        <Col><Statistic title="Added to Pipeline" value={final_added_to_db} valueStyle={{ color: '#3f8600' }} /></Col>
      </Row>

      {/* Processing Funnel */}
      <Card title="Processing Funnel" style={{ marginBottom: '24px' }}>
        <Steps current={5} size="small">
          <Step title="Total Found" description={`${total_raw_count.toLocaleString()}`} />
          <Step title="Unique" description={`${total_unique_count.toLocaleString()}`} />
          <Step title="Qualified" description={`${final_qualified_count.toLocaleString()}`} />
          <Step title="Duplicates Removed" description={`${duplicates_removed.toLocaleString()}`} />
          <Step title="Added to DB" description={<Text strong style={{color: '#3f8600'}}>{final_added_to_db.toLocaleString()}</Text>} />
        </Steps>
      </Card>

      <Row gutter={[24, 24]}>
        {/* Parameters */}
        <Col xs={24} lg={8}>
          <Card title="Run Parameters">
            <Descriptions bordered column={1} size="small">
              <Descriptions.Item label="Seed Keywords">
                {(parameters.seed_keywords || []).map(kw => <Tag key={kw}>{kw}</Tag>)}
              </Descriptions.Item>
              <Descriptions.Item label="Discovery Modes">
                {(parameters.discovery_modes || []).map(mode => <Tag key={mode} color="blue">{mode.replace(/_/g, ' ')}</Tag>)}
              </Descriptions.Item>
              <Descriptions.Item label="Max Keywords per Source">{parameters.limit || 'Default'}</Descriptions.Item>
              <Descriptions.Item label="Related Keywords Depth">{parameters.depth || 'Default'}</Descriptions.Item>
              <Descriptions.Item label="Use Exact Match (Suggestions)">
                {parameters.exact_match ? 'Enabled' : 'Disabled'}
              </Descriptions.Item>
              <Descriptions.Item label="Ignore Synonyms">
                {parameters.ignore_synonyms ? 'Enabled' : 'Disabled'}
              </Descriptions.Item>
              <Descriptions.Item label="Closely Variants">
                {parameters.closely_variants ? 'Enabled' : 'Disabled'}
              </Descriptions.Item>
              <Descriptions.Item label="Include Clickstream Data">
                {parameters.include_clickstream_data ? 'Enabled' : 'Disabled'}
              </Descriptions.Item>
              {Object.entries(parameters.filters_override || {}).map(([key, value]) => (
                <Descriptions.Item key={key} label={key.replace(/_/g, ' ')}>{String(value)}</Descriptions.Item>
              ))}
            </Descriptions>
          </Card>
        </Col>

        {/* Visualizations */}
        <Col xs={24} lg={16}>
          <Row gutter={[24, 24]}>
            <Col xs={24} md={12}>
              <PieChartCard title="Keyword Sources" data={source_counts} />
            </Col>
            <Col xs={24} md={12}>
              <PieChartCard title="Disqualification Reasons" data={disqualification_reasons} />
            </Col>
          </Row>
        </Col>
      </Row>
    </Modal>
  );
};

export default RunDetailsModal;