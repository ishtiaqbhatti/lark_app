import React from 'react';
import { Select, Button, InputNumber, Row, Col, Alert } from 'antd';
import { PlusOutlined, DeleteOutlined } from '@ant-design/icons';

const { Option } = Select;

const FilterBuilder = ({ value = [], onChange, availableFilters }) => {
  const filters = value;
  const MAX_FILTERS = 8;

  const triggerChange = (newFilters) => {
    onChange?.(newFilters);
  };

  const handleFilterChange = (index, field, fieldValue) => {
    const newFilters = [...filters];
    newFilters[index] = { ...newFilters[index], [field]: fieldValue };

    // Reset operator and value if field changes
    if (field === 'field') {
      newFilters[index].operator = null;
      newFilters[index].value = null;
    }

    triggerChange(newFilters);
  };

  const addFilter = () => {
    if (filters.length >= MAX_FILTERS) {
      // DON'T ADD - already at max
      return;
    }
    const newFilters = [...filters, { field: null, operator: null, value: null }];
    triggerChange(newFilters);
  };

  const removeFilter = (index) => {
    const newFilters = filters.filter((_, i) => i !== index);
    triggerChange(newFilters);
  };

  const getOperatorsForField = (fieldName) => {
    const allFilters = availableFilters?.flatMap(mode => mode.filters) || [];
    const field = allFilters.find(f => f.name === fieldName);
    return field ? field.operators : [];
  };

  const getInputForField = (fieldName, index) => {
    const allFilters = availableFilters?.flatMap(mode => mode.filters) || [];
    const field = allFilters.find(f => f.name === fieldName);
    if (!field) return null;

    switch (field.type) {
      case 'number':
        return <InputNumber style={{ width: '100%' }} value={filters[index].value} onChange={(val) => handleFilterChange(index, 'value', val)} />;
      case 'select':
        return (
          <Select
            style={{ width: '100%' }}
            value={filters[index].value}
            onChange={(val) => handleFilterChange(index, 'value', val)}
          >
            {field.options.map(opt => <Option key={opt} value={opt}>{opt}</Option>)}
          </Select>
        );
      default:
        return null;
    }
  };

  const uniqueFilters = availableFilters ? [...new Map(availableFilters.flatMap(mode => mode.filters).map(item => [item.name, item])).values()] : [];

  return (
    <div>
      {filters.length >= MAX_FILTERS && (
        <Alert
          message="Maximum Filters Reached"
          description="You've reached the maximum of 8 filter conditions. Remove a filter to add a new one."
          type="warning"
          showIcon
          style={{ marginBottom: 16 }}
        />
      )}
      
      {filters.map((filter, index) => (
        <Row key={index} gutter={8} style={{ marginBottom: 8 }} align="middle">
          <Col span={10}>
            <Select
              style={{ width: '100%' }}
              placeholder="Select field"
              value={filter.field}
              onChange={(val) => handleFilterChange(index, 'field', val)}
            >
              {uniqueFilters.map(f => <Option key={f.name} value={f.name}>{f.label}</Option>)}
            </Select>
          </Col>
          <Col span={4}>
            <Select
              style={{ width: '100%' }}
              placeholder="Op"
              value={filter.operator}
              onChange={(val) => handleFilterChange(index, 'operator', val)}
              disabled={!filter.field}
            >
              {getOperatorsForField(filter.field).map(op => <Option key={op} value={op}>{op}</Option>)}
            </Select>
          </Col>
          <Col span={8}>
            {getInputForField(filter.field, index)}
          </Col>
          <Col span={2}>
            <Button icon={<DeleteOutlined />} onClick={() => removeFilter(index)} danger block />
          </Col>
        </Row>
      ))}
      
      <Button 
        type="dashed" 
        onClick={addFilter} 
        icon={<PlusOutlined />} 
        disabled={filters.length >= MAX_FILTERS}
        block
      >
        Add Filter ({filters.length}/{MAX_FILTERS})
      </Button>
    </div>
  );
};

export default FilterBuilder;
