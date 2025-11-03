import React, { useState } from 'react';
import {
  Input,
  Button,
  Typography,
  Form,
  Row,
  Col,
  InputNumber,
  Select,
  Tooltip,
  Divider,
  Slider,
  Checkbox,
  Collapse,
} from 'antd';
import { RocketOutlined, QuestionCircleOutlined, SettingOutlined } from '@ant-design/icons';
import FilterBuilder from './FilterBuilder';

const { Title, Text } = Typography;
const { Option } = Select;
const { Panel } = Collapse;

const DiscoveryForm = ({ isSubmitting, onSubmit }) => {
  const [form] = Form.useForm();
  const [filters, setFilters] = useState({ standardFilters: [], serpFilters: {} });

  const onFinish = (values) => {
    const {
      seed_keywords,
      discovery_engines,
      pages_to_fetch,
      related_keywords_depth,
      search_volume_range,
      keyword_difficulty_range,
    } = values;

    let runData = {
      seed_keywords,
      discovery_modes: discovery_engines || ['keyword_ideas', 'keyword_suggestions', 'related_keywords'],
      limit: 1000,
      pages_to_fetch: pages_to_fetch || 1,
      related_keywords_depth: related_keywords_depth || 1,
    };

    const standardFilters = [...filters.standardFilters];

    if (search_volume_range) {
      standardFilters.push({ field: 'keyword_info.search_volume', operator: '>=', value: search_volume_range[0] });
      standardFilters.push({ field: 'keyword_info.search_volume', operator: '<=', value: search_volume_range[1] });
    }
    if (keyword_difficulty_range) {
      standardFilters.push({ field: 'keyword_properties.keyword_difficulty', operator: '>=', value: keyword_difficulty_range[0] });
      standardFilters.push({ field: 'keyword_properties.keyword_difficulty', operator: '<=', value: keyword_difficulty_range[1] });
    }

    runData.filters = standardFilters.length > 0 ? standardFilters : null;
    runData.required_serp_features = filters.serpFilters.required;
    runData.excluded_serp_features = filters.serpFilters.excluded;

    onSubmit({ runData });
  };

  return (
    <Form
      form={form}
      layout="vertical"
      onFinish={onFinish}
      initialValues={{
        discovery_engines: ['keyword_ideas', 'keyword_suggestions', 'related_keywords'],
        pages_to_fetch: 1,
        related_keywords_depth: 1,
        search_volume_range: [100, 10000],
        keyword_difficulty_range: [0, 40],
      }}
    >
      <Title level={3}>Start a New Discovery Run</Title>
      <Text type="secondary" style={{ marginBottom: '24px', display: 'block' }}>
        Enter broad topics or specific keywords to begin exploring related content opportunities.
      </Text>

      <Divider orientation="left">Core Search</Divider>

      <Form.Item
        name="seed_keywords"
        rules={[{ required: true, message: 'Please enter at least one seed keyword.' }]}
        label={<Title level={5}>Seed Keywords</Title>}
      >
        <Select mode="tags" placeholder="e.g., 'AI in marketing', 'how to start a blog'" size="large" />
      </Form.Item>

      <Form.Item
        name="discovery_engines"
        label={<Title level={5}>Discovery Engines</Title>}
      >
        <Checkbox.Group>
          <Checkbox value="keyword_ideas">Broad Match</Checkbox>
          <Checkbox value="keyword_suggestions">Question Finder</Checkbox>
          <Checkbox value="related_keywords">Competitor Keywords</Checkbox>
        </Checkbox.Group>
      </Form.Item>

      <Divider orientation="left">Quick Filters</Divider>

      <Row gutter={24}>
        <Col xs={24} sm={12}>
          <Form.Item
            name="search_volume_range"
            label="Monthly Search Volume"
          >
            <Slider range defaultValue={[100, 10000]} max={50000} step={100} />
          </Form.Item>
        </Col>
        <Col xs={24} sm={12}>
          <Form.Item
            name="keyword_difficulty_range"
            label="SEO Difficulty"
          >
            <Slider range defaultValue={[0, 40]} max={100} />
          </Form.Item>
        </Col>
      </Row>

      <Divider orientation="left">Advanced Targeting</Divider>

      <FilterBuilder availableFilters={{ filters: [] }} onChange={setFilters} />

      <Collapse ghost style={{ marginTop: '24px' }}>
        <Panel header={<><SettingOutlined /> Advanced API Settings</>} key="1">
          <Row gutter={24}>
            <Col xs={24} sm={12}>
              <Form.Item
                name="pages_to_fetch"
                label={
                  <span>
                    Pages to Fetch
                    <Tooltip title="Number of pages of results to fetch from the API. More pages may increase costs.">
                      <QuestionCircleOutlined style={{ marginLeft: 4, color: 'rgba(0,0,0,.45)' }} />
                    </Tooltip>
                  </span>
                }
              >
                <InputNumber style={{ width: '100%' }} placeholder="e.g., 1" min={1} max={10} />
              </Form.Item>
            </Col>
            <Col xs={24} sm={12}>
              <Form.Item
                name="related_keywords_depth"
                label={
                  <span>
                    Related Keyword Depth
                    <Tooltip title="Depth for recursive search in Competitor Keywords. Higher values are more expensive.">
                      <QuestionCircleOutlined style={{ marginLeft: 4, color: 'rgba(0,0,0,.45)' }} />
                    </Tooltip>
                  </span>
                }
              >
                <InputNumber style={{ width: '100%' }} placeholder="e.g., 1" min={1} max={5} />
              </Form.Item>
            </Col>
          </Row>
        </Panel>
      </Collapse>

      <Form.Item style={{ marginTop: '32px', marginBottom: 0 }}>
        <Button type="primary" htmlType="submit" icon={<RocketOutlined />} loading={isSubmitting} size="large" block>
          Find Opportunities
        </Button>
      </Form.Item>
    </Form>
  );
};

export default DiscoveryForm;