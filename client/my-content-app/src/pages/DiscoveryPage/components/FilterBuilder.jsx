import React, { useState, useEffect } from 'react';
import { Select, Button, InputNumber, Row, Col, Typography } from 'antd';
import { PlusOutlined, DeleteOutlined } from '@ant-design/icons';

const { Option } = Select;
const { Text } = Typography;

const SERP_FEATURES = [
    "answer_box", "app", "carousel", "multi_carousel", "featured_snippet", "google_flights",
    "google_reviews", "third_party_reviews", "google_posts", "images", "jobs", "knowledge_graph",
    "local_pack", "hotels_pack", "map", "organic", "paid", "people_also_ask", "related_searches",
    "people_also_search", "shopping", "top_stories", "twitter", "video", "events", "mention_carousel",
    "recipes", "top_sights", "scholarly_articles", "popular_products", "podcasts", "questions_and_answers",
    "find_results_on", "stocks_box", "visual_stories", "commercial_units", "local_services",
    "google_hotels", "math_solver", "currency_box", "product_considerations", "found_on_web",
    "short_videos", "refine_products", "explore_brands", "perspectives", "discussions_and_forums",
    "compare_sites", "courses", "ai_overview"
];

const AVAILABLE_FILTERS = [
    { name: 'keyword_info.search_volume', label: 'Search Volume', type: 'number', operators: ['>', '<', '=', '>=', '<='] },
    { name: 'keyword_properties.keyword_difficulty', label: 'Keyword Difficulty', type: 'number', operators: ['<', '<=', '>', '>='] },
    { name: 'keyword_info.cpc', label: 'Cost Per Click (CPC)', type: 'number', operators: ['>', '<', '=', '>=', '<='] },
    { name: 'keyword_info.competition_level', label: 'Competition Level', type: 'select', operators: ['in', 'not_in'], options: ['LOW', 'MEDIUM', 'HIGH'] },
    { name: 'search_intent_info.main_intent', label: 'Search Intent', type: 'select', operators: ['in', 'not_in'], options: ['informational', 'commercial', 'transactional', 'navigational'] },
];

const FilterBuilder = ({ onChange }) => {
  const [filters, setFilters] = useState([]);
  const [requiredSerpFeatures, setRequiredSerpFeatures] = useState([]);
  const [excludedSerpFeatures, setExcludedSerpFeatures] = useState([]);

  useEffect(() => {
    onChange({
      standardFilters: filters.filter(f => f.field && f.operator && f.value !== null),
      serpFilters: {
        required: requiredSerpFeatures,
        excluded: excludedSerpFeatures,
      },
    });
  }, [filters, requiredSerpFeatures, excludedSerpFeatures]);

  const handleFilterChange = (index, field, value) => {
    const newFilters = [...filters];
    newFilters[index][field] = value;

    if (field === 'field') {
      newFilters[index]['operator'] = null;
      newFilters[index]['value'] = null;
    }
    setFilters(newFilters);
  };

  const addFilter = () => {
    setFilters([...filters, { field: null, operator: null, value: null }]);
  };

  const removeFilter = (index) => {
    setFilters(filters.filter((_, i) => i !== index));
  };

  const getOperatorsForField = (fieldName) => {
    const field = AVAILABLE_FILTERS.find(f => f.name === fieldName);
    return field ? field.operators : [];
  };

  const getInputForField = (fieldName, index) => {
    const field = AVAILABLE_FILTERS.find(f => f.name === fieldName);
    if (!field) return null;

    switch (field.type) {
      case 'number':
        return <InputNumber value={filters[index].value} onChange={(val) => handleFilterChange(index, 'value', val)} />;
      case 'select':
        return (
          <Select
            style={{ width: 120 }}
            value={filters[index].value}
            onChange={(val) => handleFilterChange(index, 'value', val)}
            mode={field.operators.includes('in') || field.operators.includes('not_in') ? 'multiple' : 'default'}
            allowClear
          >
            {field.options.map(opt => <Option key={opt} value={opt}>{opt}</Option>)}
          </Select>
        );
      default:
        return null;
    }
  };

  return (
    <div>
      <Text strong>Standard Filters</Text>
      {filters.map((filter, index) => (
        <Row key={index} gutter={8} style={{ marginBottom: 8, marginTop: 8 }}>
          <Col>
            <Select
              style={{ width: 200 }}
              placeholder="Select field"
              value={filter.field}
              onChange={(val) => handleFilterChange(index, 'field', val)}
            >
              {AVAILABLE_FILTERS.map(f => <Option key={f.name} value={f.name}>{f.label}</Option>)}
            </Select>
          </Col>
          <Col>
            <Select
              style={{ width: 100 }}
              placeholder="Operator"
              value={filter.operator}
              onChange={(val) => handleFilterChange(index, 'operator', val)}
              disabled={!filter.field}
            >
              {getOperatorsForField(filter.field).map(op => <Option key={op} value={op}>{op}</Option>)}
            </Select>
          </Col>
          <Col>
            {getInputForField(filter.field, index)}
          </Col>
          <Col>
            <Button icon={<DeleteOutlined />} onClick={() => removeFilter(index)} danger />
          </Col>
        </Row>
      ))}
      <Button type="dashed" onClick={addFilter} icon={<PlusOutlined />} disabled={filters.length >= 8}>
        Add Filter ({filters.length}/8)
      </Button>

      <Row gutter={16} style={{ marginTop: 24 }}>
        <Col span={12}>
          <Text strong>SERP Features to Include</Text>
          <Select
            mode="multiple"
            allowClear
            style={{ width: '100%', marginTop: 8 }}
            placeholder="e.g., featured_snippet"
            onChange={setRequiredSerpFeatures}
            value={requiredSerpFeatures}
          >
            {SERP_FEATURES.map(feature => <Option key={feature} value={feature}>{feature}</Option>)}
          </Select>
        </Col>
        <Col span={12}>
          <Text strong>SERP Features to Exclude</Text>
          <Select
            mode="multiple"
            allowClear
            style={{ width: '100%', marginTop: 8 }}
            placeholder="e.g., local_pack"
            onChange={setExcludedSerpFeatures}
            value={excludedSerpFeatures}
          >
            {SERP_FEATURES.map(feature => <Option key={feature} value={feature}>{feature}</Option>)}
          </Select>
        </Col>
      </Row>
    </div>
  );
};

export default FilterBuilder;
