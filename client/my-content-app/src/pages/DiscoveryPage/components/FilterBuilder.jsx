import React, { useState } from 'react';
import { Select, Button, InputNumber, Row, Col } from 'antd';
import { PlusOutlined, DeleteOutlined } from '@ant-design/icons';

const { Option } = Select;

const FilterBuilder = ({ availableFilters, onChange }) => {
  const [filters, setFilters] = useState([{ field: null, operator: null, value: null }]);

  const handleFilterChange = (index, field, value) => {
    const newFilters = [...filters];
    newFilters[index][field] = value;

    // Reset operator and value if field changes
    if (field === 'field') {
      newFilters[index]['operator'] = null;
      newFilters[index]['value'] = null;
    }

    setFilters(newFilters);
    onChange(newFilters);
  };

  const addFilter = () => {
    const newFilters = [...filters, { field: null, operator: null, value: null }];
    setFilters(newFilters);
    onChange(newFilters);
  };

  const removeFilter = (index) => {
    const newFilters = filters.filter((_, i) => i !== index);
    setFilters(newFilters);
    onChange(newFilters);
  };

  const getOperatorsForField = (fieldName) => {
    const modeFilters = availableFilters?.filtersData?.modes.find(m => m.id === 'keyword_ideas')?.filters;
    const field = modeFilters?.find(f => f.name === fieldName);
    return field ? field.operators : [];
  };

  const getInputForField = (fieldName, index) => {
    const modeFilters = availableFilters?.filtersData?.modes.find(m => m.id === 'keyword_ideas')?.filters;
    const field = modeFilters?.find(f => f.name === fieldName);
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
      {filters.map((filter, index) => (
        <Row key={index} gutter={8} style={{ marginBottom: 8 }}>
          <Col>
            <Select
              style={{ width: 200 }}
              placeholder="Select field"
              value={filter.field}
              onChange={(val) => handleFilterChange(index, 'field', val)}
            >
              {availableFilters?.filters.map(f => <Option key={f.name} value={f.name}>{f.label}</Option>)}
            </Select>
          </Col>
          <Col>
            <Select
              style={{ width: 80 }}
              placeholder="Op"
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
    </div>
  );
};

export default FilterBuilder;
