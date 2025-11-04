// This is a new file. Create it with the following content:
import React from 'react';
import { Form, Input, InputNumber, Select, Switch, Checkbox, Slider, Typography, Row, Col, Divider, Tooltip, Space } from 'antd';
import { InfoCircleOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;
const { Option } = Select;

const DiscoverySettingsTab = ({ settings, form }) => {
  return (
    <>
      <Title level={5}>General Discovery Parameters</Title>
      <Row gutter={16}>
        <Col span={12}>
          <Form.Item name="min_search_volume" label="Minimum Search Volume">
            <InputNumber min={0} max={100000} step={10} style={{ width: '100%' }} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="max_keyword_difficulty" label="Maximum Keyword Difficulty">
            <InputNumber min={0} max={100} style={{ width: '100%' }} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="min_keyword_word_count" label="Minimum Keyword Word Count">
            <InputNumber min={1} max={20} style={{ width: '100%' }} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="max_keyword_word_count" label="Maximum Keyword Word Count">
            <InputNumber min={1} max={20} style={{ width: '100%' }} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="discovery_max_pages" label="Max API Pages to Fetch">
            <InputNumber min={1} max={100} style={{ width: '100%' }} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="discovery_related_depth" label="Related Keywords Depth">
            <Slider min={0} max={4} />
          </Form.Item>
        </Col>
        <Col span={24}>
          <Form.Item name="discovery_strategies" label="Discovery Strategies">
            <Checkbox.Group
              options={[
                { label: 'Keyword Ideas (Category-based)', value: 'Keyword Ideas' },
                { label: 'Keyword Suggestions (Phrase-based)', value: 'Keyword Suggestions' },
                { label: 'Related Keywords (SERP-based)', value: 'Related Keywords' },
              ]}
            />
          </Form.Item>
        </Col>
      </Row>

      <Divider />

      <Title level={5}>Advanced Filtering & Ordering (Global Overrides)</Title>
      <Row gutter={16}>
        <Col span={12}>
          <Form.Item name="closely_variants" label="Search Mode (Keyword Ideas)" valuePropName="checked" tooltip="If enabled, 'Keyword Ideas' uses phrase-match. If disabled, it uses broad-match. Goal presets may override.">
            <Switch checkedChildren="Phrase Match" unCheckedChildren="Broad Match" />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="discovery_ignore_synonyms" label="Ignore Synonyms" valuePropName="checked" tooltip="If enabled, highly similar keywords will be excluded. Goal presets may override.">
            <Switch />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="discovery_exact_match" label="Exact Match (Keyword Suggestions)" valuePropName="checked" tooltip="If enabled, 'Keyword Suggestions' will only return keywords with the exact seed phrase. Goal presets may override.">
            <Switch />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="include_clickstream_data" label="Include Clickstream Data (Doubles Cost)" valuePropName="checked" tooltip="If enabled, clickstream-based metrics will be included, doubling API cost for discovery requests.">
            <Switch checkedChildren="Enabled" unCheckedChildren="Disabled" />
          </Form.Item>
        </Col>
        {/* REMOVED: The following filter fields are now part of Goal Presets and should not be directly editable as global defaults here */}
        {/*
        <Col span={12}>
          <Form.Item name="min_cpc_filter" label="Minimum CPC ($)">
            <InputNumber min={0.0} step={0.1} style={{ width: '100%' }} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="max_cpc_filter" label="Maximum CPC ($)">
            <InputNumber min={0.0} step={0.1} style={{ width: '100%' }} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="min_competition" label="Minimum Competition (0-1)">
            <InputNumber min={0.0} max={1.0} step={0.01} style={{ width: '100%' }} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="max_competition" label="Maximum Competition (0-1)">
            <InputNumber min={0.0} max={1.0} step={0.01} style={{ width: '100%' }} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="max_competition_level" label="Max Competition Level">
            <Select style={{ width: '100%' }}>
              <Option value="LOW">LOW</Option>
              <Option value="MEDIUM">MEDIUM</Option>
              <Option value="HIGH">HIGH</Option>
            </Select>
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="discovery_order_by_field" label="Order Results By">
            <Select style={{ width: '100%' }}>
              <Option value="keyword_info.search_volume">Search Volume</Option>
              <Option value="keyword_properties.keyword_difficulty">Keyword Difficulty</Option>
              <Option value="keyword_info.cpc">CPC</Option>
              <Option value="keyword_info.competition">Competition</Option>
            </Select>
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="discovery_order_by_direction" label="Order Direction">
            <Select style={{ width: '100%' }}>
              <Option value="desc">Descending</Option>
              <Option value="asc">Ascending</Option>
            </Select>
          </Form.Item>
        </Col>
        <Col span={24}>
          <Form.Item
            name="search_phrase_regex"
            label={
              <Space>
                Keyword Regex Filter
                <Tooltip title="Use regular expressions to filter keywords (e.g., ^how to.*$)">
                  <InfoCircleOutlined />
                </Tooltip>
              </Space>
            }
          >
            <Input placeholder="e.g., ^best.*reviews$" />
          </Form.Item>
        </Col>
        */}
      </Row>

      <Divider />

      <Title level={5}>Intent & Qualification</Title>
      <Row gutter={16}>
        <Col span={12}>
          <Form.Item name="enforce_intent_filter" label="Enforce Intent Filter" valuePropName="checked">
            <Switch />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="allowed_intents" label="Allowed Intents">
            <Select mode="multiple" style={{ width: '100%' }}>
              <Option value="informational">Informational</Option>
              <Option value="commercial">Commercial</Option>
              <Option value="transactional">Transactional</Option>
              <Option value="navigational">Navigational</Option>
            </Select>
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="prohibited_intents" label="Prohibited Secondary Intents">
            <Select mode="multiple" style={{ width: '100%' }}>
              <Option value="informational">Informational</Option>
              <Option value="commercial">Commercial</Option>
              <Option value="transactional">Transactional</Option>
              <Option value="navigational">Navigational</Option>
            </Select>
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="require_question_keywords" label="Require Question Keywords" valuePropName="checked">
            <Switch />
          </Form.Item>
        </Col>
        <Col span={24}>
          <Form.Item name="negative_keywords" label="Negative Keywords" extra="Comma-separated list of keywords to exclude (e.g., free, login)">
            <Input.TextArea rows={2} />
          </Form.Item>
        </Col>
      </Row>

      <Divider /><br/>
      <Title level={5}>SERP & Competitor Analysis Cost Controls</Title><br/>
      <Row gutter={16}><br/>
        <Col span={12}><br/>
          <Form.Item name="load_async_ai_overview" label="Load Async AI Overview" valuePropName="checked" tooltip="Set to true to obtain AI Overview items in SERPs even if they are loaded asynchronously. Costs $0.002 extra per SERP call."><br/>
            <Switch checkedChildren="Enabled" unCheckedChildren="Disabled" /><br/>
          </Form.Item><br/>
        </Col><br/>
        <Col span={12}><br/>
          <Form.Item name="people_also_ask_click_depth" label="PAA Click Depth"><br/>
            <InputNumber min={0} max={4} style={{ width: '100%' }} tooltip="Specify the depth of clicks (1 to 4) on People Also Ask elements. Costs $0.00015 extra per click per level." /><br/>
          </Form.Item><br/>
        </Col><br/>
        <Col span={12}><br/>
          <Form.Item name="onpage_enable_browser_rendering" label="Enable Browser Rendering (High Cost)" valuePropName="checked" tooltip="If true, emulates a full browser load for Core Web Vitals (LCP/CLS) and loads JavaScript/Resources automatically. Primary cost factor for Analysis."><br/>
            <Switch checkedChildren="Enabled" unCheckedChildren="Disabled" /><br/>
          </Form.Item><br/>
        </Col><br/>
        <Col span={12}><br/>
          <Form.Item name="onpage_enable_custom_js" label="Enable Custom JavaScript" valuePropName="checked" tooltip="Allows execution of custom JavaScript during OnPage crawl. Costs $0.00025 extra per page analyzed."><br/>
            <Switch checkedChildren="Enabled" unCheckedChildren="Disabled" /><br/>
          </Form.Item><br/>
        </Col><br/>
      </Row><br/><br/>
    </>
  );
};

export default DiscoverySettingsTab;