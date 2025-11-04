import React from 'react';
import { Input, Button, Typography, Form, Row, Col, InputNumber, Select, Card, Tooltip, Divider, Collapse, Slider, Switch, Space } from 'antd';
import { RocketOutlined, QuestionCircleOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;
const { Option } = Select;
const { Panel } = Collapse;

const DiscoveryForm = ({ isSubmitting, onSubmit, settings, isLoadingSettings }) => {
  const [form] = Form.useForm();

  // Set initial values from settings once they are loaded
  React.useEffect(() => {
    if (settings) {
      form.setFieldsValue({
        limit: settings.discovery_max_pages || 100, // Default to 100 if not set in DB/config
        depth: settings.discovery_related_depth || 1, // Default to 1 if not set
        exact_match: settings.discovery_exact_match || false, // Default to false if not set
        // Add other initial values from settings here if needed
      });
    }
  }, [settings, form]);

  const onFinish = (values) => {
    const { seed_keywords, filters_simple, limit, depth, exact_match } = values;

    const runData = {
      seed_keywords: seed_keywords,
      filters: filters_simple || [], // Placeholder for eventual FilterBuilder integration
      limit: limit,
      depth: depth,
      exact_match: exact_match,
      // Add other advanced parameters here as they are added to the form
    };
    
    onSubmit({ runData });
  };

  return (
    <Form form={form} layout="vertical" onFinish={onFinish} initialValues={{
      // Default values before settings are loaded
      limit: 100,
      depth: 1,
      exact_match: false,
    }}>
      <Title level={3}>Start a New Discovery Run</Title>
      <Text type="secondary" style={{ marginBottom: '24px', display: 'block' }}>
        Enter one or more seed keywords to begin exploring related content opportunities.
      </Text>

      <Form.Item 
        name="seed_keywords" 
        rules={[{ required: true, message: 'Please enter at least one seed keyword.' }]}
        label={<Title level={4}>Seed Keywords</Title>}
      >
        <Select
          mode="tags"
          style={{ width: '100%' }}
          placeholder="Type a keyword and press Enter (e.g., 'AI in marketing')"
          size="large"
          tokenSeparators={[',']}
        />
      </Form.Item>
      
      <Collapse ghost>
        <Panel header="Advanced Run Settings" key="1">
            <Row gutter={24}>
              <Col xs={24} sm={12}>
                <Form.Item 
                  name="limit" 
                  label={
                    <Space>
                      Max Keywords per Source
                      <Tooltip title="Set the maximum number of keywords to fetch from each API source (max 1000). Higher values increase cost and discovery breadth.">
                        <QuestionCircleOutlined />
                      </Tooltip>
                    </Space>
                  }
                  rules={[{ required: true, message: 'Limit is required.'}, { type: 'number', min: 10, max: 1000, message: 'Limit must be between 10 and 1000.'}]}
                >
                  <InputNumber style={{ width: '100%' }} min={10} max={1000} step={50} />
                </Form.Item>
              </Col>
              <Col xs={24} sm={12}>
                <Form.Item 
                  name="depth" 
                  label={
                    <Space>
                      Related Keywords Depth
                      <Tooltip title="Set the discovery depth for the 'Related Keywords' API. A higher depth (max 4) finds exponentially more niche keywords but increases cost.">
                        <QuestionCircleOutlined />
                      </Tooltip>
                    </Space>
                  }
                  rules={[{ required: true, message: 'Depth is required.'}, { type: 'number', min: 1, max: 4, message: 'Depth must be between 1 and 4.'}]}
                >
                  <Slider min={1} max={4} marks={{ 1: 'Shallow', 2: 'Medium', 3: 'Deep', 4: 'Max' }} />
                </Form.Item>
              </Col>
              <Col xs={24} sm={12}>
                <Form.Item 
                  name="exact_match" 
                  label={
                    <Space>
                      Use Exact Match (for Suggestions)
                      <Tooltip title="If enabled, the 'Keyword Suggestions' API will only return phrases that contain your exact seed keyword. Disable for broader, semantic suggestions.">
                        <QuestionCircleOutlined />
                      </Tooltip>
                    </Space>
                  }
                  valuePropName="checked"
                >
                  <Switch />
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