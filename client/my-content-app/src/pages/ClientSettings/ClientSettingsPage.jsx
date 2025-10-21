// my-content-app/src/pages/ClientSettings/ClientSettingsPage.jsx
// NEW FILE
import React from 'react';
import { Layout, Typography, Form, Input, Button, Spin, Alert } from 'antd';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { getClientSettings, updateClientSettings } from '../../services/clientSettingsService';
import { useNotifications } from '../../context/NotificationContext';

const { Content } = Layout;
const { Title } = Typography;
const { TextArea } = Input;

const ClientSettingsPage = ({ clientId = 'default' }) => {
  const [form] = Form.useForm();
  const queryClient = useQueryClient();
  const { showNotification } = useNotifications();

  const { data: settings, isLoading, isError, error } = useQuery(
    ['clientSettings', clientId],
    () => getClientSettings(clientId),
    {
      enabled: !!clientId,
      onSuccess: (data) => {
        form.setFieldsValue(data);
      }
    }
  );

  const { mutate: updateSettingsMutation, isLoading: isUpdating } = useMutation(
    (newSettings) => updateClientSettings(clientId, newSettings),
    {
      onSuccess: () => {
        showNotification('success', 'Settings Updated', 'Client settings have been saved successfully.');
        queryClient.invalidateQueries(['clientSettings', clientId]);
      },
      onError: (err) => {
        showNotification('error', 'Update Failed', err.message || 'An error occurred while saving settings.');
      }
    }
  );

  const onFinish = (values) => {
    updateSettingsMutation(values);
  };

  if (isLoading) return <Spin tip="Loading settings..." />;
  if (isError) return <Alert message="Error" description={error.message} type="error" showIcon />;

  return (
    <Layout style={{ padding: '24px' }}>
      <Content>
        <Title level={2}>Client AI & Content Settings</Title>
        <Form
          form={form}
          layout="vertical"
          onFinish={onFinish}
          initialValues={settings}
        >
          <Form.Item
            name="brand_tone"
            label="Brand Tone & Voice"
            tooltip="Define the desired tone for the AI-generated content (e.g., professional, witty, conversational)."
          >
            <TextArea rows={4} placeholder="e.g., Professional and authoritative, but accessible to a general audience." />
          </Form.Item>

          <Form.Item
            name="target_audience"
            label="Target Audience"
            tooltip="Describe the primary audience for the content."
          >
            <TextArea rows={4} placeholder="e.g., Marketing managers at mid-sized tech companies." />
          </Form.Item>

          <Form.Item
            name="terms_to_avoid"
            label="Terms to Avoid"
            tooltip="List any specific words or phrases the AI should not use. Separate with commas."
          >
            <Input placeholder="e.g., synergy, disruptive, unicorn" />
          </Form.Item>

          <Form.Item
            name="client_knowledge_base"
            label="Client Knowledge Base"
            tooltip="Provide key facts, product names, and unique selling propositions for your brand. This will be injected into every AI content generation prompt."
          >
            <TextArea rows={6} placeholder="e.g., Our flagship product is 'ProfitPilot', an AI-powered SEO tool designed for small businesses to automate keyword research and content generation. We focus on ROI and actionable insights, not just vanity metrics." />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" loading={isUpdating}>
              Save Settings
            </Button>
          </Form.Item>
        </Form>
      </Content>
    </Layout>
  );
};

export default ClientSettingsPage;
