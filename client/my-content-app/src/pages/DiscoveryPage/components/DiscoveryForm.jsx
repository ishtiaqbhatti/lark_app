import React, { useState, useEffect } from 'react';
import { Input, Button, Typography, Form, Row, Col, InputNumber, Select, Switch, Modal } from 'antd';
import { RocketOutlined } from '@ant-design/icons';
import { useDiscoveryFilters } from '../hooks/useDiscoveryFilters';
import { useClient } from '../../../hooks/useClient';
import { preCheckKeywords } from '../../../services/discoveryService';

const { Title } = Typography;
const { Option } = Select;

const DiscoveryForm = ({ isSubmitting, onSubmit }) => {
  const [form] = Form.useForm();
  const { filtersData, isLoading: isLoadingFilters } = useDiscoveryFilters();
  const [selectedDiscoveryModes, setSelectedDiscoveryModes] = useState(['keyword_ideas', 'keyword_suggestions', 'related_keywords']);
  const { clientId } = useClient();
  const [isValidating, setIsValidating] = useState(false);
  const [validationStatus, setValidationStatus] = useState('');
  const [validationMessage, setValidationMessage] = useState('');

  const keywordValue = Form.useWatch('keyword', form);

  useEffect(() => {
    if (filtersData && selectedDiscoveryModes.length > 0) {
      const firstModeWithDefaults = filtersData.find(mode => mode.id === selectedDiscoveryModes[0] && mode.defaults);
      if (firstModeWithDefaults) {
        const { filters } = firstModeWithDefaults.defaults;
        const searchVolumeFilter = filters.find(f => f.field.includes('search_volume'));
        const difficultyFilter = filters.find(f => f.field.includes('keyword_difficulty'));

        form.setFieldsValue({
          search_volume_value: searchVolumeFilter ? searchVolumeFilter.value : null,
          difficulty_value: difficultyFilter ? difficultyFilter.value : null,
        });
      }
    }
  }, [selectedDiscoveryModes, filtersData, form]);

  useEffect(() => {
    if (!keywordValue) {
      setValidationStatus('');
      setValidationMessage('');
      return;
    }

    setIsValidating(true);
    setValidationStatus('validating');
    const handler = setTimeout(() => {
      preCheckKeywords({ clientId, seed_keywords: [keywordValue] })
        .then(response => {
          if (response.existing_keywords.length > 0) {
            setValidationStatus('warning');
            setValidationMessage('This keyword has been processed before.');
          } else {
            setValidationStatus('success');
            setValidationMessage('');
          }
        })
        .catch(error => {
          setValidationStatus('error');
          setValidationMessage(error.response?.data?.detail || 'Error validating keyword.');
        })
        .finally(() => {
          setIsValidating(false);
        });
    }, 500);

    return () => {
      clearTimeout(handler);
    };
  }, [keywordValue, clientId]);

      const onFinish = (values) => {
        const currentFilters = form.getFieldValue('filters'); // Assuming 'filters' is the form item holding the filter array
        if (currentFilters && currentFilters.length > 8) {
            Modal.error({
                title: 'Too Many Filters',
                content: 'You can specify a maximum of 8 filter conditions. Please remove some filters.',
            });
            return;
        }
        const { keyword, negative_keywords, limit, search_volume_value, difficulty_value, competition_level, search_intent, closely_variants, ignore_synonyms, exact_match, discovery_modes, depth } = values;

// ADDITION: Read discovery mode and max pages from form values
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
          negative_keywords: negative_keywords ? negative_keywords.split(',').map(kw => kw.trim()) : [],
          limit: limit,
          filters: filters.length > 0 ? filters : null,
          closely_variants,
          ignore_synonyms,
          exact_match,
// ADD these fields to runData:
discovery_modes,
discovery_max_pages,
depth,
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
          discovery_modes: ['keyword_ideas', 'keyword_suggestions', 'related_keywords'],
          depth: 3,
          discovery_max_pages: 1,

  

        }}>

  

          <Title level={4}>1. Enter a Seed Keyword</Title>

  

          <Form.Item name="keyword" rules={[{ required: true, message: 'Please enter a seed keyword.' }]} hasFeedback validateStatus={validationStatus} help={validationMessage}>

  

            <Input placeholder="e.g., content marketing" />

  

          </Form.Item>

          <Form.Item name="negative_keywords" label="Negative Keywords (Optional)" tooltip="Comma-separated list of keywords to exclude from the results.">
            <Input placeholder="e.g., free, jobs, careers" />
          </Form.Item>

          <Form.Item name="discovery_modes" label="Discovery Modes" rules={[{ required: true, message: 'Please select at least one discovery mode.' }]}>
            <Select
              mode="multiple"
              placeholder="Select discovery modes"
              loading={isLoadingFilters}
              style={{ width: '100%' }}
              onChange={setSelectedDiscoveryModes}
            >
              {filtersData?.map(mode => (
                <Option key={mode.id} value={mode.id}>{mode.name}</Option>
              ))}
            </Select>
          </Form.Item>

          {selectedDiscoveryModes.includes('related_keywords') && (
            <Form.Item name="depth" label="Related Keywords Depth" tooltip="How many levels of related keywords to fetch. Higher values are more expensive.">
              <InputNumber min={1} max={5} style={{ width: '100%' }} />
            </Form.Item>
          )}

  

          

  

          <Title level={4}>2. Add Filters (Optional)</Title>

  

          <Row gutter={16}>

  

            <Col span={12}>

  

              <Form.Item name="limit" label="Limit (Number of keywords to find)">

  

                <InputNumber style={{ width: '100%' }} placeholder="e.g., 1000" />

  

              </Form.Item>

  

            </Col>

            <Col span={12}>
              <Form.Item name="discovery_max_pages" label="Max Pages" tooltip="How many pages of results to fetch from the API. Higher values are more expensive.">
                <InputNumber min={1} max={10} style={{ width: '100%' }} />
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

  

                                  <Col span={12}>

  

                                    <Form.Item name="closely_variants" label="Targeted Variations" valuePropName="checked" tooltip="For Keyword Ideas, this limits results to keywords that are close variants of the seed keyword. Not applicable to other modes.">

  

                                      <Switch />

  

                                    </Form.Item>

  

                                  </Col>

  

                                  <Col span={12}>

  

                                    <Form.Item name="exact_match" label="Precise Targeting" valuePropName="checked" tooltip="For Keyword Suggestions, this returns only keywords that exactly match the seed keyword's phrasing. Not applicable to other modes.">

  

                                      <Switch />

  

                                    </Form.Item>

  

                                  </Col>

  

                                  <Col span={12}>

  

                                    <Form.Item name="ignore_synonyms" label="Focus on Core Term" valuePropName="checked" tooltip="Returns only core keywords, excluding highly similar variations.">

  

                                      <Switch />

  

                                    </Form.Item>

  

                                  </Col>

  

                    </Row>

      <Row justify="end" align="middle" style={{ marginTop: '24px' }}>
        <Col>
          <Button type="primary" htmlType="submit" icon={<RocketOutlined />} loading={isSubmitting} size="large" disabled={isValidating || validationStatus === 'error'}>
            Find Opportunities
          </Button>
        </Col>
      </Row>
    </Form>
  );
};

export default DiscoveryForm;