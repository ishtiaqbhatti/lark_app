// This is a new file. Create it with the following content:
import React from 'react';
import { Form, Input, InputNumber, Select, Switch, Slider, Typography, Row, Col, Divider, Tooltip, Alert, Space } from 'antd';
import { InfoCircleOutlined } from '@ant-design/icons';
import PromptTemplateEditor from '../../../components/PromptTemplateEditor'; // NEW

const { Title, Text } = Typography;
const { Option } = Select;

const AiContentSettingsTab = ({ settings, form }) => {
  const contentModel = Form.useWatch('ai_content_model', form); // Watch for changes in the AI content model

  return (
    <>
      <Title level={5}>AI Model & Generation</Title>
      <Row gutter={16}>
        <Col span={12}>
          <Form.Item name="ai_content_model" label="AI Content Generation Model">
            <Select style={{ width: '100%' }}>
              <Option value="gpt-4o">GPT-4o (Recommended)</Option>
              <Option value="gpt-4-turbo">GPT-4 Turbo</Option>
              <Option value="gpt-3.5-turbo">GPT-3.5 Turbo (Cost-Effective)</Option>
            </Select>
          </Form.Item>
          {contentModel === 'gpt-3.5-turbo' && (
            <Alert
              message="Cost-Effective Model Selected"
              description="GPT-3.5 Turbo is cheaper but may require more prompt engineering for quality."
              type="info"
              showIcon
              style={{ marginBottom: '16px' }}
            />
          )}
        </Col>
        <Col span={12}>
          <Form.Item name="ai_generation_temperature" label="AI Creativity (Temperature)">
            <Slider min={0.0} max={1.0} step={0.01} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="expert_persona" label="AI Writer Persona">
            <Input placeholder="e.g., a certified financial planner with 15 years of experience" />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="recommended_word_count_multiplier" label="Word Count Multiplier">
            <InputNumber min={0.5} max={3.0} step={0.1} style={{ width: '100%' }} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="max_completion_tokens_for_generation" label="Max Output Tokens">
            <InputNumber min={1000} max={32000} step={1000} style={{ width: '100%' }} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="max_words_for_ai_analysis" label="Max Words for AI Analysis">
            <InputNumber min={500} max={5000} step={100} style={{ width: '100%' }} />
          </Form.Item>
        </Col>
      </Row>

      <Divider />

      <Title level={5}>Image Generation</Title>
      <Row gutter={16}>
        <Col span={12}>
          <Form.Item name="use_pexels_first" label="Use Pexels for Images" valuePropName="checked">
            <Switch checkedChildren="Enabled" unCheckedChildren="Disabled" />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="num_in_article_images" label="Number of In-Article Images">
            <InputNumber min={0} max={5} style={{ width: '100%' }} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="overlay_text_enabled" label="Add Text Overlay to Images" valuePropName="checked">
            <Switch checkedChildren="Enabled" unCheckedChildren="Disabled" />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="overlay_text_color" label="Overlay Text Color">
            <Input type="color" style={{ width: '100%' }} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="overlay_background_color" label="Overlay Background Color">
            <Input type="color" style={{ width: '100%' }} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="overlay_font_size" label="Overlay Font Size">
            <InputNumber min={10} max={60} style={{ width: '100%' }} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="overlay_position" label="Overlay Position">
            <Select style={{ width: '100%' }}>
              <Option value="top_left">Top Left</Option>
              <Option value="top_center">Top Center</Option>
              <Option value="top_right">Top Right</Option>
              <Option value="bottom_left">Bottom Left</Option>
              <Option value="bottom_center">Bottom Center</Option>
              <Option value="bottom_right">Bottom Right</Option>
              <Option value="center">Center</Option>
            </Select>
          </Form.Item>
        </Col>
      </Row>

      <Divider />

      <Title level={5}>Custom AI Prompt Template</Title>
      <Form.Item 
        name="custom_prompt_template" 
        label={
          <Space>
            Edit your base prompt for the AI content generator.
            <Tooltip title="This template guides the AI's writing. Use available placeholders for dynamic data.">
              <InfoCircleOutlined />
            </Tooltip>
          </Space>
        }
        style={{ marginBottom: 0 }}
      >
        <PromptTemplateEditor disabled={false} />
      </Form.Item>
    </>
  );
};

export default AiContentSettingsTab;