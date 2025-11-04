import React, { useState, useEffect } from 'react'; // Add useEffect
import { Input, Button, Typography, Form, Row, Col, InputNumber, Select, Card, Tooltip, Divider, Spin } from 'antd'; // Add Spin
import { RocketOutlined, QuestionCircleOutlined } from '@ant-design/icons';
import { useQuery } from 'react-query'; // Add useQuery
import { getDiscoveryGoalsAndDefaults } from '../../../services/discoveryService'; // NEW: Import service

const { Title, Text } = Typography;
const { Option } = Select;

const DiscoveryForm = ({ isSubmitting, onSubmit }) => {
  const [form] = Form.useForm();
  const [selectedGoal, setSelectedGoal] = useState(null);

  const { data: goalsAndDefaults, isLoading: isLoadingGoals } = useQuery(
    'discoveryGoalsAndDefaults',
    getDiscoveryGoalsAndDefaults,
    {
      staleTime: Infinity,
      cacheTime: Infinity,
      onSuccess: (data) => {
        if (data && data.length > 0) {
          // Set initial goal and pre-fill form values
          const defaultGoal = data[0].name;
          setSelectedGoal(defaultGoal);
          form.setFieldsValue({
            discovery_goal: defaultGoal,
            min_search_volume: data[0].default_sv,
            max_keyword_difficulty: data[0].default_kd,
          });
        }
      }
    }
  );

  useEffect(() => {
    // When the selectedGoal changes, update the KD/SV defaults in the form
    if (selectedGoal && goalsAndDefaults) {
      const currentGoalPreset = goalsAndDefaults.find(goal => goal.name === selectedGoal);
      if (currentGoalPreset) {
        form.setFieldsValue({
          min_search_volume: currentGoalPreset.default_sv,
          max_keyword_difficulty: currentGoalPreset.default_kd,
        });
      }
    }
  }, [selectedGoal, goalsAndDefaults, form]);


  const onFinish = (values) => {
    const { keyword, discovery_goal, min_search_volume, max_keyword_difficulty } = values;

    const goalMap = {
      "Find Low-Hanging Fruit": "Low-Hanging Fruit",
      "Target High-Value Conversions": "High-Value Conversions",
      "Lead Thought Leadership & Authority Building": "Thought Leadership",
    };

    const runData = {
      seed_keywords: [keyword],
      discovery_goal: goalMap[discovery_goal] || discovery_goal,
      min_search_volume: min_search_volume,
      max_keyword_difficulty: max_keyword_difficulty,
    };
    
    onSubmit({ runData });
  };

  const handleGoalChange = (goalName) => {
    setSelectedGoal(goalName);
    // Defaults for KD/SV will be set by the useEffect hook
  };

  return (
    <Form form={form} layout="vertical" onFinish={onFinish} initialValues={{
      // Initial values will be set by useEffect after goals load
    }}>
      <Title level={3}>Start a New Discovery Run</Title>
      <Text type="secondary" style={{ marginBottom: '24px', display: 'block' }}>
        Select a strategic goal and enter a seed keyword to begin exploring related content opportunities.
      </Text>

      <Row gutter={24}>
        <Col xs={24} sm={12}>
          <Form.Item 
            name="discovery_goal"
            label={<Title level={4}>Discovery Goal</Title>}
            rules={[{ required: true, message: 'Please select a discovery goal.' }]}
          >
            <Select 
              placeholder="Select a strategic goal" 
              size="large" 
              loading={isLoadingGoals}
              onChange={handleGoalChange}
              value={selectedGoal}
            >
              {goalsAndDefaults?.map(goal => (
                <Option key={goal.name} value={goal.name}>{goal.name}</Option>
              ))}
            </Select>
          </Form.Item>
        </Col>
        <Col xs={24} sm={12}>
          <Form.Item 
            name="keyword" 
            rules={[{ required: true, message: 'Please enter a seed keyword.' }]}
            label={<Title level={4}>Seed Keyword</Title>}
          >
            <Input placeholder="e.g., 'AI in marketing' or 'how to start a blog'" size="large" />
          </Form.Item>
        </Col>
      </Row>
      
      <Divider orientation="left" style={{ color: 'rgba(0,0,0,.55)', fontSize: '16px', marginTop: '32px' }}>
        Customize (Optional)
      </Divider>
      <Row gutter={24}>
          <Col xs={24} sm={12}>
            <Form.Item 
              name="min_search_volume" 
              label={
                <span>
                  Min. Monthly Search Volume 
                  <Tooltip title="Only find keywords with at least this many monthly searches.">
                    <QuestionCircleOutlined style={{ marginLeft: 4, color: 'rgba(0,0,0,.45)' }} />
                  </Tooltip>
                </span>
              }
            >
              <InputNumber style={{ width: '100%' }} placeholder="e.g., 500" min={0} />
            </Form.Item>
          </Col>
          <Col xs={24} sm={12}>
            <Form.Item 
              name="max_keyword_difficulty" 
              label={
                <span>
                  Max. SEO Difficulty 
                  <Tooltip title="Only find keywords with a difficulty score below this value (0-100).">
                    <QuestionCircleOutlined style={{ marginLeft: 4, color: 'rgba(0,0,0,.45)' }} />
                  </Tooltip>
                </span>
              }
            >
              <InputNumber style={{ width: '100%' }} placeholder="e.g., 20" min={0} max={100} />
            </Form.Item>
          </Col>
        </Row>

      <Form.Item style={{ marginTop: '32px', marginBottom: 0 }}>
        <Button type="primary" htmlType="submit" icon={<RocketOutlined />} loading={isSubmitting || isLoadingGoals} size="large" block>
          Find Opportunities
        </Button>
      </Form.Item>
    </Form>
  );
};

export default DiscoveryForm;