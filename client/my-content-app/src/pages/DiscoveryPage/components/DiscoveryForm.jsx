import React from 'react';
import { Input, Button, Typography, Form, Row, Col, InputNumber, Select, Card, Tooltip, Divider } from 'antd';
import { RocketOutlined, QuestionCircleOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;
const { Option } = Select;

const DiscoveryForm = ({ isSubmitting, onSubmit }) => {
  const [form] = Form.useForm();

  const onFinish = (values) => {
    const { keyword, search_volume_value, difficulty_value, competition_level, search_intent } = values;

    const filters = [];
    const filterPathPrefix = 'keyword_data.';
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
      filters: filters.length > 0 ? filters : null,
    };
    
    onSubmit({ runData });
  };

  return (
    <Form form={form} layout="vertical" onFinish={onFinish} initialValues={{
      search_volume_value: 500,
      difficulty_value: 20,
      competition_level: ['LOW'],
      search_intent: ['informational'],
    }}>
      <Title level={3}>Start a New Discovery Run</Title>
      <Text type="secondary" style={{ marginBottom: '24px', display: 'block' }}>
        Enter a broad topic or a specific keyword to begin exploring related content opportunities.
      </Text>

      <Form.Item 
        name="keyword" 
        rules={[{ required: true, message: 'Please enter a seed keyword.' }]}
        label={<Title level={4}>Seed Keyword</Title>}
      >
        <Input placeholder="e.g., 'AI in marketing' or 'how to start a blog'" size="large" />
      </Form.Item>
      
      <Divider orientation="left" style={{ color: 'rgba(0,0,0,.55)', fontSize: '16px', marginTop: '32px' }}>
        Fine-tune with Filters (Optional)
      </Divider>
        <Row gutter={24}>
          <Col xs={24} sm={12}>
            <Form.Item 
              name="search_volume_value" 
              label={
                <span>
                  Monthly Search Volume (Greater than) 
                  <Tooltip title="Only find keywords with at least this many monthly searches.">
                    <QuestionCircleOutlined style={{ marginLeft: 4, color: 'rgba(0,0,0,.45)' }} />
                  </Tooltip>
                </span>
              }
            >
              <InputNumber style={{ width: '100%' }} placeholder="e.g., 500" />
            </Form.Item>
          </Col>
          <Col xs={24} sm={12}>
            <Form.Item 
              name="difficulty_value" 
              label={
                <span>
                  SEO Difficulty (Less than) 
                  <Tooltip title="Only find keywords with a difficulty score below this value (0-100).">
                    <QuestionCircleOutlined style={{ marginLeft: 4, color: 'rgba(0,0,0,.45)' }} />
                  </Tooltip>
                </span>
              }
            >
              <InputNumber style={{ width: '100%' }} placeholder="e.g., 20" min={0} max={100} />
            </Form.Item>
          </Col>
          <Col xs={24} sm={12}>
            <Form.Item 
              name="competition_level" 
              label={
                <span>
                  Competition Level 
                  <Tooltip title="Filter by the level of competition for paid ads.">
                    <QuestionCircleOutlined style={{ marginLeft: 4, color: 'rgba(0,0,0,.45)' }} />
                  </Tooltip>
                </span>
              }
            >
              <Select mode="multiple" placeholder="Any" allowClear>
                <Option value="LOW">Low</Option>
                <Option value="MEDIUM">Medium</Option>
                <Option value="HIGH">High</Option>
              </Select>
            </Form.Item>
          </Col>
          <Col xs={24} sm={12}>
            <Form.Item 
              name="search_intent" 
              label={
                <span>
                  Search Intent 
                  <Tooltip title="Filter for keywords based on the user's goal (e.g., to learn, to buy).">
                    <QuestionCircleOutlined style={{ marginLeft: 4, color: 'rgba(0,0,0,.45)' }} />
                  </Tooltip>
                </span>
              }
            >
              <Select mode="multiple" placeholder="Any" allowClear>
                <Option value="informational">Informational</Option>
                <Option value="commercial">Commercial</Option>
                <Option value="transactional">Transactional</Option>
                <Option value="navigational">Navigational</Option>
              </Select>
            </Form.Item>
          </Col>
        </Row>

      <Form.Item style={{ marginTop: '32px', marginBottom: 0 }}>
        <Button type="primary" htmlType="submit" icon={<RocketOutlined />} loading={isSubmitting} size="large" block>
          Find Opportunities
        </Button>
      </Form.Item>
    </Form>
  );
};

export default DiscoveryForm;