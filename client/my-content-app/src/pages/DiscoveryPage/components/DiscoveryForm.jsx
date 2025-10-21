import React from 'react';
import { Input, Button, Typography, Form, Row, Col, InputNumber, Select, Switch, Modal } from 'antd';
import { RocketOutlined } from '@ant-design/icons';
import { useDiscoveryFilters } from '../hooks/useDiscoveryFilters';

const { Title } = Typography;
const { Option } = Select;

const DiscoveryForm = ({ isSubmitting, onSubmit }) => {
  const [form] = Form.useForm();
  useDiscoveryFilters();

      const onFinish = (values) => {
        const currentFilters = form.getFieldValue('filters'); // Assuming 'filters' is the form item holding the filter array
        if (currentFilters && currentFilters.length > 8) {
            Modal.error({
                title: 'Too Many Filters',
                content: 'You can specify a maximum of 8 filter conditions. Please remove some filters.',
            });
            return;
        }
        const { keyword, limit, search_volume_value, difficulty_value, competition_level, search_intent, include_clickstream_data, closely_variants, ignore_synonyms, exact_match } = values;

// ADDITION: Read discovery mode and max pages from form values
const discovery_modes = form.getFieldValue('discovery_modes') || ['ideas'];
const discovery_max_pages = form.getFieldValue('discovery_max_pages') || 1;

        // ... (rest of filtering logic) ...
        const filters = [];
        const filterPathPrefix = 'keyword_data.'; // Defaulting to a common prefix, backend will handle specifics
        if (search_volume_value !== undefined && search_volume_value !== null) {
          filters.push({ field: `${filterPathPrefix}keyword_info.search_volume`, operator: '>', value: search_volume_value });
        }
        if (difficulty_value !== undefined && difficulty_value !== null) {
          filters.push({ field: `${filterPathPrefix}keyword_properties.keyword_difficulty`, operator: '<', value: difficulty_value });
        }
        if (competition_level && competition_level.length > 0) {
          filters.push({ field: `${filterPathPrefix}keyword_info.competition_level`, operator: 'in', value: competition_level });
        }
        if (search_intent && search_intent.length > 0) {
          filters.push({ field: `${filterPathPrefix}search_intent_info.main_intent`, operator: 'in', value: search_intent });
        }

        const runData = {
          seed_keywords: [keyword],
          limit: limit,
          filters: filters.length > 0 ? filters : null,
          include_clickstream_data,
          closely_variants,
          ignore_synonyms,
          exact_match,
// ADD these fields to runData:
discovery_modes,
discovery_max_pages,
        };
        
        onSubmit({ runData });
      };

  

      return (

  

        <Form form={form} layout="vertical" onFinish={onFinish} initialValues={{

  

          limit: 1000,

  

          search_volume_value: 500,

  

          difficulty_value: 20,

  

          competition_level: ['LOW'],

  

          search_intent: ['informational'],

  

        }}>

  

          <Title level={4}>1. Enter a Seed Keyword</Title>

  

          <Form.Item name="keyword" rules={[{ required: true, message: 'Please enter a seed keyword.' }]}>

  

            <Input placeholder="e.g., content marketing" />

  

          </Form.Item>

  

          

  

          <Title level={4}>2. Add Filters (Optional)</Title>

  

          <Row gutter={16}>

  

            <Col span={12}>

  

              <Form.Item name="limit" label="Limit (Number of keywords to find)">

  

                <InputNumber style={{ width: '100%' }} placeholder="e.g., 1000" />

  

              </Form.Item>

  

            </Col>

  

            <Col span={12}>

  

              <Form.Item name="search_volume_value" label="Monthly Search Volume (Greater than)">

  

                <InputNumber style={{ width: '100%' }} placeholder="e.g., 500" />

  

              </Form.Item>

  

            </Col>

  

            <Col span={12}>

  

              <Form.Item name="difficulty_value" label="SEO Difficulty (Less than)">

  

                <InputNumber style={{ width: '100%' }} placeholder="e.g., 20" min={0} max={100} />

  

              </Form.Item>

  

            </Col>

  

            <Col span={12}>

  

              <Form.Item name="competition_level" label="Competition Level">

  

                <Select mode="multiple" placeholder="Any" allowClear>

  

                  <Option value="LOW">Low</Option>

  

                  <Option value="MEDIUM">Medium</Option>

  

                  <Option value="HIGH">High</Option>

  

                </Select>

  

              </Form.Item>

  

            </Col>

  

            <Col span={12}>

  

              <Form.Item name="search_intent" label="Search Intent">

  

                <Select mode="multiple" placeholder="Any" allowClear>

  

                  <Option value="informational">Informational</Option>

  

                  <Option value="commercial">Commercial</Option>

  

                  <Option value="transactional">Transactional</Option>

  

                  <Option value="navigational">Navigational</Option>

  

                </Select>

  

              </Form.Item>

  

            </Col>

  

          </Row>

          <Row gutter={16}>
            <Col span={24}>
              <Form.Item name="include_clickstream_data" label="Include Clickstream Demographics" valuePropName="checked" tooltip="Provides audience demographic data but doubles the API cost of the discovery run.">
                <Switch />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="closely_variants" label="Use Phrase Match" valuePropName="checked" tooltip="Limits results to keywords that are close variants of the seed keyword (more targeted).">
                <Switch />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="exact_match" label="Use Exact Match" valuePropName="checked" tooltip="Returns only keywords that exactly match the seed keyword's phrasing.">
                <Switch />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="ignore_synonyms" label="Ignore Synonyms" valuePropName="checked" tooltip="Returns only core keywords, excluding highly similar variations.">
                <Switch />
              </Form.Item>
            </Col>
          </Row>

      <Row justify="end" align="middle" style={{ marginTop: '24px' }}>
        <Col>
          <Button type="primary" htmlType="submit" icon={<RocketOutlined />} loading={isSubmitting} size="large">
            Find Opportunities
          </Button>
        </Col>
      </Row>
    </Form>
  );
};

export default DiscoveryForm;