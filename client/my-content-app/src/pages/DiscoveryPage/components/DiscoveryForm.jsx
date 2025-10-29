import React, { useState, useEffect } from 'react';
import { Input, Button, Typography, Form, Row, Col, InputNumber, Select, Switch, Modal } from 'antd';
import { RocketOutlined } from '@ant-design/icons';
import { useDiscoveryFilters } from '../hooks/useDiscoveryFilters';
import { useClient } from '../../../hooks/useClient';
import { preCheckKeywords } from '../../../services/discoveryService';
import FilterBuilder from './FilterBuilder';

const { Title } = Typography;
const { Option } = Select;

const goalPresets = [
  {
    key: 'optimal_easy_rank',
    label: '🎯 Optimal: Easy to Rank + Good Traffic',
    description: 'Scientifically optimized for blog content. Balances traffic potential with ranking feasibility using 8 proven filters.',
    filters: [
      { field: 'keyword_info.search_volume', operator: '>=', value: 500 },
      { field: 'keyword_info.search_volume', operator: '<=', value: 50000 },
      { field: 'keyword_properties.keyword_difficulty', operator: '<=', value: 40 },
      { field: 'keyword_info.competition_level', operator: 'in', value: ['LOW', 'MEDIUM'] },
      { field: 'search_intent_info.main_intent', operator: '=', value: 'informational' },
      { field: 'avg_backlinks_info.backlinks', operator: '<=', value: 100 },
      { field: 'avg_backlinks_info.referring_domains', operator: '<=', value: 50 },
      { field: 'keyword_info.cpc', operator: '>=', value: 0.30 },
    ],
  },
  {
    key: 'quick_wins',
    label: '🍎 Quick Wins (Ultra Easy)',
    description: 'Very low competition keywords you can rank for quickly.',
    filters: [
      { field: 'keyword_properties.keyword_difficulty', operator: '<=', value: 20 },
      { field: 'keyword_info.search_volume', operator: '>=', value: 200 },
      { field: 'keyword_info.competition_level', operator: '=', value: 'LOW' },
      { field: 'search_intent_info.main_intent', operator: 'in', value: ['informational', 'commercial'] },
      { field: 'keyword_info.cpc', operator: '>=', value: 0.10 },
    ],
  },
  {
    key: 'high_traffic',
    label: '📈 High-Volume Content',
    description: 'Target high search volume informational keywords.',
    filters: [
      { field: 'keyword_info.search_volume', operator: '>=', value: 2000 },
      { field: 'search_intent_info.main_intent', operator: '=', value: 'informational' },
      { field: 'keyword_properties.keyword_difficulty', operator: '<=', value: 50 },
      { field: 'keyword_info.competition_level', operator: 'in', value: ['LOW', 'MEDIUM'] },
    ],
  },
  {
    key: 'commercial_value',
    label: '💰 High Commercial Value',
    description: 'Keywords with strong monetization potential.',
    filters: [
      { field: 'search_intent_info.main_intent', operator: 'in', value: ['commercial', 'transactional'] },
      { field: 'keyword_info.cpc', operator: '>=', value: 2.00 },
      { field: 'keyword_info.competition', operator: '>=', value: 0.6 },
      { field: 'keyword_properties.keyword_difficulty', operator: '<=', value: 60 },
      { field: 'keyword_info.search_volume', operator: '>=', value: 500 },
    ],
  },
  {
    key: 'niche_topics',
    label: '🎣 Underserved Niches',
    description: 'Low competition, specific topics with dedicated audiences.',
    filters: [
      { field: 'keyword_properties.keyword_difficulty', operator: '<=', value: 15 },
      { field: 'keyword_info.search_volume', operator: '>=', value: 50 },
      { field: 'keyword_info.search_volume', operator: '<=', value: 500 },
      { field: 'keyword_info.competition_level', operator: '=', value: 'LOW' },
    ],
  },
];


const DiscoveryForm = ({ isSubmitting, onSubmit }) => {
  const [form] = Form.useForm();
  const { filtersData, isLoading: isLoadingFilters } = useDiscoveryFilters();
  const [selectedDiscoveryModes, setSelectedDiscoveryModes] = useState([
    'keyword_ideas', 'keyword_suggestions', 'related_keywords'
  ]);
  const { clientId } = useClient();
  const [isValidating, setIsValidating] = useState(false);
  const [validationStatus, setValidationStatus] = useState('');
  const [validationMessage, setValidationMessage] = useState('');

  // ... existing validation logic ...

  // SHOW SKELETON WHEN LOADING:
  if (isLoadingFilters) {
    return (
      <Card>
        <Skeleton active paragraph={{ rows: 8 }} />
      </Card>
    );
  }

  return (
    <Form 
      form={form} 
      layout="vertical" 
      onFinish={onFinish} 
      onValuesChange={handleValuesChange}
      initialValues={{
        // ... existing initial values ...
      }}
    >
      {/* ... existing form fields ... */}

      <Row justify="end" align="middle" style={{ marginTop: '24px' }}>
        <Col>
          <Button 
            type="primary" 
            htmlType="submit" 
            icon={<RocketOutlined />} 
            loading={isSubmitting} 
            size="large" 
            disabled={isValidating || validationStatus === 'error'}
          >
            {isSubmitting ? 'Finding Opportunities...' : 'Find Opportunities'}
          </Button>
        </Col>
      </Row>
    </Form>
  );
};

export default DiscoveryForm;